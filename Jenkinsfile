pipeline {
    agent any

    stages {
        stage('Setup Portable Python') {
            steps {
                sh '''
                set -e

                echo "=== Скачиваем портативный Python 3.10.14 ==="
                curl -fsSL "https://github.com/indygreg/python-build-standalone/releases/download/20240415/cpython-3.10.14+20240415-x86_64-unknown-linux-gnu-install_only.tar.gz" -o python.tar.gz

                echo "=== Распаковываем Python ==="
                tar -xzf python.tar.gz
                rm python.tar.gz

                # Находим папку с Python (обычно это cpython-3.10.14+...)
                PYTHON_DIR=$(find . -maxdepth 1 -type d -name "cpython-*" | head -n1)
                if [ -z "$PYTHON_DIR" ]; then
                    echo "Ошибка: папка с Python не найдена после распаковки"
                    exit 1
                fi
                echo "Используем Python из: $PYTHON_DIR"

                echo "=== Проверяем работу Python ==="
                "$PYTHON_DIR/bin/python3" --version

                # Экспортируем PATH для следующих шагов (опционально, но удобно)
                export PATH="$PYTHON_DIR/bin:$PATH"
                '''
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                sh '''
                set -e

                # Определяем ту же папку с Python повторно (на случай разных шагов)
                PYTHON_DIR=$(find . -maxdepth 1 -type d -name "cpython-*" | head -n1)
                if [ -z "$PYTHON_DIR" ]; then
                    echo "Ошибка: папка с Python не найдена"
                    exit 1
                fi

                echo "=== Устанавливаем зависимости из requirements.txt ==="
                "$PYTHON_DIR/bin/python3" -m pip install --no-cache-dir -r requirements.txt

                echo "=== Запускаем тесты Otus AutoQA ==="
                "$PYTHON_DIR/bin/python3" -m pytest
                '''
            }
        }
    }
}