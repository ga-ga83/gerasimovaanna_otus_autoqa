import csv
import json
from importlib.metadata import distribution

from context_managers import timer_context, FileOpener


def distribute_books():
    books_file = 'books.csv'
    users_file = 'users.json'
    result_file = 'result.json'

    #Читаем список книг
    with open(books_file, mode='r', encoding='utf-8') as f:
        books = list(csv.DictReader(f))

    #Читаем список пользователей
    with FileOpener(users_file, 'r') as f:
        users = json.load(f)


    list_books = len(books)
    list_users = len(users)

    if list_users == 0:
        print(f'Error: the list of users is empty')
        return []

    base_share = list_books // list_users
    remainder_users = list_books % list_users

    result_data = []

    for i, user in enumerate(users):
        start_idx = i * base_share + min(i, remainder_users)
        end_idx = start_idx + base_share + (1 if i < remainder_users else 0)

        user_data = user.copy()
        user_data['books'] = books [start_idx:end_idx]
        result_data.append(user_data)
    #write result of json
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)

    print(f'\n[Success] Файл {result_file} успешно создан.')
    return result_data

if __name__ == "__main__":
    #Запуск скрипта внутри таймера
    with timer_context('Books Distribution'):
        distribute_books()
    print(f'\n[End] скрипт завершил работу.')

