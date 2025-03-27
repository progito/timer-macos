import time
import os
import json
from datetime import datetime


def show_notification(title, message):
    applescript = f'display notification "{message}" with title "{title}" sound name "Glass"'
    os.system(f"osascript -e '{applescript}'")

def load_schedule(file_path="schedule.json"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Создайте его с нужным расписанием.")
        return {}
    except json.JSONDecodeError:
        print("Ошибка в формате JSON.")
        return {}


def pomodoro_timer():

    schedule = load_schedule()

    work_time = 45 * 60  
    break_time = 15 * 60  
    
    while True:
        current_time = datetime.now().strftime("%H:%M")  

        if current_time in schedule:
            event = schedule[current_time]
            description = event["описание"]
            timeout = event["таймаут"] * 60 
            print(f"Событие: {description} на {timeout // 60} минут")
            show_notification("Событие!", description)
            time.sleep(timeout)
            show_notification("Конец события!", f"{description} завершено.")
        else:
            print("Работаем 45 минут...")
            time.sleep(work_time)
            show_notification("Конец работы!", "45 минут прошло. Время 15-минутного перерыва!")
            
            print("Перерыв 15 минут...")
            time.sleep(break_time)
            show_notification("Конец перерыва!", "15 минут прошло. Пора возвращаться к работе!")

if __name__ == "__main__":
    print("Запускаем таймер с расписанием...")
    try:
        pomodoro_timer()
    except KeyboardInterrupt:
        print("\nТаймер остановлен пользователем.")
