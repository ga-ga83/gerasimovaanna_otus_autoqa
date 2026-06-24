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
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print(f"1. [ENTER] Открываем файл {self.filename}...(mode: {self.mode}")
        self.file = open(self.filename, self.mode)
        return self.file  # Этот объект пойдет в переменную после "as"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"3. [EXIT] Закрываем файл {self.filename} в любом случае!")
        self.file.close()

        if exc_type is not None:
            print(f"Замечена ошибка: {exc_type}. Но файл мы всё равно закрыли!")
            return True
        return False


if __name__ == "__main__":
    with timer_context("JSON Processing"):
        time.sleep(2)  # Имитация работы
        print("step two!")
    print("step five!")

    with FileOpener("data/result.json", "w") as f:
        print("2. [WITH] Пишем данные в файл...")
        f.write("")
        f.div()

print('foo')