def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="URL, который будет проверяться",
    )
    parser.addoption(
        "--status_code",
        action="store",
        type=int,
        default=200,
        help="Ожидаемый HTTP статус-код",
    )
