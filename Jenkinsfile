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

        stage('Install Docker') {
            steps {
                script {
                    sh 'sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common'
                    sh 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -'
                    sh "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\""
                    sh 'sudo apt-get update && sudo apt-get install -y docker-ce'
                }
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
                sh "docker build -t ${IMAGE_FULL} ."
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def pytestArgs = [
                        "HW_8/test_prestashop_all.py",
                        "--base-url=${APP_URL}",
                        "--browser=${BROWSER_NAME}",
                        "--browser-version=${BROWSER_VERSION}",
                        "--selenoid-url=${SELENOID_URL}",
                        "-v",
                        "--alluredir=${ALLURE_DIR}",
                        "--clean-alluredir",
                        "${HEADLESS_FLAG}".trim()
                    ].findAll { it.trim() != '' }.join(' ')

                    echo "=== Запуск тестов из образа: ${IMAGE_FULL} ==="
                    sh """
                        docker run --rm \\
                          --user root \\
                          --network ${NETWORK_NAME} \\
                          -v ${REPORTS_DIR}:/app/reports \\
                          -v ${ALLURE_DIR}:/app/allure-results \\
                          -v ${SCREENSHOTS_DIR}:/app/screenshots \\
                          ${IMAGE_FULL} \\
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

