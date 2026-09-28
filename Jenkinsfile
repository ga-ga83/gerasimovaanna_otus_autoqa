pipeline {
    agent any

    environment {
        IMAGE_NAME = 'otus-autoqa-tests'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh '''
                set -e
                echo "=== Собираем Docker-образ ==="
                docker build -t "${IMAGE_NAME}" .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                set -e
                echo "=== Запускаем тесты из HW_8 ==="
                docker run --rm \
                  -v "${WORKSPACE}/HW_8:/app/HW_8" \
                  -w /app \
                  "${IMAGE_NAME}" \
                  pytest HW_8/ -v
                '''
            }
        }
    }

    post {
        always {
            echo "=== Сборка завершена, статус: ${currentBuild.result ?: 'SUCCESS'} ==="
        }
        cleanup {
            sh 'docker rmi "${IMAGE_NAME}" 2>/dev/null || true'
        }
    }
}