import time
from functools import wraps

import prompt


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: файл базы данных не найден.")
        except KeyError as error:
            print(f"Ошибка: таблица или столбец {error} не найден.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")

        return None

    return wrapper

def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = prompt.string(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )

            if answer.lower() != "y":
                print("Операция отменена.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()

        result = func(*args, **kwargs)

        elapsed_time = time.monotonic() - start_time

        print(
            f"Функция {func.__name__} выполнилась "
            f"за {elapsed_time:.3f} секунд."
        )

        return result

    return wrapper