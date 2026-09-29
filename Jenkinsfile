pipeline {
    agent any  // <-- запускаем на любой доступной ноде

    environment {
        IMAGE_NAME = 'my-python-test-image'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${FULL_IMAGE} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Создаём папки для артефактов, чтобы не было предупреждений
                    sh 'mkdir -p reports screenshots'

                    sh """
                        docker run --rm \\
                          --user testuser \\
                          -v \$(pwd)/reports:/home/testuser/reports \\
                          -v \$(pwd)/screenshots:/home/testuser/screenshots \\
                          ${FULL_IMAGE}
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
                }
                failure {
                    echo 'Тесты упали — проверь логи и скриншоты.'
                }
            }
        }
    }

    post {
        always {
            script {
                sh "docker rmi ${FULL_IMAGE} || true"
            }
        }
    }
}