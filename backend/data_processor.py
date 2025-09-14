import pandas as pd
import glob
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data')

_clients_df = None
_transactions_df = None
_transfers_df = None

def _load_data():
    global _clients_df, _transactions_df, _transfers_df
    clients_file_path = os.path.join(DATA_PATH, 'clients.csv')
    try:
        _clients_df = pd.read_csv(clients_file_path)
        _clients_df.set_index('client_code', inplace=True)
    except FileNotFoundError:
        print(f"Критическая ошибка: файл {clients_file_path} не найден!")
        return

    transaction_files = glob.glob(os.path.join(DATA_PATH, 'client_*_transactions_3m.csv'))
    if transaction_files:
        _transactions_df = pd.concat((pd.read_csv(f) for f in transaction_files), ignore_index=True)
    else:
        _transactions_df = pd.DataFrame()

    transfer_files = glob.glob(os.path.join(DATA_PATH, 'client_*_transfers_3m.csv'))
    if transfer_files:
        _transfers_df = pd.concat((pd.read_csv(f) for f in transfer_files), ignore_index=True)
    else:
        _transfers_df = pd.DataFrame()

# ===================================================================
# ИЗМЕНЕНИЕ: Теперь функция возвращает и сырые данные для анализа
# ===================================================================
def get_full_client_data(client_code: int) -> dict:
    """
    Собирает и возвращает полный профиль клиента, включая
    DataFrame'ы с его транзакциями и переводами.
    """
    if _clients_df is None:
        _load_data()
        if _clients_df is None:
            return None

    try:
        client_info = _clients_df.loc[client_code].to_dict()
    except KeyError:
        return None

    client_transactions = _transactions_df[_transactions_df['client_code'] == client_code]
    client_transfers = _transfers_df[_transfers_df['client_code'] == client_code]

    total_spending = 0
    top_categories = []
    if not client_transactions.empty:
        total_spending = client_transactions['amount'].sum()
        top_categories_series = client_transactions.groupby('category')['amount'].sum().nlargest(3)
        top_categories = [
            {"category": index, "amount": round(value, 2)}
            for index, value in top_categories_series.items()
        ]

    # Собираем всё в единый словарь
    full_data = {
        "profile": {
            "client_code": client_code,
            "name": client_info['name'],
            "status": client_info['status'],
            "age": client_info['age'],
            "city": client_info['city'],
            "avg_monthly_balance_KZT": client_info['avg_monthly_balance_KZT'],
        },
        "metrics": {
            "total_spending_3m": round(total_spending, 2),
            "top_categories": top_categories
        },
        # Добавляем сами данные для глубокого анализа
        "transactions_df": client_transactions,
        "transfers_df": client_transfers
    }
    return full_data