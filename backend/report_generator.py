import csv
import os
from tqdm import tqdm 
import data_processor
import logic_engine
import notification_generator

def create_recommendation_report(output_filename: str = "recommendations.csv"):
    print("Начало процесса генерации отчета...")

    # Шаг 1: Получить список всех воинов (клиентов) для тренировки.
    all_clients = data_processor.get_all_clients()
    if not all_clients:
        print("Ошибка: Список клиентов пуст. Проверьте источник данных.")
        return

    # Шаг 2: Подготовить поле боя (CSV-файл) и нанести разметку (заголовки).
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # quotechar='"' и quoting=csv.QUOTE_MINIMAL - стандарт для текстов с запятыми.
            writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Заголовки, как того требует устав (ТЗ).
            writer.writerow(['client_code', 'product', 'push_notification'])

            # Шаг 3: Пройти по каждому воину, оценить его и нанести удар.
            # tqdm показывает твой прогресс, не позволяя тебе отвлечься.
            for client_info in tqdm(all_clients, desc="Обработка клиентов"):
                client_code = client_info['client_code']
                
                # Получаем полное досье.
                full_data = data_processor.get_full_client_data(client_code)
                if not full_data:
                    # Пропускаем тех, кто не явился (нет данных).
                    continue

                # Выбираем лучшую технику (продукт).
                best_product, benefit = logic_engine.find_best_product(client_code, full_data)

                # Создаем идеальный удар (пуш-уведомление).
                # Здесь вызывается твой генератор уведомлений.
                push_text = notification_generator.generate_push_notification(
                    best_product,
                    full_data,
                    benefit
                )

                writer.writerow([client_code, best_product, push_text])

        print(f"\nОтчет успешно создан. Результат сохранен в файл: {os.path.abspath(output_filename)}")

    except IOError as e:
        print(f"Критическая ошибка: Не удалось записать файл '{output_filename}'. Причина: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка в процессе генерации отчета: {e}")

# --- Пример использования ---
# Этот блок будет выполнен, только если ты запустишь этот файл напрямую.
if __name__ == '__main__':
    # Вызов функции для создания отчета.
    # Имя файла можно изменить при необходимости.
    create_recommendation_report("client_recommendations.csv")