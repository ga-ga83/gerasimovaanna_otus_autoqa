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
                    sh "mkdir -p ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"

                    sh "chmod -R 777 ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"

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

                    // ДИАГНОСТИКА: Проверяем pytest.ini и запускаем простой тест с allure
                    echo "=== ДИАГНОСТИКА: Проверка pytest.ini ==="
                    sh """
                        docker run --rm --user root \\
                          --network ${NETWORK_NAME} \\
                          -v ${ALLURE_DIR}:/app/allure-results \\
                          ${FULL_IMAGE} \\
                          bash -c '
                            echo "--- pytest.ini ---";
                            cat /app/pytest.ini 2>/dev/null || echo "pytest.ini не найден";
                            echo "";
                            echo "--- Простой тест allure ---";
                            mkdir -p /app/allure-results;
                            echo "def test_dummy(): assert True" > /tmp/test_dummy.py;
                            python -m pytest /tmp/test_dummy.py -v --alluredir=/app/allure-results --clean-alluredir;
                            echo "--- Файлы после простого теста ---";
                            ls -la /app/allure-results/;
                          '
                    """

                    def pytestArgs = [
                        "HW_8/test_prestashop_all.py",
                        "--base-url=${params.APP_URL}",
                        "--browser=${params.BROWSER_NAME}",
                        "--browser-version=${params.BROWSER_VERSION}",
                        "--selenoid-url=${params.SELENOID_URL}",
                        "-v",
                        "--alluredir=/app/allure-results",
                        "--clean-alluredir",
                        "${params.HEADLESS_FLAG}".trim()
                    ].findAll { it.trim() != '' }.join(' ')

                    echo "=== ПОЛНЫЙ ЗАПУСК тестов ==="
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

                    echo "--- Содержимое папки allure-results ---"
                    sh "ls -la ${ALLURE_DIR}/"

                    echo "--- Количество файлов результатов (*-result.json) ---"
                    def count = sh(script: "find ${ALLURE_DIR} -name '*-result.json' | wc -l", returnStdout: true).trim()
                    echo "Найдено JSON-файлов результатов: ${count}"

                    if (count.toInteger() == 0) {
                        error "ОШИБКА: allure-results пуст. Смотри логи диагностики выше."
                    }
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
                    commandline: 'Allure 2.29.0'
                ])
            }
        }
    }
}
