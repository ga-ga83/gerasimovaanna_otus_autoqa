pipeline {
    agent any

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://selenoid:4444/wd/hub', description: 'Адрес Executor')
        string(name: 'APP_URL', defaultValue: 'http://prestashop:80/', description: 'Адрес приложения')
        string(name: 'BROWSER_NAME', defaultValue: 'chrome', description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: '128.0', description: 'Версия браузера')
        string(name: 'THREADS_COUNT', defaultValue: '1', description: 'Количество потоков')
        string(name: 'HEADLESS_FLAG', defaultValue: '--headless', description: 'Флаг headless')
    }

    environment {
        IMAGE_NAME = 'my-python-test-image'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        NETWORK_NAME = 'prestashop_network'

        REPORTS_DIR = "${WORKSPACE}/reports"
        ALLURE_DIR = "${WORKSPACE}/allure-results"
        SCREENSHOTS_DIR = "${WORKSPACE}/screenshots"
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

        stage('Prepare Environment') {
            steps {
                script {
                    sh "rm -rf ${ALLURE_DIR}/*"
                    sh "mkdir -p ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"
                    sh "chmod -R 777 ${ALLURE_DIR}"

                    def networkExists = sh(script: "docker network ls --format '{{.Name}}' | grep -q '^${NETWORK_NAME}\$'", returnStatus: true) == 0
                    if (!networkExists) {
                        error "Сеть ${NETWORK_NAME} не найдена! Запустите docker-compose up."
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh "chmod -R 777 ${ALLURE_DIR}"

                    sh '''
                        echo "=== Настройка PrestaShop ==="
                        if docker ps -q -f name=prestashop | grep -q .; then
                            docker exec prestashop sed -i "s/define('_PS_MODE_DEV_', true)/define('_PS_MODE_DEV_', false)/" /var/www/html/config/defines.inc.php 2>/dev/null || true
                            docker exec prestashop rm -rf /var/www/html/var/cache/* 2>/dev/null || true
                            echo "PrestaShop configured."
                        else
                            echo "Warning: PrestaShop container not found."
                        fi
                    '''

                    def threads = params.THREADS_COUNT.toInteger()

                    def pytestArgs = [
                        "HW_8/test_prestashop_all.py",
                        "--base-url=${params.APP_URL}",
                        "--browser=${params.BROWSER_NAME}",
                        "--browser-version=${params.BROWSER_VERSION}",
                        "--selenoid-url=${params.SELENOID_URL}",
                        "-v",
                        "--alluredir=/app/allure-results",
                        "${params.HEADLESS_FLAG}".trim()
                    ].findAll { it.trim() != '' }.join(' ')

                    sh """
                        docker run --rm \\
                          --user root \\
                          --network ${NETWORK_NAME} \\
                          -v ${REPORTS_DIR}:/app/reports \\
                          -v ${ALLURE_DIR}:/app/allure-results \\
                          -v ${SCREENSHOTS_DIR}:/app/screenshots \\
                          ${FULL_IMAGE} \\
                          python -m pytest ${pytestArgs}
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
                }
                failure {
                    echo 'Тесты упали.'
                }
            }
        }
    }

    post {
        always {
            script {
                sh "docker rmi ${FULL_IMAGE} || true"

                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']],
                    commandline: '3.16.0'
                ])
            }
        }
    }
}