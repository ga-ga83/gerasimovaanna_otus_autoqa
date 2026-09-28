pipeline {
    agent any

    environment {
        PYTHON_HOME = "${WORKSPACE}/python"
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                set -e
                # 1. Ставим системные зависимости и браузеры
                apt-get update
                apt-get install -y wget gnupg ca-certificates curl unzip fonts-liberation libgtk-3-0 libnss3 firefox-esr

                # Установка