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
                timeout(time: 5, unit: 'MINUTES') {
                    bat '"C:\\Program Files\\Python314\\python.exe" run_all_tests.py'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
        }
    }
}