import time


def handle_db_errors(func):
    """Handle common database errors."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as error:
            print(f"Ошибка: Таблица или столбец {error} не найден.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")

        return None

    return wrapper


def confirm_action(action_name):
    """Request confirmation before a dangerous operation."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )

            if answer.lower() != "y":
                print("Операция отменена.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Measure and print function execution time."""

    def wrapper(*args, **kwargs):
        start_time = time.monotonic()

        result = func(*args, **kwargs)

        elapsed_time = time.monotonic() - start_time

        print(
            f"Функция {func.__name__} выполнилась "
            f"за {elapsed_time:.3f} секунд"
        )

        return result

    return wrapper


def create_cacher():
    """Create a closure for caching function results."""
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result

        return result

    return cache_result