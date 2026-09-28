pipeline {
    agent any

    stages {
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
                script {
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
}
