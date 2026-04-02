pipeline {
    agent any

    environment {
        AWS_REGION      = "ap-south-1"
        AWS_ACCOUNT_ID  = "957948932374"
        ECR_REPO        = "myapp-dev-app"
        IMAGE_TAG       = "v${BUILD_NUMBER}"
        ECR_URI         = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
        ECS_CLUSTER     = "myapp-dev"
        ECS_SERVICE     = "myapp-dev"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Raghukongala/appdeplo-repo.git'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
            }
        }

        stage('Push to ECR') {
            steps {
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_URI}:latest
                    docker push ${ECR_URI}:${IMAGE_TAG}
                    docker push ${ECR_URI}:latest
                """
            }
        }

        stage('Deploy to ECS') {
            steps {
                sh """
                    aws ecs update-service \
                        --cluster ${ECS_CLUSTER} \
                        --service ${ECS_SERVICE} \
                        --force-new-deployment \
                        --region ${AWS_REGION}
                """
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 30'
                sh 'curl -f http://myapp-dev-alb-1786334768.ap-south-1.elb.amazonaws.com/health'
            }
        }
    }

    post {
        success {
            echo "Deployed ${ECR_URI}:${IMAGE_TAG} successfully"
        }
        failure {
            echo "Deployment failed"
        }
    }
}
