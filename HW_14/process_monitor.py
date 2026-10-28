import subprocess
import csv
from io import StringIO
from datetime import datetime


def get_process_data():
    """
    Для Windows: использует tasklist /FO CSV, парсит CSV и возвращает список словарей.
    Поля: Image Name, PID, Session Name, Session#, Mem Usage
    """
    try:
        # tasklist с выводом в CSV — удобно и надёжно парсить
        result = subprocess.run(
            ["tasklist", "/FO", "CSV"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения tasklist: {e}")
        return []
    except FileNotFoundError:
        print("Не найдена команда tasklist. Это стандартная утилита Windows.")
        return []

    # Парсим CSV через встроенный csv-модуль
    reader = csv.DictReader(StringIO(result.stdout))
    processes = []
    for row in reader:
        # Очищаем кавычки, если они остались
        cleaned_row = {k.strip('"'): v.strip('"') for k, v in row.items()}
        processes.append(cleaned_row)

    return processes


def analyze_processes(processes):
    """
    Анализирует список процессов (Windows tasklist) и возвращает статистику.
    tasklist не даёт % CPU, поэтому total_cpu = 0.
    Память в tasklist — в КБ.
    """
    if not processes:
        return None

    # Пользователи: в Windows это 'User Name'
    users = sorted(set(p.get('User Name', 'unknown') for p in processes))
    total_processes = len(processes)

    user_counts = {}
    for p in processes:
        user = p.get('User Name', 'unknown')
        user_counts[user] = user_counts.get(user, 0) + 1

    # Суммируем память в КБ (tasklist даёт Mem Usage в формате "12 345 K")
    def parse_mem_kb(mem_str):
        if not mem_str:
            return 0
        # Удаляем пробелы и ' K', если есть
        val = mem_str.replace(',', '').replace(' ', '').replace('K', '')
        try:
            return int(val)
        except ValueError:
            return 0

    total_mem_kb = sum(parse_mem_kb(p.get('Mem Usage', '0')) for p in processes)

    # CPU в tasklist нет → total_cpu условно 0
    total_cpu = 0.0

    # Процесс с максимальной памятью
    max_mem_proc = max(
        processes,
        key=lambda p: parse_mem_kb(p.get('Mem Usage', '0')),
        default=None
    )
    max_mem_display = "unknown"
    if max_mem_proc:
        mem_kb = parse_mem_kb(max_mem_proc.get('Mem Usage', '0'))
        name = max_mem_proc.get('Image Name', 'unknown').split('.')[0]
        max_mem_display = f"{mem_kb:,} KB {name[:20]}"

    # Про CPU сказать нечего — tasklist не показывает % CPU
    max_cpu_display = "N/A (tasklist не показывает % CPU)"

    return {
        'users': users,
        'total_processes': total_processes,
        'user_counts': user_counts,
        'total_cpu': total_cpu,
        'total_mem': total_mem_kb,
        'max_mem': max_mem_display,
        'max_cpu': max_cpu_display
    }


def format_report(stats):
    """
    Форматирует статистику в строку отчёта.
    """
    report_lines = [
        "Отчёт о состоянии системы (Windows):",
        f"Пользователи системы: {', '.join(repr(u) for u in stats['users'])}",
        f"Процессов запущено: {stats['total_processes']}",
        "",
        "Количество процессов по пользователям:"
    ]

    for user in sorted(stats['user_counts'].keys()):
        count = stats['user_counts'][user]
        report_lines.append(f"{user}: {count}")

    report_lines.extend([
        "",
        f"Всего памяти используется: {stats['total_mem']:,} KB",
        f"Всего CPU используется: {stats['total_cpu']:.1f}% (недоступно в tasklist)",
        f"Больше всего памяти использует: {stats['max_mem']}",
        f"Больше всего CPU использует: {stats['max_cpu']}"
    ])

    return '\n'.join(report_lines)


def save_report_to_file(report_text):
    """
    Сохраняет отчёт в файл с именем в формате ДД-ММ-ГГГГ-ЧЧ:ММ-scan.txt
    """
    now = datetime.now()
    filename = now.strftime("%d-%m-%Y-%H:%M") + "-scan.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\nОтчёт сохранён в файл: {filename}")
    except IOError as e:
        print(f"Ошибка записи файла: {e}")


def main():
    print("Сбор данных о процессах (tasklist)...")
    processes = get_process_data()

    if not processes:
        print("Не удалось получить данные о процессах.")
        return

    stats = analyze_processes(processes)
    if stats is None:
        print("Ошибка анализа данных.")
        return

    report = format_report(stats)

    # Вывод в стандартный поток вывода
    print("\n" + report)

    # Сохранение в файл
    save_report_to_file(report)


if __name__ == "__main__":
    main()
