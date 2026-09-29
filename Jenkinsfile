pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-python-test-image'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        NETWORK_NAME = 'prestashop_network'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${FULL_IMAGE} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'mkdir -p reports screenshots'

                    def networkExists = sh(script: "docker network ls --format '{{.Name}}' | grep -q '^${NETWORK_NAME}\$'", returnStatus: true) == 0
                    if (!networkExists) {
                        error "Сеть ${NETWORK_NAME} не найдена! Сначала запусти PrestaShop через docker compose."
                    }

                    // ── Отключаем debug mode и скрываем Symfony toolbar ──
                    sh '''
                        echo "=== Отключение debug mode PrestaShop ==="

                        # 1. Показываем текущее состояние
                        echo "--- Текущий _PS_MODE_DEV_ ---"
                        docker exec prestashop grep -n "_PS_MODE_DEV_" /var/www/html/config/defines.inc.php 2>/dev/null || echo "Не найдено в defines.inc.php"

                        # 2. Пробуем отключить (разные варианты кавычек и пробелов)
                        docker exec prestashop sed -i "s/define('_PS_MODE_DEV_', true)/define('_PS_MODE_DEV_', false)/" /var/www/html/config/defines.inc.php 2>/dev/null || true
                        docker exec prestashop sed -i 's/define("_PS_MODE_DEV_", true)/define("_PS_MODE_DEV_", false)/' /var/www/html/config/defines.inc.php 2>/dev/null || true
                        docker exec prestashop sed -ri "s/define\$\\s*'_PS_MODE_DEV_'\\s*,\\s*true\\s*\$/define('_PS_MODE_DEV_', false)/" /var/www/html/config/defines.inc.php 2>/dev/null || true
                        docker exec prestashop sed -ri "s/define\$\\s*\"_PS_MODE_DEV_\"\\s*,\\s*true\\s*\$/define('_PS_MODE_DEV_', false)/" /var/www/html/config/defines.inc.php 2>/dev/null || true

                        # 3. Проверяем результат
                        echo "--- После замены ---"
                        docker exec prestashop grep -n "_PS_MODE_DEV_" /var/www/html/config/defines.inc.php 2>/dev/null || echo "Не найдено"

                        # 4. Резервный план: скрываем Symfony toolbar через CSS
                        # Добавляем display:none в существующие CSS-файлы админ-темы
                        docker exec prestashop sh -c 'for f in $(find /var/www/html -maxdepth 6 -name "*.css" -path "*/themes/new-theme/*"); do echo ".sf-toolbarreset, .sf-toolbar { display: none !important; }" >> "$f"; done' 2>/dev/null || true
                        echo "CSS override добавлен в файлы админ-темы"

                        # 5. Очищаем весь кэш
                        docker exec prestashop rm -rf /var/www/html/var/cache/* 2>/dev/null || true
                        docker exec prestashop rm -rf /var/www/html/cache/smarty/* 2>/dev/null || true
                        echo "Кэш очищен"

                        echo "=== Готово ==="
                    '''

                    // ── Запуск тестов ──
                    sh """
                        docker run --rm \\
                          --user testuser \\
                          --network ${NETWORK_NAME} \\
                          -v \$(pwd)/reports:/home/testuser/reports \\
                          -v \$(pwd)/screenshots:/home/testuser/screenshots \\
                          ${FULL_IMAGE}
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
                }
                failure {
                    echo 'Тесты упали — проверь логи и скриншоты.'
                }
            }
        }
    }

    post {
        always {
            script {
                sh "docker rmi ${FULL_IMAGE} || true"
            }
        }
    }
}
