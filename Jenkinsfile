pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-python-test-image'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        NETWORK_NAME = 'prestashop-net'
        PRESTASHOP_CONTAINER = 'prestashop'
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
                    sh 'mkdir -p reports screenshots'

                    // Создаём сеть (если уже есть — не ошибка)
                    sh "docker network create ${NETWORK_NAME} 2>/dev/null || true"

                    // Запускаем PrestaShop в этой сети
                    // Имя контейнера = prestashop, чтобы тесты могли обращаться по имени хоста
                    sh """
                        docker run -d --rm \\
                          --name ${PRESTASHOP_CONTAINER} \\
                          --network ${NETWORK_NAME} \\
                          -e DB_SERVER=db \\
                          -e DB_USER=prestashop \\
                          -e DB_PASSWD=prestashop \\
                          -e DB_NAME=prestashop \\
                          prestashop/prestashop:latest
                    """

                    // Ждём, пока PrestaShop поднимется (может потребоваться 30-60 секунд)
                    sh """
                        echo 'Waiting for PrestaShop to start...'
                        for i in \$(seq 1 60); do
                            if docker exec ${PRESTASHOP_CONTAINER} curl -sf http://localhost:80/ > /dev/null 2>&1; then
                                echo 'PrestaShop is up!'
                                break
                            fi
                            echo "Attempt \$i: PrestaShop not ready yet..."
                            sleep 5
                        done
                    """

                    // Запускаем тесты в той же сети
                    sh """
                        docker run --rm \\
                          --user testuser \\
                          --network ${NETWORK_NAME} \\
                          -v \$(pwd)/reports:/home/testuser/reports \\
                          -v \$(pwd)/screenshots:/home/testuser/screenshots \\
                          ${FULL_IMAGE}
                    """
                }
            }
            post {
                always {
                    // Останавливаем PrestaShop
                    sh "docker stop ${PRESTASHOP_CONTAINER} 2>/dev/null || true"

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
                sh "docker network rm ${NETWORK_NAME} 2>/dev/null || true"
            }
        }
    }
}