import pandas as pd

# ===================================================================
# Функции-оценщики (Scorers)
# Каждая функция принимает полные данные клиента и возвращает
# кортеж: (Название продукта, Оценка выгоды в KZT)
# ===================================================================

def score_travel_card(data: dict) -> (str, float):
    """Оценивает выгоду от Карты для путешествий."""
    transactions = data['transactions_df']
    travel_categories = ['Путешествия', 'Такси', 'Отели'] # Включаем и отели
    
    # Считаем траты по релевантным категориям
    travel_spending = transactions[transactions['category'].isin(travel_categories)]['amount'].sum()
    
    # Кешбэк 4%
    benefit = travel_spending * 0.04
    return "Карта для путешествий", round(benefit, 2)

def score_premium_card(data: dict) -> (str, float):
    """Оценивает выгоду от Премиальной карты."""
    transactions = data['transactions_df']
    balance = data['profile']['avg_monthly_balance_KZT']
    
    # Определяем базовый кешбэк
    if balance >= 6_000_000:
        base_cashback_rate = 0.04
    elif balance >= 1_000_000:
        base_cashback_rate = 0.03
    else:
        base_cashback_rate = 0.02

    base_benefit = transactions['amount'].sum() * base_cashback_rate
    
    # Повышенный кешбэк 4% на премиум-категории
    premium_categories = ['Ювелирные украшения', 'Косметика и Парфюмерия', 'Кафе и рестораны']
    premium_spending = transactions[transactions['category'].isin(premium_categories)]['amount'].sum()
    
    # Досчитываем дополнительную выгоду (4% - базовая ставка)
    additional_benefit = premium_spending * (0.04 - base_cashback_rate)
    
    total_benefit = base_benefit + additional_benefit
    
    # Ограничение кешбэка 100 000 в месяц (300 000 за 3 месяца)
    total_benefit = min(total_benefit, 300_000)
    
    return "Премиальная карта", round(total_benefit, 2)

def score_credit_card(data: dict) -> (str, float):
    """Оценивает выгоду от Кредитной карты."""
    transactions = data['transactions_df']
    
    # 10% на топ-3 категории (берем из уже посчитанных метрик)
    top_categories_spending = sum(cat['amount'] for cat in data['metrics']['top_categories'])
    benefit_from_top_cat = top_categories_spending * 0.10

    # 10% на онлайн-услуги
    online_categories = ['Играем дома', 'Смотрим дома', 'Едим дома']
    online_spending = transactions[transactions['category'].isin(online_categories)]['amount'].sum()
    benefit_from_online = online_spending * 0.10
    
    return "Кредитная карта", round(benefit_from_top_cat + benefit_from_online, 2)

def score_deposits(data: dict) -> (str, float):
    """Оценивает выгоду от Депозитов, выбирая лучший."""
    balance = data['profile']['avg_monthly_balance_KZT']
    
    # Рассчитываем годовой доход и берем за 3 месяца (делим на 4)
    # Считаем выгоду от лучшей ставки (Сберегательный)
    benefit = (balance * 0.165) / 4
    
    return "Депозит Сберегательный", round(benefit, 2)

# ... (по аналогии можно добавить оценщики для других продуктов)
# Для хакатона 4-5 ключевых продуктов будет достаточно для отличного результата.

# ===================================================================
# Главная функция-оркестратор
# ===================================================================

def find_best_product(client_code: int, full_data: dict) -> (str, float):
    """
    Принимает полные данные клиента, прогоняет через все оценщики
    и возвращает лучший продукт и его выгоду.
    """
    if not full_data:
        return None, None
        
    # Список всех наших функций-оценщиков
    scorers = [
        score_travel_card,
        score_premium_card,
        score_credit_card,
        score_deposits,
    ]
    
    results = []
    for scorer in scorers:
        results.append(scorer(full_data))
        
    # Сортируем результаты по выгоде (по убыванию)
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Возвращаем лучший результат
    best_product, best_benefit = results[0]
    
    return best_product, best_benefit