pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Target environment')
    }

    environment {
        AWS_REGION     = 'ap-south-1'
        AWS_ACCOUNT_ID = '957948932374'
        ECR_REPO       = "myapp-${params.ENV}-app"
        IMAGE_TAG      = "${BUILD_NUMBER}"
        ECS_CLUSTER    = "myapp-${params.ENV}-cluster"
        ECS_SERVICE    = "myapp-${params.ENV}-service"
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'Accesskey',         variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'Secret access key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh """
                        export AWS_DEFAULT_REGION=${AWS_REGION}
                        aws ecr get-login-password --region ${AWS_REGION} | \\
                          docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

                        docker tag ${ECR_REPO}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}
                        docker tag ${ECR_REPO}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:latest

                        docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}
                        docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:latest
                    """
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                withCredentials([
                    string(credentialsId: 'Accesskey',         variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'Secret access key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh """
                        export AWS_DEFAULT_REGION=${AWS_REGION}
                        aws ecs update-service \\
                          --cluster ${ECS_CLUSTER} \\
                          --service ${ECS_SERVICE} \\
                          --force-new-deployment \\
                          --region ${AWS_REGION}

                        echo "Waiting for service to stabilize..."
                        aws ecs wait services-stable \\
                          --cluster ${ECS_CLUSTER} \\
                          --services ${ECS_SERVICE} \\
                          --region ${AWS_REGION}

                        echo "Deployment complete!"
                    """
                }
            }
        }
    }

    post {
        always { cleanWs() }
        success { echo "App deployed successfully to ${params.ENV}" }
        failure { echo "App deployment FAILED on ${params.ENV}" }
    }
}
