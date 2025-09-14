import pandas as pd
from typing import Tuple, List, Dict

# --- КОНСТАНТЫ РАСЧЕТОВ (Техническая дисциплина) ---
FX_SAVING_RATE = 0.01
INVESTMENT_ANNUAL_YIELD = 0.165 
INVESTMENT_BALANCE_SHARE = 0.30 
GOLD_ANNUAL_YIELD = 0.10
GOLD_BALANCE_THRESHOLD = 7_000_000

# --- НОВЫЕ СТРАТЕГИЧЕСКИЕ ПАРАМЕТРЫ ---
# Порог для определения состоятельного клиента
WEALTHY_CLIENT_BALANCE_THRESHOLD = 3_000_000
# Множитель для обеспечения доминирования приоритетных продуктов
WEALTHY_CLIENT_MULTIPLIER = 100 


# --- Функции-оценщики (score_*) остаются БЕЗ ИЗМЕНЕНИЙ ---
# ... (здесь находятся все функции score_* от score_travel_card до score_cash_loan) ...
def score_travel_card(data: dict) -> Tuple[str, float]:
    transactions = data['transactions_df']
    travel_categories = ['Путешествия', 'Такси', 'Отели']
    travel_spending = transactions[transactions['category'].isin(travel_categories)]['amount'].sum()
    benefit = travel_spending * 0.04
    return "Карта для путешествий", round(benefit, 2)

def score_premium_card(data: dict) -> Tuple[str, float]:
    balance = data['profile']['avg_monthly_balance_KZT']
    if balance < 500_000:
        return "Премиальная карта", 0.0
    transactions = data['transactions_df']
    if balance >= 6_000_000: base_rate = 0.04
    elif balance >= 1_000_000: base_rate = 0.03
    else: base_rate = 0.02
    premium_categories = ['Ювелирные украшения', 'Косметика и Парфюмерия', 'Кафе и рестораны']
    non_premium_mask = ~transactions['category'].isin(premium_categories)
    premium_mask = transactions['category'].isin(premium_categories)
    non_premium_benefit = transactions.loc[non_premium_mask, 'amount'].sum() * base_rate
    premium_benefit = transactions.loc[premium_mask, 'amount'].sum() * 0.04
    total_benefit = min(non_premium_benefit + premium_benefit, 300_000)
    return "Премиальная карта", round(total_benefit, 2)

def score_credit_card(data: dict) -> Tuple[str, float]:
    transactions = data['transactions_df']
    if transactions.empty:
        return "Кредитная карта", 0.0
    top_categories_series = transactions.groupby('category')['amount'].sum().nlargest(3)
    top_categories_list = top_categories_series.index.tolist()
    online_categories_list = ['Играем дома', 'Кино', 'Едим дома']
    all_promo_categories = set(top_categories_list + online_categories_list)
    promo_spending_mask = transactions['category'].isin(all_promo_categories)
    total_promo_spending = transactions.loc[promo_spending_mask, 'amount'].sum()
    total_benefit = total_promo_spending * 0.10
    return "Кредитная карта", round(total_benefit, 2)

