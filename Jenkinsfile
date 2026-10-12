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
                    echo "=== Очистка и подготовка директорий ==="
                    // Удаляем старые папки, чтобы отчеты не дублировались и не наслаивались
                    sh "rm -rf ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"
                    sh "mkdir -p ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"
                    // Выставляем полные права 777, чтобы у Docker-контейнера
                    // не возникло конфликтов прав при записи файлов на хост-машину
                    sh "chmod -R 777 ${REPORTS_DIR} ${ALLURE_DIR} ${SCREENSHOTS_DIR}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
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

                    // Динамически получаем UID и GID текущего пользователя Jenkins.
                    // Это решает проблему, когда тесты падают из-за разницы прав root хоста и контейнера.
                    def uid = sh(script: 'id -u', returnStdout: true).trim()
                    def gid = sh(script: 'id -g', returnStdout: true).trim()

                    try {
                        sh """
                            docker run --rm \
                              --user ${uid}:${gid} \
                              --network ${NETWORK_NAME} \
                              -v ${REPORTS_DIR}:/app/reports \
                              -v ${ALLURE_DIR}:/app/allure-results \
                              -v ${SCREENSHOTS_DIR}:/app/screenshots \
                              ${params.IMAGE_FULL} \
                              python -m pytest ${pytestArgs}
                        """
                    } catch (Exception e) {
                        // Если тесты упали, мы ловим ошибку, чтобы pipeline не прервался
                        // и мы смогли увидеть логи команды ls -R ниже
                        echo "Тесты завершились с ошибками или упали: ${e.message}"
                        currentBuild.result = 'FAILURE'
                    } finally {
                        echo "=== Проверка сгенерированных файлов Allure на агенте ==="
                        // Если этот шаг покажет файлы .json, значит плагин Allure их точно увидит
                        sh "ls -R ${ALLURE_DIR}"
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
                    // Указываем относительный путь от корня WORKSPACE, соответствующий ALLURE_DIR
                    results: [[path: 'allure-results']],
                    commandline: 'Allure 2.29.0'
                ])
            }
        }
    }
}
