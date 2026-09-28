pipeline {
    agent none

    environment {
        IMAGE_NAME = 'my-python-test-image'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            agent { label 'docker-slave' }
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            agent { label 'docker-slave' }
            steps {
                script {
                    // Сборка образа с контекстом текущей директории, где лежит Dockerfile
                    sh "docker build -t ${FULL_IMAGE} ."
                }
            }
        }

        stage('Run Tests') {
            agent { label 'docker-slave' }
            steps {
                script {
                    // Запуск контейнера с пробросом volumes для отчётов/скриншотов (если тесты их создают)
                    // --user testuser: запускаем как непривилегированный пользователь из Dockerfile
                    // -e DISPLAY можно добавить, если тесты используют браузер в GUI-режиме (нужен VNC/Xvfb)
                    sh """
                        docker run --rm \\
                          --user testuser \\
                          -v \$(pwd)/reports:/home/testuser/reports \\
                          -v \$(pwd)/screenshots:/home/testuser/screenshots \\
                          ${FULL_IMAGE}
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/**/*', allowEmpty: true
                    archiveArtifacts artifacts: 'screenshots/**/*', allowEmpty: true
                }
                failure {
                    echo 'Тесты упали — проверь логи и скриншоты.'
                }
            }
        }
    }

    post {
        always {
            // Очистка образов и контейнеров, чтобы не забивать диск
            script {
                sh "docker rmi ${FULL_IMAGE} || true"
            }
        }
    }
}