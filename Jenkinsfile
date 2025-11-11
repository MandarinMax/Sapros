pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '--user root'
        }
    }

    stages {
        stage('Test') {
            steps {
                echo 'Запуск тестов...'
                sh '''
                    python --version
                    pip install -r requirements.txt
                    pytest tests/ -v
                '''
            }
        }
    }

    post {
        always {
            echo 'Тестирование завершено'
        }
    }
}