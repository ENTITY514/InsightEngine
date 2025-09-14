import pandas as pd
import locale

# Установим русскую локаль для красивого форматирования чисел
try:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
except locale.Error:
    print("Локаль ru_RU.UTF-8 не найдена, используется стандартная.")

def format_currency(amount: float) -> str:
    """Форматирует число в денежный формат с пробелами и знаком тенге."""
    # locale.format_string не всегда работает как надо, используем f-string
    return f"{int(amount):,} ₸".replace(",", " ")

# ===================================================================
# Генераторы текста для каждого продукта
# ===================================================================

def _generate_for_travel_card(data: dict, benefit: float) -> str:
    name = data['profile']['name']
    transactions = data['transactions_df']
    
    # Ищем конкретные данные для персонализации
    taxi_spending = transactions[transactions['category'] == 'Такси']['amount'].sum()
    taxi_rides = len(transactions[transactions['category'] == 'Такси'])
    
    if taxi_rides > 3:
        # Если есть поездки на такси, делаем акцент на них
        return f"{name}, за последние 3 месяца вы совершили {taxi_rides} поездок на такси на {format_currency(taxi_spending)}. С картой для путешествий вернули бы ≈ {format_currency(benefit)}. Откройте её в приложении. 🚕"
    else:
        # Общий шаблон, если такси не основная категория
        return f"{name}, заметили ваши траты на путешествия. С нашей тревел-картой вы могли бы вернуть {format_currency(benefit)} кешбэком. Хотите оформить?"

def _generate_for_premium_card(data: dict, benefit: float) -> str:
    name = data['profile']['name']
    balance_str = format_currency(data['profile']['avg_monthly_balance_KZT'])
    
    return f"{name}, ваш средний остаток на счёте — {balance_str}. Премиальная карта даст повышенный кешбэк до 4% и бесплатные снятия по всему миру. Ваша выгода могла составить {format_currency(benefit)}. ✨"

def _generate_for_credit_card(data: dict, benefit: float) -> str:
    name = data['profile']['name']
    top_categories = [cat['category'] for cat in data['metrics']['top_categories']]
    
    # Делаем красивый список категорий
    if len(top_categories) >= 3:
        cat_str = f"{top_categories[0]}, {top_categories[1]} и {top_categories[2]}"
    else:
        cat_str = ", ".join(top_categories)
        
    return f"{name}, ваши топ-категории — {cat_str}. Кредитная карта даёт до 10% кешбэка в любимых категориях. С ней вы бы дополнительно получили {format_currency(benefit)}. Оформить карту."

def _generate_for_deposit(data: dict, benefit: float) -> str:
    name = data['profile']['name']
    
    return f"{name}, у вас на счёте остаются свободные средства. Разместите их на сберегательном вкладе и получите доход до {format_currency(benefit)} уже в следующем квартале. Открыть вклад. 💰"


# ===================================================================
# Главная функция-оркестратор
# ===================================================================

def generate_push_notification(product_name: str, full_data: dict, benefit: float) -> str:
    """
    Выбирает нужный шаблон на основе названия продукта и генерирует текст.
    """
    # Словарь-маршрутизатор: сопоставляет название продукта с функцией-генератором
    generators = {
        "Карта для путешествий": _generate_for_travel_card,
        "Премиальная карта": _generate_for_premium_card,
        "Кредитная карта": _generate_for_credit_card,
        "Депозит Сберегательный": _generate_for_deposit,
    }
    
    # Выбираем нужный генератор, если его нет - используем шаблон по умолчанию
    generator_func = generators.get(product_name)
    
    if generator_func:
        return generator_func(full_data, benefit)
    else:
        # Шаблон по умолчанию для продуктов без специального генератора
        return f"{full_data['profile']['name']}, у нас есть выгодное предложение по продукту '{product_name}' с потенциальной выгодой {format_currency(benefit)}. Узнайте подробности в приложении."