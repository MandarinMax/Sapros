pipeline {
    agent any

    stages {
        stage('Unit Test') {
            steps {
                script {
                    // Используем python3 -m pip вместо pip
                    sh 'python3 -m pip install -r requirements.txt'
                    sh 'python3 -m pytest'
                }
            }
        }
    }
}