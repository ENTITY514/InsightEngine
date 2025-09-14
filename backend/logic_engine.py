import pandas as pd
from typing import Tuple, List

# --- КОНСТАНТЫ РАСЧЕТОВ (Техническая дисциплина) ---
FX_SAVING_RATE = 0.01
INVESTMENT_ANNUAL_YIELD = 0.165 
INVESTMENT_BALANCE_SHARE = 0.30 
GOLD_ANNUAL_YIELD = 0.10
GOLD_BALANCE_THRESHOLD = 7_000_000

# --- СТРАТЕГИЧЕСКИЕ КОЭФФИЦИЕНТЫ (Мудрость рекомендации) ---
STRATEGIC_COEFFICIENTS = {
    "SAVER": {
        "products": ["Депозит Накопительный"], # Сберегательный теперь для инвесторов
        "multiplier": 1.8 
    },
    "SPENDER": {
        "products": ["Кредитная карта", "Премиальная карта"],
        "multiplier": 1.5
    },
    "TRAVELER": {
        "products": ["Карта для путешествий", "Депозит Мультивалютный", "Обмен валют"],
        "multiplier": 1.7
    },
    # ИЗМЕНЕНИЕ 4.1: Профиль "ИНВЕСТОР" переориентирован на продукты сохранения капитала.
    "INVESTOR": { 
        "products": ["Депозит Сберегательный", "Золотые слитки"],
        "multiplier": 2.5 
    },
    # ИЗМЕНЕНИЕ 4.2: Новый профиль для агрессивного продвижения инвестиций начинающим.
    "NOVICE_INVESTOR": {
        "products": ["Инвестиции"],
        "multiplier": 2.2 # Сильный множитель для обеспечения приоритета
    }
}

# --- Функции-оценщики (score_*) ---

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

# ИЗМЕНЕНИЕ 1: Порог входа в инвестиции снижен для привлечения начинающих.
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

# ИЗМЕНЕНИЕ 2: Порог для сберегательного депозита повышен. Это продукт для состоятельных.
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

# ИЗМЕНЕНИЕ 3: Введена новая, более точная сегментация клиентов.
def _get_client_profile_type(data: dict) -> List[str]:
    profile_tags = []
    balance = data['profile']['avg_monthly_balance_KZT']
    total_spending = data['metrics']['total_spending_3m']
    
    if balance >= 1_000_000:
        profile_tags.append("INVESTOR")
    elif 50_000 <= balance < 1_000_000: # Новый сегмент
        profile_tags.append("NOVICE_INVESTOR")

    if balance > 200_000 and balance > total_spending:
        profile_tags.append("SAVER")
    if total_spending > 500_000 and total_spending > balance * 2:
        profile_tags.append("SPENDER")
        
    transactions = data['transactions_df']
    travel_spending = transactions[transactions['category'].isin(['Путешествия', 'Такси', 'Отели'])]['amount'].sum()
    if total_spending > 0 and travel_spending / total_spending > 0.1:
        profile_tags.append("TRAVELER")
        
    return list(set(profile_tags)) # Убираем возможные дубли

def rank_top_products(full_data: dict) -> list[tuple[str, float]]:
    if not full_data: return []

    scorers = [
        score_travel_card, score_premium_card, score_credit_card,
        score_fx_exchange, score_investments, score_gold_bars,
        score_sber_deposit, score_nakop_deposit, score_multi_deposit,
        score_cash_loan,
    ]
    
    base_results = {product: benefit for product, benefit in [scorer(full_data) for scorer in scorers]}
    client_profile_tags = _get_client_profile_type(full_data)
    
    strategic_results = []
    for product, benefit in base_results.items():
        new_benefit = benefit
        for tag in client_profile_tags:
            if tag in STRATEGIC_COEFFICIENTS and product in STRATEGIC_COEFFICIENTS[tag]["products"]:
                new_benefit *= STRATEGIC_COEFFICIENTS[tag]["multiplier"]
        strategic_results.append((product, new_benefit))

    strategic_results.sort(key=lambda x: x[1], reverse=True)

    transactions = full_data['transactions_df']
    current_cards = []
    if not transactions.empty:
        current_cards = transactions['product'].unique().tolist()

    final_recommendations = [res for res in strategic_results if res[0] not in current_cards and res[1] > 0]
    
    if len(final_recommendations) < 4:
        fallback_products = [
            "Депозит Сберегательный", "Инвестиции", "Премиальная карта",
            "Кредитная карта", "Депозит Накопительный"
        ]
        recommended_product_names = [rec[0] for rec in final_recommendations]
        for product in fallback_products:
            if len(final_recommendations) >= 4:
                break
            if product not in recommended_product_names and product not in current_cards:
                final_recommendations.append((product, 0.0))

    return final_recommendations[:4]