pipeline {
    agent any

    environment {
        // Путь к портативному Python после распаковки — фиксируем один раз
        PYTHON_HOME = "${WORKSPACE}/python"
        PATH = "${PYTHON_HOME}/bin:${PATH}"
    }

    stage('Setup Portable Python') {
            steps {
                script {
                    sh '''
                    echo "=== Скачиваем портативный скомпилированный Python 3.10 ==="
                    curl -fsSL "https://github.com" -o python.tar.gz

                    echo "=== Распаковываем Python ==="
                    tar -xzvf python.tar.gz
                    rm python.tar.gz

                    echo "=== Проверяем работу портативного Python ==="
                    ./python/bin/python3 --version
                    '''
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
