pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_FULL', defaultValue: 'gerasimovaanna_otus_autoqa-tests:latest', description: 'Docker-образ с тестами')
        string(name: 'SELENOID_URL', defaultValue: 'http://selenoid:4444/wd/hub', description: 'Адрес Selenoid')
        string(name: 'APP_URL', defaultValue: 'http://prestashop:80/', description: 'URL приложения')
        string(name: 'BROWSER_NAME', defaultValue: 'chrome', description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: '128.0', description: 'Версия браузера')
        string(name: 'HEADLESS_FLAG', defaultValue: '--headless', description: 'Флаг headless')
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

        stage('Verify Docker') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    sh "mkdir -p ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"
                    sh "chmod -R 755 ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // Строим образ напрямую через docker build с корректным параметром имени
                sh "docker build -t ${params.IMAGE_FULL} ."
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

                    echo "=== Проверка файлов Allure на агенте ==="
                    sh "ls -R ${ALLURE_DIR}"
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
                    results: [[path: ALLURE_DIR]],
                    commandline: 'Allure 2.29.0'
                ])
            }
        }
    }
}