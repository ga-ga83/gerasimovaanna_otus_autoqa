pipeline {
    agent none // Отключаем глобальный агент, чтобы сначала сделать checkout

    stages {
        stage('Checkout') {
            agent any // Используем любой доступный узел Jenkins для скачивания кода
            steps {
                checkout scm // Скачиваем ваш репозиторий с Dockerfile
            }
        }

        stage('Run tests') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir '.'
                    args '--user root'
                }
            }
            steps {
                // Теперь Dockerfile на месте, образ соберется, и запустятся тесты
                sh 'pytest -v'
            }
        }
    }
}
