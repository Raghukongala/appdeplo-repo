pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Raghukongala/appdeplo-repo.git'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t tcs-calculator:latest .'
            }
        }

        stage('Docker Run') {
            steps {
                sh 'docker stop tcs-calculator || true'
                sh 'docker rm tcs-calculator || true'
                sh 'docker run -d --name tcs-calculator -p 5000:5000 tcs-calculator:latest'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 5'
                sh 'curl -f http://localhost:5000/health'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
