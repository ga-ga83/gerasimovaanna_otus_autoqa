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
        // Путь, куда мы сохраним скачанный докер внутри воркспейса
        DOCKER_BIN_DIR = "${WORKSPACE}/docker-cli-bin"
    }

    stages {
        stage('Initialize Docker CLI') {
            steps {
                script {
                    // Создаем папку и скачиваем официальный Linux-клиент в формате ZIP
                    sh "mkdir -p ${DOCKER_BIN_DIR}"
                    echo "=== Скачивание стабильного Linux Docker CLI ==="
                    sh "curl -fsSL https://docker.com -o ${WORKSPACE}/docker.zip"

                    echo "=== Распаковка бинарника ==="
                    sh "unzip -o ${WORKSPACE}/docker.zip -d ${WORKSPACE}/tmp_extract"
                    sh "mv ${WORKSPACE}/tmp_extract/docker/docker ${DOCKER_BIN_DIR}/docker"
                    sh "chmod +x ${DOCKER_BIN_DIR}/docker"

                    // Очищаем временные файлы
                    sh "rm -rf ${WORKSPACE}/docker.zip ${WORKSPACE}/tmp_extract"
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker') {
            steps {
                // Добавляем нашу папку с бинарником в PATH текущего шага
                withEnv(["PATH+DOCKER=${DOCKER_BIN_DIR}"]) {
                    sh 'docker --version'
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
                withEnv(["PATH+DOCKER=${DOCKER_BIN_DIR}"]) {
                    sh "docker build -t ${IMAGE_FULL} ."
                }
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
                    withEnv(["PATH+DOCKER=${DOCKER_BIN_DIR}"]) {
                        sh """
                            docker run --rm \
                              --user root \
                              --network ${NETWORK_NAME} \
                              -v ${REPORTS_DIR}:/app/reports \
                              -v ${ALLURE_DIR}:/app/allure-results \
                              -v ${SCREENSHOTS_DIR}:/app/screenshots \
                              ${IMAGE_FULL} \
                              python -m pytest ${pytestArgs}
                        """
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
