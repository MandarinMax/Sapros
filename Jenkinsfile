pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt pytest pytest-html
                '''
                sh '''
                    . venv/bin/activate
                    pytest --html=report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            junit 'report.xml'  // Альтернатива для отчетов
            archiveArtifacts 'report.html'  // Сохраняем отчет как артефакт
        }
    }
}