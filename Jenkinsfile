pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Привет! Это мой первый пайплайн!'
            }
        }

        stage('Build') {
            steps {
                echo 'Собираем проект...'
                sh 'echo "Build completed"'
            }
        }

        stage('Test') {
            steps {
                echo 'Запускаем тесты...'
                sh 'echo "All tests passed"'
            }
        }
    }
}