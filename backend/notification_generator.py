import os
import random
import google.generativeai as genai
from dotenv import load_dotenv
import locale
from typing import Dict, Any

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY не найден в файле .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
except locale.Error:
    print("Не удалось установить русскую локаль ru_RU.UTF-8.")

def format_currency(amount: float) -> str:
    """Форматирует число как валюту с пробелами и знаком тенге."""
    return f"{int(amount):,} ₸".replace(",", " ")

def _create_hook(product_name: str, data: Dict[str, Any]) -> str:
    # ... (логика этой функции остается прежней) ...
    profile = data['profile']
    metrics = data['metrics']
    transactions = data['transactions_df']

    if product_name in ["Кредитная карта", "Премиальная карта"]:
        if metrics.get("top_categories"):
            top_cats_list = [cat['category'] for cat in metrics['top_categories'][:3]]
            if top_cats_list:
                return f"Ваши самые частые категории трат за последние 3 месяца: {', '.join(top_cats_list)}."

    if product_name == "Карта для путешествий":
        travel_spending = transactions[transactions['category'].isin(['Путешествия', 'Такси', 'Отели'])]['amount'].sum()
        if travel_spending > 5000:
            return f"За последние 3 месяца ваши расходы на такси, отели и путешествия составили {format_currency(travel_spending)}."

    if "Депозит" in product_name or product_name == "Инвестиции":
        balance = profile.get('avg_monthly_balance_KZT', 0)
        if balance > 100000:
            return f"Мы видим, что у вас на счете регулярно остаются свободные средства в размере около {format_currency(balance)}."
            
    if product_name == "Подтверждение выгоды":
        try:
            current_card_name = transactions['product'].mode()[0]
            return f"Вы активно и выгодно пользуетесь вашей картой «{current_card_name}»."
        except (KeyError, IndexError):
            return "Вы активно пользуетесь нашими услугами."

    total_spending = metrics.get('total_spending_3m', 0)
    if total_spending > 0:
        return f"За последние 3 месяца вы потратили {format_currency(total_spending)}."
        
    return "Мы проанализировали ваши финансы."

def _generate_fallback_notification(product_name: str, data: Dict[str, Any], benefit: float) -> str:
    """
    ИЗМЕНЕНИЕ: Шаблоны переработаны для демонстрации конкретной выгоды в цифрах.
    """
    name = data['profile'].get('name', 'Клиент')
    top_cats_list = [cat['category'] for cat in data['metrics'].get('top_categories', [])[:3]]
    top_cats_str = ", ".join(top_cats_list)

    templates = {
        "Карта для путешествий": [
            f"{name}, ваши поездки могут быть еще выгоднее. С тревел-картой вы могли бы вернуть {format_currency(benefit)} за последние 3 месяца. ✈️ Хотите оформить?",
            f"{name}, заметили ваши траты на такси и отели. Превратите их в выгоду! С нашей картой для путешествий вы бы сэкономили {format_currency(benefit)}. Узнайте больше.",
            f"Путешествовать — здорово, а с кешбэком — еще лучше! {name}, ваша выгода с картой для путешествий могла составить {format_currency(benefit)}. Откройте ее в приложении."
        ],
        "Премиальная карта": [
            f"{name}, с вашим стилем трат премиальная карта могла бы принести {format_currency(benefit)} за 3 месяца. Наслаждайтесь повышенным кешбэком и привилегиями! ✨ Оформить сейчас.",
            f"Заметили ваши траты в ресторанах. {name}, с премиальной картой вы бы получили не только повышенный кешбэк, но и выгоду в {format_currency(benefit)}. Подключить сейчас.",
            f"{name}, ваш статус позволяет получать больше. Премиальная карта — это не только комфорт, но и прямая выгода, которая могла составить {format_currency(benefit)}. Попробуйте."
        ],
        "Кредитная карта": [
            f"{name}, ваши топ-категории — {top_cats_str}. С кредитной картой вы бы получили до 10% кешбэка, а ваша выгода составила бы {format_currency(benefit)}. 💳 Оформить карту.",
            f"{name}, ваша выгода с нашей кредитной картой могла составить {format_currency(benefit)} за 3 месяца благодаря кешбэку в любимых категориях. Узнайте ваш кредитный лимит.",
            f"Покупайте то, что любите, и экономьте! {name}, с нашей кредитной картой вы бы вернули {format_currency(benefit)} с ваших обычных покупок. Начать экономить."
        ],
        "Депозит Сберегательный": [
            f"{name}, ваш остаток на счете может приносить реальный доход. Разместите его на сберегательном вкладе и получите до {format_currency(benefit)} годовых. 📈 Открыть.",
            f"Заставьте ваши деньги работать! {name}, ваш капитал мог бы принести {format_currency(benefit)} пассивного дохода в год на сберегательном депозите. Начать копить."
        ],
        # Для продуктов без прямой "упущенной выгоды" сохраняем фокус на пользе
        "Инвестиции": [
            f"{name}, попробуйте инвестиции с низким порогом входа и без комиссий на старте. Это проще, чем кажется. Начните с любой суммы! 🚀 Открыть счёт.",
            f"{name}, ваш стабильный доход позволяет задуматься о будущем. Откройте для себя мир инвестиций и заставьте капитал работать. Узнайте больше."
        ],
        "Кредит наличными": [
            f"{name}, если нужен запас на крупные траты — можно оформить кредит наличными с гибкими выплатами. Узнайте доступный лимит прямо в приложении.",
            f"{name}, планируете большое событие или покупку? Кредит наличными поможет реализовать ваши планы без лишних справок и ожиданий. Рассчитать условия."
        ]
        # ... и так далее для остальных продуктов
    }
    
    product_templates = templates.get(product_name)
    if product_templates:
        return random.choice(product_templates)
    else:
        # Резервная заглушка, если выгода равна нулю или шаблон не найден
        if benefit > 0:
            return f"{name}, у нас есть для вас предложение по продукту «{product_name}» с выгодой до {format_currency(benefit)}. Узнайте подробности в приложении. 😊"
        else:
            return f"{name}, у нас есть интересное предложение по продукту «{product_name}». Узнайте больше в приложении. 😉"

def generate_push_notification(product_name: str, full_data: Dict[str, Any], benefit: float) -> str:
    try:
        # ... (основная логика вызова Gemini) ...
        profile = full_data['profile']
        hook = _create_hook(product_name, full_data)
        
        task = "" # Логика постановки задачи для Gemini
        if product_name == "Инвестиции":
            task = "..."
        # ... и так далее
        
        prompt = f"""...""" # Промпт для Gemini
        
        response = model.generate_content(prompt)
        if not response.text or response.text.isspace():
             raise ValueError("API вернул пустой ответ.")
        return response.text.strip().replace('"', '').replace('*', '')
    except Exception as e:
        print(f"!!! ОШИБКА GEMINI API: {e}. Активирован резервный генератор уведомлений.")
        return _generate_fallback_notification(product_name, full_data, benefit)