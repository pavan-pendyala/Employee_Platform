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
                echo '=== Building Docker image with Docker Compose ==='
                script {
                    sh 'docker-compose build app'
                }
            }
        }

        stage('Test') {
            steps {
                echo '=== Running health check ==='
                script {
                    sh '''
                        docker-compose run --rm app python -c "
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
                    sh 'docker-compose up -d'
                }
            }
        }

        stage('Validate Services') {
            steps {
                echo '=== Validating running services ==='
                script {
                    sh '''
                        echo "Waiting for app to be ready..."
                        sleep 5
                        docker-compose exec -T app curl -f http://localhost:8000/ || exit 1
                        echo "✓ App is healthy"
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
