pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = 'YOUR_AWS_ACCOUNT_ID'
        ECR_REPOSITORY = 'jenkins-aws-webapp'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_NAME = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
        APP_SERVER = 'APP_SERVER_PRIVATE_IP'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    docker rm -f jenkins-test || true

                    docker run -d \
                    --name jenkins-test \
                    -p 5001:5000 \
                    ${IMAGE_NAME}:${IMAGE_TAG}

                    sleep 5

                    curl -f http://localhost:5001/health

                    docker rm -f jenkins-test
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password \
                    --region ${AWS_REGION} | \
                    docker login \
                    --username AWS \
                    --password-stdin \
                    ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}

                    docker tag \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    ${IMAGE_NAME}:latest

                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        aws ecr get-login-password \
                        --region ${AWS_REGION} |
                        docker login \
                        --username AWS \
                        --password-stdin \
                        ${ECR_REGISTRY}

                        docker pull ${IMAGE_NAME}:${IMAGE_TAG}

                        docker rm -f jenkins-aws-webapp || true

                        docker run -d \
                        --name jenkins-aws-webapp \
                        --restart unless-stopped \
                        -p 5000:5000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                    '
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        curl -f http://localhost:5000/health
                    '
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }

        failure {
            echo 'Deployment failed. Check the console output.'
        }

        always {
            sh '''
                docker rm -f jenkins-test || true
            '''
        }
    }
}