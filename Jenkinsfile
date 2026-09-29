pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-python-test-image'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        NETWORK_NAME = 'prestashop_network'
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

                    // Проверяем, что сеть существует
                    def networkExists = sh(script: "docker network ls --format '{{.Name}}' | grep -q '^${NETWORK_NAME}\$'", returnStatus: true) == 0
                    if (!networkExists) {
                        error "Сеть ${NETWORK_NAME} не найдена! Сначала запуши PrestaShop через docker compose."
                    }

                    // Отключаем debug mode в PrestaShop, чтобы убрать Symfony Web Debug Toolbar
                    // (он перекрывает кнопки админки → ElementClickInterceptedException)
                    // и ускорить загрузку страниц (→ TimeoutException)
                    sh '''
                        docker exec prestashop sed -i "s/define('_PS_MODE_DEV_', true)/define('_PS_MODE_DEV_', false)/" /var/www/html/config/defines.inc.php || true
                        docker exec prestashop rm -rf /var/www/html/var/cache/* || true
                        echo "PrestaShop debug mode disabled, cache cleared"
                    '''

                    // Запускаем тесты
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

