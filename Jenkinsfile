pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_FULL', defaultValue: 'my-python-test-image:latest', description: 'Готовый Docker-образ с тестами')
        // остальные параметры...
        string(name: 'SELENOID_URL', defaultValue: 'http://selenoid:4444/wd/hub')
        string(name: 'APP_URL', defaultValue: 'http://prestashop:80/')
        string(name: 'BROWSER_NAME', defaultValue: 'chrome')
        string(name: 'BROWSER_VERSION', defaultValue: '128.0')
        string(name: 'THREADS_COUNT', defaultValue: '1')
        string(name: 'HEADLESS_FLAG', defaultValue: '--headless')
    }

    environment {
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

        // Build Docker Image — УДАЛЕНО

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
                    // Проверка PrestaShop (как у тебя)
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

                    echo "=== Запуск тестов из образа: ${params.IMAGE_FULL} ==="
                    sh """
                        docker run --rm \\
                          --user root \\
                          --network ${NETWORK_NAME} \\
                          -v ${REPORTS_DIR}:/app/reports \\
                          -v ${ALLURE_DIR}:/app/allure-results \\
                          -v ${SCREENSHOTS_DIR}:/app/screenshots \\
                          ${params.IMAGE_FULL} \\
                          python -m pytest ${pytestArgs}
                    """

                    echo "--- Содержимое папки allure-results ---"
                    sh "ls -la ${ALLURE_DIR}/"

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
                // Не пытаемся удалить образ, если он внешний
                echo "Образ ${params.IMAGE_FULL} не удаляется (внешний)."

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