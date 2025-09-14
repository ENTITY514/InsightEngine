import pandas as pd
from typing import Tuple, List

# --- КОНСТАНТЫ РАСЧЕТОВ (Техническая дисциплина) ---
FX_SAVING_RATE = 0.01
INVESTMENT_ANNUAL_YIELD = 0.15
INVESTMENT_BALANCE_SHARE = 0.20
GOLD_ANNUAL_YIELD = 0.10
GOLD_BALANCE_THRESHOLD = 7_000_000

# --- СТРАТЕГИЧЕСКИЕ КОЭФФИЦИЕНТЫ (Мудрость рекомендации) ---
STRATEGIC_COEFFICIENTS = {
    "SAVER": { # Клиент-Накопитель
        "products": ["Депозит Сберегательный", "Депозит Накопительный"],
        "multiplier": 1.8 
    },
    "SPENDER": { # Клиент-Транжира
        "products": ["Кредитная карта", "Премиальная карта"],
        "multiplier": 1.5
    },
    "TRAVELER": { # Клиент-Путешественник
        "products": ["Карта для путешествий", "Депозит Мультивалютный", "Обмен валют"],
        "multiplier": 1.7
    }
}

# --- Функции-оценщики (score_*) остаются БЕЗ ИЗМЕНЕНИЙ ---
def score_travel_card(data: dict) -> Tuple[str, float]:
    transactions = data['transactions_df']
    travel_categories = ['Путешествия', 'Такси', 'Отели']
    travel_spending = transactions[transactions['category'].isin(travel_categories)]['amount'].sum()
    benefit = travel_spending * 0.04
    return "Карта для путешествий", round(benefit, 2)

def score_premium_card(data: dict) -> Tuple[str, float]:
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
    if balance < 500_000: return "Инвестиции", 0.0
    investable_amount = balance * INVESTMENT_BALANCE_SHARE
    quarterly_yield = INVESTMENT_ANNUAL_YIELD / 4
    benefit = investable_amount * quarterly_yield
    return "Инвестиции", round(benefit, 2)

def score_gold_bars(data: dict) -> Tuple[str, float]:
    balance = data['profile']['avg_monthly_balance_KZT']
    if balance < GOLD_BALANCE_THRESHOLD: return "Золотые слитки", 0.0
    investable_amount = balance * INVESTMENT_BALANCE_SHARE
    quarterly_yield = GOLD_ANNUAL_YIELD / 4
    benefit = investable_amount * quarterly_yield
    return "Золотые слитки", round(benefit, 2)

def score_sber_deposit(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    deposit_activity = transfers[transfers['type'].str.contains('deposit', na=False)]
    if deposit_activity.empty and balance > 300_000:
        quarterly_benefit = (balance * 0.165) / 4
        return "Депозит Сберегательный", round(quarterly_benefit, 2)
    return "Депозит Сберегательный", 0.0

def score_nakop_deposit(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    topup_activity = transfers[transfers['type'] == 'deposit_topup_out']
    if not topup_activity.empty:
        quarterly_benefit = (balance * 0.155) / 4
        return "Депозит Накопительный", round(quarterly_benefit, 2)
    return "Депозит Накопительный", 0.0

def score_multi_deposit(data: dict) -> Tuple[str, float]:
    transfers = data['transfers_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    fx_activity = transfers[transfers['type'].isin(['deposit_fx_topup_out', 'deposit_fx_withdraw_in', 'fx_buy', 'fx_sell'])]
    if not fx_activity.empty:
        quarterly_benefit = (balance * 0.145) / 4
        return "Депозит Мультивалютный", round(quarterly_benefit, 2)
    return "Депозит Мультивалютный", 0.0

def score_cash_loan(data: dict) -> Tuple[str, float]:
    return "Кредит наличными", 0.0

# --- Новый модуль: Диагностика профиля клиента ---
def _get_client_profile_type(data: dict) -> List[str]:
    profile_tags = []
    balance = data['profile']['avg_monthly_balance_KZT']
    total_spending = data['metrics']['total_spending_3m']
    
    # Определение "Накопителя"
    if balance > 200_000 and balance > total_spending:
        profile_tags.append("SAVER")
        
    # Определение "Транжиры"
    if total_spending > 500_000 and total_spending > balance * 2:
        profile_tags.append("SPENDER")
        
    # Определение "Путешественника"
    transactions = data['transactions_df']
    travel_spending = transactions[transactions['category'].isin(['Путешествия', 'Такси', 'Отели'])]['amount'].sum()
    if travel_spending > total_spending * 0.1: # Если траты на путешествия > 10% от всех трат
        profile_tags.append("TRAVELER")
        
    return profile_tags

# --- Финальная версия главной функции-оркестратора ---
def rank_top_products(full_data: dict) -> list[tuple[str, float]]:
    if not full_data: return []

    scorers = [
        score_travel_card, score_premium_card, score_credit_card,
        score_fx_exchange, score_investments, score_gold_bars,
        score_sber_deposit, score_nakop_deposit, score_multi_deposit,
        score_cash_loan,
    ]
    
    # 1. Расчет честной, базовой выгоды (Уровень Техники)
    base_results = {product: benefit for product, benefit in [scorer(full_data) for scorer in scorers]}
    
    # 2. Определение профиля клиента (Уровень Стратегии)
    client_profile_tags = _get_client_profile_type(full_data)
    
    # 3. Применение стратегических коэффициентов
    strategic_results = []
    for product, benefit in base_results.items():
        new_benefit = benefit
        for tag in client_profile_tags:
            if product in STRATEGIC_COEFFICIENTS[tag]["products"]:
                new_benefit *= STRATEGIC_COEFFICIENTS[tag]["multiplier"]
        strategic_results.append((product, new_benefit))

    # 4. Ранжирование, сравнение с текущей картой и выбор лучших
    strategic_results.sort(key=lambda x: x[1], reverse=True)

    transactions = full_data['transactions_df']
    current_cards = []
    if not transactions.empty:
        current_cards = transactions['product'].unique().tolist()

    current_card_benefit = 0
    current_card_name = None
    # Важно: выгоду текущей карты берем из честных, базовых расчетов
    for card_name in current_cards:
        if card_name in base_results:
            current_card_benefit = base_results[card_name]
            current_card_name = card_name
            break
    
    best_new_product_benefit = 0
    # Лучший новый продукт ищем уже в стратегическом рейтинге
    for product, benefit in strategic_results:
        if product not in current_cards and benefit > 0:
            best_new_product_benefit = benefit
            break

    final_recommendations = []
    # Сравниваем честную выгоду текущей карты со стратегической выгодой новой
    if current_card_benefit >= best_new_product_benefit and current_card_name is not None:
        final_recommendations.append(("Подтверждение выгоды", current_card_benefit, current_card_name))
        other_new_products = [res for res in strategic_results if res[0] not in current_cards and res[1] > 0]
        final_recommendations.extend(other_new_products)
    else:
        final_recommendations = [res for res in strategic_results if res[0] not in current_cards and res[1] > 0]
        
    return [(res[0], res[1]) for res in final_recommendations[:4]]