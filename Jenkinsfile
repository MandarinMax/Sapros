pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip3 install --user pytest && python3 -m pytest'
            }
        }
    }
}