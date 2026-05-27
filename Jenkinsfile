pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        IMAGE_NAME = "employee-api"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '=== Checking out code from GitHub ==='
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '=== Building Docker image ==='
                script {
                    sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
                }
            }
        }

        stage('Test') {
            steps {
                echo '=== Running health check ==='
                script {
                    sh '''
                        docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -c "
from app.main import app
from app.database import Base
print('✓ FastAPI app imported successfully')
print('✓ Database models imported successfully')
"
                    '''
                }
            }
        }

        stage('Start Services') {
            steps {
                echo '=== Starting Docker services ==='
                script {
                    sh 'docker compose up -d'
                }
            }
        }

        stage('Validate Services') {
            steps {
                echo '=== Validating running services ==='
                script {
                    sh '''
                        echo "Waiting for app to be ready..."
                        sleep 3
                        curl -f http://localhost:8000/ || exit 1
                        echo "✓ App is healthy"
                    '''
                }
            }
        }

        stage('Push to Registry (Optional)') {
            when {
                branch 'main'
            }
            steps {
                echo '=== Pushing image to registry ==='
                script {
                    sh '''
                        # Uncomment to push to Docker Hub
                        # docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/your-username/${IMAGE_NAME}:${IMAGE_TAG}
                        # docker push ${REGISTRY}/your-username/${IMAGE_NAME}:${IMAGE_TAG}
                        echo "✓ Push step configured (uncomment to enable)"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo '=== Cleaning up ==='
            sh 'docker compose down || true'
        }

        success {
            echo '✓ Build and tests passed!'
        }

        failure {
            echo '✗ Build or tests failed!'
        }
    }
}
