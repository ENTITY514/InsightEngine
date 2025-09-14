import pandas as pd
from typing import Tuple, List, Dict, Set

FX_SAVING_RATE = 0.01
INVESTMENT_ANNUAL_YIELD = 0.165 
INVESTMENT_BALANCE_SHARE = 0.30 
GOLD_ANNUAL_YIELD = 0.10
GOLD_BALANCE_THRESHOLD = 7_000_000
CAPITALIST_CLIENT_THRESHOLD = 1_000_000
PREMIUM_CARD_MIN_BALANCE = 400_000

BEHAVIORAL_BOOSTS = {
    "HIGH_FX_ACTIVITY": {"Депозит Мультивалютный": 3.0},
    "HAS_INVESTMENTS": {"Инвестиции": 5.0},
    "HIGH_P2P_OUTFLOW": {"Премиальная карта": 1.5},
    "HAS_LOAN_PAYMENTS": {"Кредитная карта": 1.5}
}


def score_premium_card(data: dict) -> Tuple[str, float]:
    """Внедрен новый порог отсечения."""
    balance = data['profile']['avg_monthly_balance_KZT']
    if balance < PREMIUM_CARD_MIN_BALANCE:
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

def score_travel_card(data: dict) -> Tuple[str, float]:
    transactions = data['transactions_df']
    travel_categories = ['Путешествия', 'Такси', 'Отели']
    travel_spending = transactions[transactions['category'].isin(travel_categories)]['amount'].sum()
    benefit = travel_spending * 0.04
    return "Карта для путешествий", round(benefit, 2)

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
    if not topup_activity.empty or balance > CAPITALIST_CLIENT_THRESHOLD:
        annual_benefit = balance * 0.155
        return "Депозит Накопительный", round(annual_benefit, 2)
    return "Депозит Накопительный", 0.0

def score_multi_deposit(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    fx_activity = transfers[transfers['type'].isin(['deposit_fx_topup_out', 'deposit_fx_withdraw_in', 'fx_buy', 'fx_sell'])]
    if not fx_activity.empty or balance > CAPITALIST_CLIENT_THRESHOLD:
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

def _get_behavioral_tags(transfers_df: pd.DataFrame) -> Set[str]:
    """Анализирует историю переводов и возвращает набор поведенческих тегов."""
    tags = set()
    if transfers_df.empty:
        return tags

    fx_operations_count = transfers_df[transfers_df['type'].isin(['fx_buy', 'fx_sell'])].shape[0]
    if fx_operations_count > 2: 
        tags.add("HIGH_FX_ACTIVITY")
        
    investment_ops_count = transfers_df[transfers_df['type'].str.contains('invest', na=False)].shape[0]
    if investment_ops_count > 0:
        tags.add("HAS_INVESTMENTS")
        
    p2p_outflow_sum = transfers_df[transfers_df['type'] == 'p2p_out']['amount'].sum()
    if p2p_outflow_sum > 200000: 
        tags.add("HIGH_P2P_OUTFLOW")

    loan_payments_count = transfers_df[transfers_df['type'] == 'loan_payment_out'].shape[0]
    if loan_payments_count > 0:
        tags.add("HAS_LOAN_PAYMENTS")
        
    return tags

def _calculate_monthly_surplus(data: Dict[str, pd.DataFrame]) -> float:
    transfers = data['transfers_df']
    total_inflow_transfers = transfers[transfers['type'].str.endswith('_in')]['amount'].sum()
    total_outflow_transfers = transfers[transfers['type'].str.endswith('_out')]['amount'].sum()
    total_transactions_spending = data['metrics']['total_spending_3m']
    total_outflow = total_outflow_transfers + total_transactions_spending
    surplus_3m = total_inflow_transfers - total_outflow
    return surplus_3m / 3

def rank_top_products(full_data: dict) -> list[tuple[str, float]]:
    if not full_data: return []

    balance = full_data['profile']['avg_monthly_balance_KZT']
    
    scorers = [
        score_travel_card, score_premium_card, score_credit_card,
        score_fx_exchange, score_investments, score_gold_bars,
        score_sber_deposit, score_nakop_deposit, score_multi_deposit,
        score_cash_loan,
    ]
    all_results = {p: b for p, b in [scorer(full_data) for scorer in scorers]}

    behavioral_tags = _get_behavioral_tags(full_data['transfers_df'])
    
    for tag in behavioral_tags:
        if tag in BEHAVIORAL_BOOSTS:
            for product, multiplier in BEHAVIORAL_BOOSTS[tag].items():
                if product in all_results:
                    all_results[product] *= multiplier
    
    if balance > CAPITALIST_CLIENT_THRESHOLD:
        guaranteed_products = ["Депозит Сберегательный", "Депозит Накопительный", "Депозит Мультивалютный"]
        final_recommendations = [(p, all_results.get(p, 0.0)) for p in guaranteed_products]
        remaining_products = sorted([(p, b) for p, b in all_results.items() if p not in guaranteed_products], key=lambda x: x[1], reverse=True)
        if remaining_products:
            final_recommendations.append(remaining_products[0])
        return final_recommendations[:4]
    else:
        monthly_surplus = _calculate_monthly_surplus(full_data)
        segment_whitelist = []
        if monthly_surplus < 100000:
            segment_whitelist = ["Кредитная карта", "Карта для путешествий", "Премиальная карта", "Кредит наличными"]
        elif 100000 <= monthly_surplus < 1000000:
            segment_whitelist = ["Инвестиции", "Депозит Накопительный"]
        else:
            segment_whitelist = ["Инвестиции", "Золотые слитки", "Депозит Мультивалютный", "Депозит Сберегательный"]

        surviving_products_list = [(p, b) for p, b in all_results.items() if p in segment_whitelist and b > 0]
        surviving_products_list.sort(key=lambda x: x[1], reverse=True)
        
        if len(surviving_products_list) < 4:
            recommended_names = [p[0] for p in surviving_products_list]
            for product_name in segment_whitelist:
                if len(surviving_products_list) >= 4:
                    break
                if product_name not in recommended_names:
                    surviving_products_list.append((product_name, 0.0))
        return surviving_products_list[:4]