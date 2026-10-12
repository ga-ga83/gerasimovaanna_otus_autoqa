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

        // Если образ уже собран локально и ты просто тестируешь пайплайн,
        // эту стадию можно убрать. Если нужно собирать каждый раз — оставь.
        stage('Build Docker Image') {
            steps {
                echo "=== Сборка Docker-образа ==="
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
                        "${params.HEADLESS_FLAG}".trim()
                    ].findAll { it.trim() != '' }.join(' ')

                    echo "=== Запуск тестов из образа: ${params.IMAGE_FULL} ==="

                    try {
                        sh """
                            docker run --rm \\
                                --network ${NETWORK_NAME} \\
                                -v ${REPORTS_DIR}:/app/reports \\
                                -v ${ALLURE_DIR}:/app/allure-results \\
                                -v ${SCREENSHOTS_DIR}:/app/screenshots \\
                                ${params.IMAGE_FULL} \\
                                python -m pytest ${pytestArgs}
                        """
                    } catch (Exception e) {
                        echo "Тесты завершились с ошибками: ${e.message}"
                        currentBuild.result = 'FAILURE'
                    } finally {
                        echo "=== Проверка файлов Allure на агенте ==="
                        sh "ls -lhR ${ALLURE_DIR}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo "=== Генерация Allure отчета ==="
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
        failure {
            echo "Пайплайн упал. Проверь логи и права на папки."
        }
    }
}
