pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Unit Test') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'  // Установить зависимости проекта
                    sh 'pytest'  // Запустить тесты
                }
            }
        }
        // Дополнительные этапы для сборки, деплоя и т. д.
    }