def score_fx_exchange(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    fx_operations = transfers[transfers['type'].isin(['fx_buy', 'fx_sell'])]
    if fx_operations.empty: return "Обмен валют", 0.0
    fx_volume = fx_operations['amount'].sum()
    benefit = fx_volume * FX_SAVING_RATE
    return "Обмен валют", round(benefit, 2)

def score_investments(data: dict) -> Tuple[str, float]:
    balance = data['profile']['avg_monthly_balance_KZT']
    if balance < 50_000: 
        return "Инвестиции", 0.0
    investable_amount = balance * INVESTMENT_BALANCE_SHARE
    benefit = investable_amount * INVESTMENT_ANNUAL_YIELD
    return "Инвестиции", round(benefit, 2)

def score_gold_bars(data: dict) -> Tuple[str, float]:
    balance = data['profile']['avg_monthly_balance_KZT']
    if balance < GOLD_BALANCE_THRESHOLD: return "Золотые слитки", 0.0
    investable_amount = balance * INVESTMENT_BALANCE_SHARE
    benefit = investable_amount * GOLD_ANNUAL_YIELD
    return "Золотые слитки", round(benefit, 2)

def score_sber_deposit(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    deposit_activity = transfers[transfers['type'].str.contains('deposit', na=False)]
    if deposit_activity.empty and balance > 1_000_000:
        annual_benefit = balance * 0.165
        return "Депозит Сберегательный", round(annual_benefit, 2)
    return "Депозит Сберегательный", 0.0

def score_nakop_deposit(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    topup_activity = transfers[transfers['type'] == 'deposit_topup_out']
    if not topup_activity.empty:
        annual_benefit = balance * 0.155
        return "Депозит Накопительный", round(annual_benefit, 2)
    return "Депозит Накопительный", 0.0

def score_multi_deposit(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    fx_activity = transfers[transfers['type'].isin(['deposit_fx_topup_out', 'deposit_fx_withdraw_in', 'fx_buy', 'fx_sell'])]
    if not fx_activity.empty:
        annual_benefit = balance * 0.145
        return "Депозит Мультивалютный", round(annual_benefit, 2)
    return "Депозит Мультивалютный", 0.0

def score_cash_loan(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    if transfers.empty:
        return "Кредит наличными", 0.0
    total_salary = transfers[transfers['type'] == 'salary_in']['amount'].sum()
    if total_salary == 0:
        return "Кредит наличными", 0.0
    loan_payments = transfers[transfers['type'] == 'loan_payment_out']['amount'].sum()
    p2p_payments = transfers[transfers['type'] == 'p2p_out']['amount'].sum()
    utilities_payments = transfers[transfers['type'] == 'utilities_out']['amount'].sum()
    total_committed_spending = loan_payments + p2p_payments + utilities_payments
    spending_to_income_ratio = total_committed_spending / total_salary
    if spending_to_income_ratio > 0.65:
        return "Кредит наличными", 1.0
    total_transactions_spending = data['metrics']['total_spending_3m']
    if (total_transactions_spending + total_committed_spending) > total_salary:
        return "Кредит наличными", 1.0
    return "Кредит наличными", 0.0


# --- Модуль расчета излишка (без изменений) ---
def _calculate_monthly_surplus(data: Dict[str, pd.DataFrame]) -> float:
    transfers = data['transfers_df']
    total_inflow_transfers = transfers[transfers['type'].str.endswith('_in')]['amount'].sum()
    total_outflow_transfers = transfers[transfers['type'].str.endswith('_out')]['amount'].sum()
    total_transactions_spending = data['metrics']['total_spending_3m']
    total_outflow = total_outflow_transfers + total_transactions_spending
    surplus_3m = total_inflow_transfers - total_outflow
    return surplus_3m / 3

# --- УСОВЕРШЕНСТВОВАННАЯ ГЛАВНАЯ ФУНКЦИЯ-ОРКЕСТРАТОР ---
def rank_top_products(full_data: dict) -> list[tuple[str, float]]:
    if not full_data: return []

    # --- ПРОТОКОЛ ПРИОРИТЕТА: ЭТАП 1 - ИДЕНТИФИКАЦИЯ ---
    balance = full_data['profile']['avg_monthly_balance_KZT']
    is_wealthy_client = balance > WEALTHY_CLIENT_BALANCE_THRESHOLD
    priority_products = ["Депозит Сберегательный", "Золотые слитки", "Депозит Мультивалютный"]

    # === ВРАТА 1: ОПРЕДЕЛЕНИЕ ИСТИНЫ ===
    monthly_surplus = _calculate_monthly_surplus(full_data)
    
    # === ВРАТА 2: ОТСЕЧЕНИЕ ЛИШНЕГО ===
    segment_whitelist = []
    if monthly_surplus < 100000:
        segment_whitelist = ["Кредитная карта", "Карта для путешествий", "Премиальная карта", "Кредит наличными"]
    elif 100000 <= monthly_surplus < 1000000:
        segment_whitelist = ["Инвестиции", "Депозит Накопительный"]
    else: # >= 1000000
        segment_whitelist = ["Инвестиции", "Золотые слитки", "Депозит Мультивалютный", "Депозит Сберегательный"]

    # --- ПРОТОКОЛ ПРИОРИТЕТА: ЭТАП 2 - ГАРАНТИЯ РАССМОТРЕНИЯ ---
    if is_wealthy_client:
        for p in priority_products:
            if p not in segment_whitelist:
                segment_whitelist.append(p)

    # === ВРАТА 3: ВОЗВЫШЕНИЕ СИЛЬНЕЙШЕГО ===
    scorers = [
        score_travel_card, score_premium_card, score_credit_card,
        score_fx_exchange, score_investments, score_gold_bars,
        score_sber_deposit, score_nakop_deposit, score_multi_deposit,
        score_cash_loan,
    ]
    
    all_results = {product: benefit for product, benefit in [scorer(full_data) for scorer in scorers]}
    
    # --- ПРОТОКОЛ ПРИОРИТЕТА: ЭТАП 3 - ДОМИНИРОВАНИЕ В РЕЙТИНГЕ ---
    if is_wealthy_client:
        for product_name in priority_products:
            if product_name in all_results:
                all_results[product_name] *= WEALTHY_CLIENT_MULTIPLIER

    # Применяем фильтр "белого списка"
    surviving_products_list = [(p, b) for p, b in all_results.items() if p in segment_whitelist and b > 0]
    
    # Ранжируем выживших
    surviving_products_list.sort(key=lambda x: x[1], reverse=True)
    
    # Гарантируем наличие 4 рекомендаций
    if len(surviving_products_list) < 4:
        recommended_names = [p[0] for p in surviving_products_list]
        for product_name in segment_whitelist:
            if len(surviving_products_list) >= 4:
                break
            if product_name not in recommended_names:
                surviving_products_list.append((product_name, 0.0))

    return surviving_products_list[:4]