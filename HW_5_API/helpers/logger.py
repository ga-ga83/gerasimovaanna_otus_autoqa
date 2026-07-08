import logging


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # не добавляем дублирование обработчиков, если логгер уже сконфигурирован
    if logger.handlers:
        return logger

    # создаем обработчик для вывода логов в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # создаем обработчик для записи логов в файл
    log_path = Path(__file__).resolve().parents[2] / 'log.log'
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # форматирование логов
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # добавляем обработчики к логгеру
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = create_logger()

