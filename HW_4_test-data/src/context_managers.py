from contextlib import contextmanager
import time


@contextmanager
def timer_context(task_name: str = "Operation"):
    """Контекстный менеджер для замера времени выполнения кода"""
    print(f"\n [Timer] Starting {task_name}...")
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"Finished {task_name}. Duration: {end_time - start_time:.4f} seconds")


class FileOpener:
    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file: object | None = None

    def __enter__(self):
        print(f"1. [ENTER] Открываем файл {self.filename}...(mode: {self.mode}")
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file  # Этот объект пойдет в переменную после "as"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"3. [EXIT] Закрываем файл {self.filename} в любом случае!")
        if self.file:
            self.file.close()
            print(f'Закрыли файл {self.filename}')

        if exc_type is not None:
            print(f"Замечена ошибка: {exc_type}. Но файл мы всё равно закрыли!")
            return False
        return True

