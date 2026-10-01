pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_FULL',      defaultValue: 'gerasimovaanna_otus_autoqa-tests:latest', description: 'Готовый Docker-образ с тестами')
        string(name: 'SELENOID_URL',     defaultValue: 'http://selenoid:4444/wd/hub', description: 'Адрес Selenoid')
        string(name: 'APP_URL',          defaultValue: 'http://prestashop:80/', description: 'Адрес приложения')
        string(name: 'BROWSER_NAME',     defaultValue: 'chrome', description: 'Имя браузера')
        string(name: 'BROWSER_VERSION',  defaultValue: '128.0', description: 'Версия браузера')
        string(name: 'THREADS_COUNT',    defaultValue: '1', description: 'Количество потоков')
        string(name: 'HEADLESS_FLAG',    defaultValue: '--headless', description: 'Флаг headless')
    }

    environment {
        NETWORK_NAME    = 'prestashop_network'
        REPORTS_DIR     = "${WORKSPACE}/reports"
        ALLURE_DIR      = "${WORKSPACE}/allure-results"
        SCREENSHOTS_DIR = "${WORKSPACE}/screenshots"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    // Создаём директории для артефактов
                    sh "mkdir -p ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"
                    sh "chmod -R 777 ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"

                    // Проверяем наличие сети
                    def networkExists = sh(
                        script: "docker network ls --format '{{.Name}}' | grep -q '^${NETWORK_NAME}\$'",
                        returnStatus: true
                    ) == 0
                    if (!networkExists) {
                        error "Сеть ${NETWORK_NAME} не найдена! Запустите docker-compose up."
                    }

                    // Проверяем и настраиваем PrestaShop
                    sh '''
                        echo "=== Настройка PrestaShop ==="
                        if docker ps -q -f name=prestashop | grep -q .; then
                            docker exec prestashop sed -i "s/define('_PS_MODE_DEV_', true)/define('_PS_MODE_DEV_', false)/" /var/www/html/config/defines.inc.php 2>/dev/null || true
                            docker exec prestashop rm -rf /var/www/html/var/cache/* 2>/dev/null || true
                            echo "PrestaShop настроен."
                        else
                            echo "ВНИМАНИЕ: Контейнер prestashop не найден!"
                        fi
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
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
                        docker run --rm \
                          --user root \
                          --network ${NETWORK_NAME} \
                          -v ${REPORTS_DIR}:/app/reports \
                          -v ${ALLURE_DIR}:/app/allure-results \
                          -v ${SCREENSHOTS_DIR}:/app/screenshots \
                          ${params.IMAGE_FULL} \
                          python -m pytest ${pytestArgs}
                    """

                    echo "--- Содержимое папки allure-results ---"
                    sh "ls -la ${ALLURE_DIR}/"

                    def count = sh(
                        script: "find ${ALLURE_DIR} -name '*-result.json' | wc -l",
                        returnStdout: true
                    ).trim()
                    echo "Найдено JSON-файлов результатов: ${count}"

                    if (count.toInteger() == 0) {
                        error "ОШИБКА: allure-results пуст. Проверьте логи выше."
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/**/*',         allowEmptyArchive: true
                    archiveArtifacts artifacts: 'screenshots/**/*',     allowEmptyArchive: true
                    archiveArtifacts artifacts: 'allure-results/**/*',  allowEmptyArchive: true
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