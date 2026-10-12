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

        stage('Verify & Prepare Workspace') {
            steps {
                sh 'docker --version'
                echo "=== Подготовка директорий ==="
                sh '''
                    mkdir -p "${REPORTS_DIR}" "${ALLURE_DIR}" "${SCREENSHOTS_DIR}"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "=== Сборка Docker-образа ==="
                sh """
                    docker build \
                        --build-arg UID=\$(id -u) \
                        --build-arg GID=\$(id -g) \
                        -t ${params.IMAGE_FULL} .
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def pytestArgsList = [
                        "HW_8/test_prestashop_all.py",  // Проверь, что этот путь верный в репозитории!
                        "--base-url=${params.APP_URL}",
                        "--browser=${params.BROWSER_NAME}",
                        "--browser-version=${params.BROWSER_VERSION}",
                        "--selenoid-url=${params.SELENOID_URL}",
                        "-v",
                        "--alluredir=/app/allure-results",
                        "${params.HEADLESS_FLAG}".trim()
                    ]

                    def pytestArgs = pytestArgsList.findAll { it.trim() != '' }.join(' ')
                    echo "[DEBUG] Запуск: python -m pytest ${pytestArgs}"

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
                        echo "❌ Тесты упали: ${e.message}"
                        currentBuild.result = 'FAILURE'
                    } finally {
                        echo "=== Содержимое папки allure-results ==="
                        sh "ls -lhR ${ALLURE_DIR} || echo 'Папка пуста'"
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
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']],
                    commandline: 'Allure 2.29.0'  // Имя инструмента из Global Tool Configuration
                ])

                def reportDir = "${WORKSPACE}/allure-report"
                if (fileExists("${reportDir}/index.html")) {
                    echo "✅ Allure Report готов: ${reportDir}/index.html"
                } else {
                    error "❌ Ошибка генерации отчета: index.html не найден. Проверь логи Allure CLI."
                }
            }
            archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
        }
        failure {
            echo "Пайплайн завершился с ошибкой."
        }
        cleanup {
            echo "Очистка завершена."
        }
    }
}