pipeline {
    agent any
    
    environment {
        // Указываем путь к Python (настрой под свою систему)
        PYTHON_PATH = 'python'
        // Или для Windows: PYTHON_PATH = 'C:\\Python39\\python.exe'
    }

    stages {
        stage('Hello') {
            steps {
                echo 'Привет! Это мой первый пайплайн для Python проекта!'
            }
        }

        stage('Setup') {
            steps {
                echo 'Настройка окружения...'
                // Создаем виртуальное окружение
                sh '${PYTHON_PATH} -m venv venv'
                // Активируем и устанавливаем зависимости
                sh 'venv\\Scripts\\pip install -r requirements.txt'  // Windows
                // Для Linux/Mac: sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Build') {
            steps {
                echo 'Проверка кода...'
                // Проверка синтаксиса
                sh 'venv\\Scripts\\python -m py_compile *.py'  // Windows
                // Для Linux/Mac: sh 'source venv/bin/activate && python -m py_compile *.py'

                // Или проверка стиля кода
                sh 'venv\\Scripts\\python -m pylint *.py --fail-under=7 || true'  // Опционально
            }
        }

        stage('Test') {
            steps {
                echo 'Запускаем тесты...'
                // Запуск тестов через unittest
                sh 'venv\\Scripts\\python -m unittest discover -s tests -v'  // Windows
                // Для Linux/Mac: sh 'source venv/bin/activate && python -m unittest discover -s tests -v'

                // Или если используете pytest:
                // sh 'venv\\Scripts\\python -m pytest tests/ -v'

                // Или если тесты в конкретном файле:
                // sh 'venv\\Scripts\\python -m unittest test_module.py'
            }
            post {
                always {
                    // Сохраняем отчеты о тестах (если генерируются)
                    junit 'test-reports/*.xml'  // если используете генерацию JUnit отчетов
                }
            }
        }

        stage('Reports') {
            steps {
                echo 'Генерация отчетов...'
                // Генерация coverage отчета
                sh 'venv\\Scripts\\python -m coverage run -m unittest discover -s tests'
                sh 'venv\\Scripts\\python -m coverage report'
                sh 'venv\\Scripts\\python -m coverage html'

                // Архивируем отчеты
                sh 'tar -czf coverage-report.tar.gz htmlcov/'  // Linux/Mac
                // Для Windows: bat 'tar -czf coverage-report.tar.gz htmlcov/'
            }
        }
    }

    post {
        always {
            echo 'Пайплайн завершен!'
            // Очистка
            sh 'rm -rf venv'  // Linux/Mac
            // Для Windows: bat 'rd /s /q venv'
        }
        success {
            echo 'Все этапы выполнены успешно! 🎉'
            // Можно добавить уведомления
        }
        failure {
            echo 'Пайплайн завершился с ошибкой! ❌'
            // Можно добавить уведомления об ошибке
        }
    }
}