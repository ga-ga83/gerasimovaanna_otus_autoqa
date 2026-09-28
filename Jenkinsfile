pipeline {
    agent any

    environment {
        // Путь к портативному Python после распаковки — фиксируем один раз
        PYTHON_HOME = "${WORKSPACE}/python"
        PATH = "${PYTHON_HOME}/bin:${PATH}"
    }

    stages {
        stage('Setup Portable Python') {
            steps {
                script {
                    // Выбираем стабильную версию Python (пример: 3.11.10)
                    def pyVersion = '3.11.10'
                    def fileName = "Python-${pyVersion}.tgz"
                    def url = "https://www.python.org/ftp/python/${pyVersion}/${fileName}"

                    sh """
                        echo "=== Скачиваем портативный Python ${pyVersion} ==="
                        curl -fsSL "${url}" -o "${fileName}"

                        echo "=== Распаковываем Python ==="
                        tar -xzvf "${fileName}"
                        rm "${fileName}"

                        # Переименовываем папку, чтобы путь был предсказуемым
                        mv "Python-${pyVersion}" "python"

                        echo "=== Проверяем работу Python ==="
                        "${PYTHON_HOME}/bin/python3" --version
                    """
                }
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                sh """
                    echo "=== Устанавливаем зависимости из requirements.txt ==="
                    "${PYTHON_HOME}/bin/python3" -m pip install --no-cache-dir -r requirements.txt

                    echo "=== Запускаем тесты Otus AutoQA ==="
                    "${PYTHON_HOME}/bin/python3" -m pytest
                """
            }
        }
    }
}