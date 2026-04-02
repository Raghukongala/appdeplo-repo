pipeline {
    agent any

    environment {
        AWS_REGION     = "ap-south-1"
        AWS_ACCOUNT_ID = "957948932374"
        ECR_REPO       = "myapp-dev-app"
        IMAGE_TAG      = "v${BUILD_NUMBER}"
        ECR_URI        = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
        ECS_CLUSTER    = "myapp-dev"
        ECS_SERVICE    = "myapp-dev"
        ALB_URL        = "http://myapp-dev-alb-1786334768.ap-south-1.elb.amazonaws.com"
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

        stage('Wait for ECS Stability') {
            steps {
                sh """
                    aws ecs wait services-stable \
                        --cluster ${ECS_CLUSTER} \
                        --services ${ECS_SERVICE} \
                        --region ${AWS_REGION}
                """
            }
        }

        stage('Smoke Test') {
            steps {
                sh """
                    echo "Testing health endpoint..."
                    curl -f ${ALB_URL}/health

                    echo "Testing calculate endpoint..."
                    curl -f -X POST ${ALB_URL}/calculate \
                        -H 'Content-Type: application/json' \
                        -d '{"a": 10, "b": 5, "operator": "+"}'
                """
            }
        }
    }

    post {
        success {
            echo "Deployment successful - ${ALB_URL}"
        }
        failure {
            echo "Deployment failed - check logs"
        }
    }
}
