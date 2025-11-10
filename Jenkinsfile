pipeline {
    agent any
    
    environment {
        // Используем python3 вместо python
        PYTHON_PATH = 'python3'
    }

    stages {
        stage('Setup') {
            steps {
                echo 'Проверяем доступность Python...'
                sh '${PYTHON_PATH} --version'
                sh '${PYTHON_PATH} -m venv venv'
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Запускаем тесты...'
                //sh 'venv/bin/python -m unittest discover -s tests -v'
                // Или для pytest:
                 sh 'venv/bin/python -m pytest tests/ -v'
            }
        }
    }
}