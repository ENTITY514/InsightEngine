import pandas as pd
import glob
import os
from typing import List, Dict, Optional
import locale

def get_client_details(client_code: int) -> Optional[Dict]:
    try:
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')
        except locale.Error:
            print("Не удалось установить русскую локаль для названий месяцев.")

    full_data = get_full_client_data(client_code)
    if not full_data:
        return None

    transactions_df = full_data['transactions_df']
    monthly_transactions = {}
    if not transactions_df.empty:
        transactions_df['month'] = transactions_df['date'].dt.strftime('%B').str.capitalize()
        grouped_trans = transactions_df.groupby(['month', 'category'])['amount'].sum().round(2)
        for (month, category), amount in grouped_trans.items():
            if month not in monthly_transactions:
                monthly_transactions[month] = {}
            monthly_transactions[month][category] = amount
            
    transfers_df = full_data['transfers_df']
    monthly_transfers = {}
    if not transfers_df.empty:
        transfers_df['month'] = transfers_df['date'].dt.strftime('%B').str.capitalize()
        grouped_transf = transfers_df.groupby(['month', 'type'])['amount'].sum().round(2)
        for (month, type), amount in grouped_transf.items():
            if month not in monthly_transfers:
                monthly_transfers[month] = {}
            monthly_transfers[month][type] = amount
            
    return {
        "monthly_transactions": monthly_transactions,
        "monthly_transfers": monthly_transfers
    }

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data') 

_clients_df: Optional[pd.DataFrame] = None
_transactions_df: Optional[pd.DataFrame] = None
_transfers_df: Optional[pd.DataFrame] = None

def _load_data():
    """
    Загружает все данные из CSV в DataFrame'ы Pandas с явным контролем типов.
    Это техника мастера: быстрая, точная и предсказуемая.
    """
    global _clients_df, _transactions_df, _transfers_df

    clients_file_path = os.path.join(DATA_PATH, 'clients.csv')
    try:
        _clients_df = pd.read_csv(
            clients_file_path,
            dtype={
                'client_code': 'uint16',
                'name': 'str',
                'status': 'category',
                'age': 'uint8',
                'city': 'category',
                'avg_monthly_balance_KZT': 'float64'
            }
        )
        _clients_df.set_index('client_code', inplace=True)
    except FileNotFoundError:
        raise RuntimeError(f"Критическая ошибка: Основной файл данных '{clients_file_path}' не найден.")

    transaction_files = glob.glob(os.path.join(DATA_PATH, 'client_*_transactions_3m.csv'))
    if transaction_files:
        _transactions_df = pd.concat((
            pd.read_csv(f, dtype={'client_code': 'uint16', 'category': 'category', 'amount': 'float64'}, parse_dates=['date'])
            for f in transaction_files
        ), ignore_index=True)
    else:
        _transactions_df = pd.DataFrame()

    transfer_files = glob.glob(os.path.join(DATA_PATH, 'client_*_transfers_3m.csv'))
    if transfer_files:
        _transfers_df = pd.concat((
            pd.read_csv(f, dtype={'client_code': 'uint16', 'type': 'category', 'direction': 'category', 'amount': 'float64'}, parse_dates=['date'])
            for f in transfer_files
        ), ignore_index=True)
    else:
        _transfers_df = pd.DataFrame()

def get_full_client_data(client_code: int) -> Optional[Dict]:
    if _clients_df is None:
        _load_data()

    try:
        client_info = _clients_df.loc[client_code].to_dict()
    except KeyError:
        return None 

    client_transactions = _transactions_df[_transactions_df['client_code'] == client_code]
    client_transfers = _transfers_df[_transfers_df['client_code'] == client_code]

    if not client_transactions.empty:
        total_spending = client_transactions['amount'].sum()
        top_categories_series = client_transactions.groupby('category')['amount'].sum().nlargest(3)
        top_categories = [
            {"category": index, "amount": round(value, 2)}
            for index, value in top_categories_series.items()
        ]
    else:
        total_spending = 0
        top_categories = []

    profile_data = client_info
    profile_data['client_code'] = client_code

    full_data = {
        "profile": profile_data,
        "metrics": {
            "total_spending_3m": round(total_spending, 2),
            "top_categories": top_categories
        },
        "transactions_df": client_transactions,
        "transfers_df": client_transfers
    }
    return full_data

def get_all_clients() -> List[Dict]:
    """Возвращает краткий список всех клиентов (код и имя)."""
    if _clients_df is None:
        _load_data()
    
    if _clients_df is None:
        return []

    clients_list = _clients_df.reset_index()[['client_code', 'name']].to_dict('records')
    return clients_list