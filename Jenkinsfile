pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-u root'
        }
    }

    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt pytest pytest-html'
                sh 'pytest --html=report.html --self-contained-html'
            }
        }
    }

    post {
        always {
            archiveArtifacts 'report.html'
        }
    }
}