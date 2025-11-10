pipeline {
    agent any

    stages {
        stage('Check Environment') {
            steps {
                echo 'Проверяем окружение...'
                sh '''
                    echo "=== Доступные инструменты ==="
                    python3 --version || echo "Python3 не найден"
                    python --version || echo "Python не найден"
                    pip3 --version || echo "Pip3 не найден"
                    pip --version || echo "Pip не найден"
                    echo "=== Содержимое проекта ==="
                    ls -la
                    echo "=== Файл зависимостей ==="
                    if [ -f "requirements.txt" ]; then
                        cat requirements.txt
                    else
                        echo "requirements.txt не найден"
                    fi
                    echo "=== Структура тестов ==="
                    find . -name "*test*.py" -type f | head -10
                '''
            }
        }

        stage('Hello') {
            steps {
                echo 'Привет! Это мой первый пайплайн!'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Устанавливаем зависимости...'
                sh '''
                    python3 -m pip install --upgrade pip
                    if [ -f "requirements.txt" ]; then
                        python3 -m pip install -r requirements.txt
                    else
                        echo "requirements.txt не найден, устанавливаем pytest"
                        python3 -m pip install pytest
                    fi
                    echo "=== Установленные пакеты ==="
                    python3 -m pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Запускаем тесты...'
                sh '''
                    echo "=== Запуск тестов ==="

                    # Пробуем разные способы запуска тестов
                    if [ -d "tests" ]; then
                        echo "Запуск тестов из папки tests"
                        python3 -m pytest tests/ -v
                    elif [ -d "test" ]; then
                        echo "Запуск тестов из папки test"
                        python3 -m pytest test/ -v
                    else
                        echo "Поиск тестов во всем проекте"
                        python3 -m pytest . -v
                    fi
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Собираем проект...'
                sh 'echo "Build completed"'
            }
        }
    }

    post {
        always {
            echo 'Пайплайн завершен!'
        }
        success {
            echo '✅ Все тесты прошли успешно!'
        }
        failure {
            echo '❌ Пайплайн завершился с ошибкой'
        }
    }
}