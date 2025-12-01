pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                bat '"C:\\Program Files\\Python314\\python.exe" -m pip install selenium webdriver-manager'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"C:\\Program Files\\Python314\\python.exe" -u run_all_tests.py'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
        }
    }
}