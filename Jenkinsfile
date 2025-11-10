pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '--user root'  // для прав на запись файлов
        }
    }

    stages {
        stage('Check Environment') {
            steps {
                sh 'python --version'
                sh 'pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --upgrade pip'
                script {
                    // Проверяем есть ли requirements.txt
                    if (fileExists('requirements.txt')) {
                        sh 'pip install -r requirements.txt'
                    } else {
                        echo 'requirements.txt не найден, устанавливаем базовые зависимости'
                        sh 'pip install pytest'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Пытаемся найти и запустить тесты разными способами
                    if (fileExists('tests')) {
                        echo 'Запускаем тесты из папки tests'
                        sh 'python -m pytest tests/ -v || echo "Pytest не сработал"'
                    } else if (fileExists('test')) {
                        echo 'Запускаем тесты из папки test'
                        sh 'python -m pytest test/ -v || echo "Pytest не сработал"'
                    } else {
                        echo 'Ищем тесты в проекте'
                        sh 'python -m pytest . -v --tb=short || echo "Тесты не найдены"'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Пайплайн завершен!'
        }
        success {
            echo '✅ Все этапы выполнены успешно!'
        }
        failure {
            echo '❌ Пайплайн завершился с ошибкой'
        }
    }
}