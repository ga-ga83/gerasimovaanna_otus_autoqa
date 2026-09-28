pipeline {
    agent any

    stages {
        stage('Setup Portable Python') {
            steps {
                // Скачиваем изолированный Python для Linux по прямой ссылке, так как в системе его нет
                sh '''
                echo "=== Скачиваем портативный Python ==="
                curl -fsSL "https://github.com" -o python.tar.gz

                echo "=== Распаковываем Python ==="
                tar -xzvf python.tar.gz
                rm python.tar.gz

                echo "=== Проверяем работу Python ==="
                ./python/bin/python3 --version
                '''
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                // Устанавливаем ваши зависимости Otus AutoQA и запускаем тесты напрямую
                sh '''
                echo "=== Устанавливаем зависимости из requirements.txt ==="
                ./python/bin/python3 -m pip install --no-cache-dir -r requirements.txt

                echo "=== Запускаем тесты Otus AutoQA ==="
                ./python/bin/python3 -m pytest
                '''
            }
        }
    }
}
