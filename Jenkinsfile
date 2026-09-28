pipeline {
    agent any

    environment {
        PYTHON_HOME = "${WORKSPACE}/python"
        PATH = "${PYTHON_HOME}/bin:${PATH}"
    }

    stages {
        stage('Setup Portable Python') {
            steps {
                sh '''
                set -e

                # Если Python уже на месте — пропускаем скачивание
                if [ -x "${PYTHON_HOME}/bin/python3" ]; then
                    echo "=== Портативный Python уже установлен ==="
                    "${PYTHON_HOME}/bin/python3" --version
                    exit 0
                fi

                echo "=== Скачиваем портативный Python 3.10.14 ==="
                curl -fsSL \
                  "https://github.com/indygreg/python-build-standalone/releases/download/20240415/cpython-3.10.14+20240415-x86_64-unknown-linux-gnu-install_only.tar.gz" \
                  -o python.tar.gz

                echo "=== Распаковываем Python ==="
                mkdir -p "${PYTHON_HOME}"
                tar -xzf python.tar.gz -C "${WORKSPACE}"
                rm python.tar.gz

                echo "=== Проверяем работу Python ==="
                "${PYTHON_HOME}/bin/python3" --version
                '''
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                sh '''
                set -e

                echo "=== Устанавливаем зависимости из requirements.txt ==="
                "${PYTHON_HOME}/bin/python3" -m pip install --no-cache-dir -r requirements.txt

                echo "=== Запускаем тесты Otus AutoQA ==="
                "${PYTHON_HOME}/bin/python3" -m pytest
                '''
            }
        }
    }
}