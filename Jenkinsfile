pipeline {
    agent any

    stages {
        stage('Setup Portable Python') {
            steps {
                sh '''
                echo "=== Скачиваем портативный Python 3.10.14 ==="
                curl -fsSL "https://github.com/indygreg/python-build-standalone/releases/download/20240415/cpython-3.10.14+20240415-x86_64-unknown-linux-gnu-install_only.tar.gz" -o python.tar.gz

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