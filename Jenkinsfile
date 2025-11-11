pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && pip install pytest pytest-html'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest --html=report.html --self-contained-html'
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'report.html',
                        reportName: 'Pytest Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed'
        }
    }
}