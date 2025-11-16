pipeline {
    agent any

    stages {
        stage('Install Python Venv') {
            steps {
                sh 'apt-get update && apt-get install -y python3-venv'
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest'
            }
        }
    }
}