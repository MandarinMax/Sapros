pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv venv --system-site-packages
                    . venv/bin/activate
                    pip install pytest
                    pytest
                '''
            }
        }
    }
}