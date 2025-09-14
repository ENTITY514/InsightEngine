import pandas as pd
from typing import Tuple

FX_SAVING_RATE = 0.01  

INVESTMENT_ANNUAL_YIELD = 0.15 
INVESTMENT_BALANCE_SHARE = 0.20 

GOLD_ANNUAL_YIELD = 0.10 
GOLD_BALANCE_THRESHOLD = 7_000_000


def score_travel_card(data: dict) -> Tuple[str, float]:
    """Выгода = Кешбэк 4% на релевантные категории."""
    transactions = data['transactions_df']
    travel_categories = ['Путешествия', 'Такси', 'Отели']
    travel_spending = transactions[transactions['category'].isin(travel_categories)]['amount'].sum()
    benefit = travel_spending * 0.04
    return "Карта для путешествий", round(benefit, 2)

def score_premium_card(data: dict) -> Tuple[str, float]:
    """Выгода = Суммарный кешбэк с учетом базовой и премиальной ставок."""
    transactions = data['transactions_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    
    if balance >= 6_000_000: base_rate = 0.04
    elif balance >= 1_000_000: base_rate = 0.03
    else: base_rate = 0.02

    premium_categories = ['Ювелирные украшения', 'Косметика и Парфюмерия', 'Кафе и рестораны']
    
    non_premium_mask = ~transactions['category'].isin(premium_categories)
    premium_mask = transactions['category'].isin(premium_categories)

    non_premium_benefit = transactions.loc[non_premium_mask, 'amount'].sum() * base_rate
    premium_benefit = transactions.loc[premium_mask, 'amount'].sum() * 0.04
    
    total_benefit = min(non_premium_benefit + premium_benefit, 300_000) # Лимит за 3 месяца
    return "Премиальная карта", round(total_benefit, 2)

def score_credit_card(data: dict) -> Tuple[str, float]:
    """
    Выгода = Кешбэк 10% на топ-3 категории расходов И на онлайн-услуги.
    Расчет исключает двойное начисление и ограничен лимитом.
    """
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
    """Выгода = Предполагаемая экономия на комиссии от объема обмена."""
    transfers = data['transfers_df']
    fx_operations = transfers[transfers['type'].isin(['fx_buy', 'fx_sell'])]
    
    # Сигнал: если клиент уже менял валюту, продукт ему релевантен.
    if fx_operations.empty:
        return "Обмен валют", 0.0
        
    fx_volume = fx_operations['amount'].sum()
    benefit = fx_volume * FX_SAVING_RATE # Экономия, а не оборот
    return "Обмен валют", round(benefit, 2)

def score_investments(data: dict) -> Tuple[str, float]:
    """Выгода = Потенциальный доход от инвестирования части свободных средств."""
    balance = data['profile']['avg_monthly_balance_KZT']
    
    # Сигнал: если у клиента есть стабильный остаток, можно предложить инвестиции.
    if balance < 500_000: # Порог входа
        return "Инвестиции", 0.0
        
    # Расчет выгоды как потенциальный доход за 3 месяца (квартал)
    investable_amount = balance * INVESTMENT_BALANCE_SHARE
    quarterly_yield = INVESTMENT_ANNUAL_YIELD / 4
    benefit = investable_amount * quarterly_yield
    return "Инвестиции", round(benefit, 2)

def score_gold_bars(data: dict) -> Tuple[str, float]:
    """Выгода = Потенциальный доход от вложения в золото как защитный актив."""
    balance = data['profile']['avg_monthly_balance_KZT']
    
    if balance < GOLD_BALANCE_THRESHOLD:
        return "Золотые слитки", 0.0
        
    investable_amount = balance * INVESTMENT_BALANCE_SHARE # Можно использовать ту же логику
    quarterly_yield = GOLD_ANNUAL_YIELD / 4
    benefit = investable_amount * quarterly_yield
    return "Золотые слитки", round(benefit, 2)

def score_sber_deposit(data: dict) -> Tuple[str, float]:
    """Выгода = Процентный доход. Только для неактивных денег."""
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    
    deposit_activity = transfers[transfers['type'].str.contains('deposit', na=False)]
    
    if deposit_activity.empty and balance > 300_000:
        benefit = (balance * 0.165) / 4 # Расчет за 3 месяца
        return "Депозит Сберегательный", round(benefit, 2)
    
    return "Депозит Сберегательный", 0.0

def score_nakop_deposit(data: dict) -> Tuple[str, float]:
    """Выгода = Процентный доход. Для тех, кто пополняет."""
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    topup_activity = transfers[transfers['type'] == 'deposit_topup_out']
    
    if not topup_activity.empty:
        benefit = (balance * 0.155) / 4
        return "Депозит Накопительный", round(benefit, 2)
        
    return "Депозит Накопительный", 0.0

def score_multi_deposit(data: dict) -> Tuple[str, float]:
    """Выгода = Процентный доход. Для тех, кто работает с валютой."""
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    fx_activity = transfers[transfers['type'].isin(['deposit_fx_topup_out', 'deposit_fx_withdraw_in', 'fx_buy', 'fx_sell'])]
    
    if not fx_activity.empty:
        benefit = (balance * 0.145) / 4
        return "Депозит Мультивалютный", round(benefit, 2)

    return "Депозит Мультивалютный", 0.0

def score_cash_loan(data: dict) -> Tuple[str, float]:
    """Кредит не несет прямой выгоды в KZT. Он решает потребность. Оценка 0."""
    # Логику определения потребности можно улучшить, но выгоду он не генерирует.
    return "Кредит наличными", 0.0

# ===================================================================
# Главная функция-оркестратор
# ===================================================================

def rank_top_products(full_data: dict) -> list[tuple[str, float]]:
    """
    Прогоняет данные через все оценщики и возвращает
    ранжированный список из топ-4 продуктов и их выгод.
    """
    if not full_data:
        return []
        
    scorers = [
        score_travel_card,
        score_premium_card,
        score_credit_card,
        score_fx_exchange,
        score_investments,
        score_gold_bars,
        score_sber_deposit,
        score_nakop_deposit,
        score_multi_deposit,
        score_cash_loan,
    ]
    
    results = []
    for scorer in scorers:
        results.append(scorer(full_data))
        
    # Сортировка по выгоде
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Отфильтровываем продукты с нулевой или отрицательной выгодой
    positive_results = [res for res in results if res[1] > 0]
    
    # Возвращаем до 4 лучших результатов
    return positive_results[:4]