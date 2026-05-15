pipeline {
    agent any
    environment {
        IMAGE_NAME     = "flask-student-app"
        SELENIUM_IMG   = "selenium-tests"
        CONTAINER_NAME = "flask-app-container"
        APP_PORT       = "5000"
        NETWORK_NAME   = "ci-network"
    }
    stages {
        stage('Code Build') {
            steps {
                echo '=== STAGE 1: Building Application ==='
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Unit Testing') {
            steps {
                echo '=== STAGE 2: Running Unit Tests ==='
                sh '''
                    . venv/bin/activate
                    mkdir -p reports
                    pytest tests/test_unit.py -v --tb=short --junitxml=reports/unit-test-results.xml
                '''
            }
            post {
                always {
                    junit 'reports/unit-test-results.xml'
                }
            }
        }
        stage('Containerized Deployment') {
            steps {
                echo '=== STAGE 3: Deploying Docker Container ==='
                sh '''
                    docker network inspect ${NETWORK_NAME} >/dev/null 2>&1 || docker network create ${NETWORK_NAME}
                    docker rm -f ${CONTAINER_NAME} || true
                    docker build -t ${IMAGE_NAME}:latest -f Dockerfile.app .
                    docker run -d --name ${CONTAINER_NAME} --network ${NETWORK_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:latest
                    sleep 10
                    echo "App deployed on port ${APP_PORT}"
                '''
            }
        }
        stage('Containerized Selenium Testing') {
            steps {
                echo '=== STAGE 4: Running Selenium Tests ==='
                sh '''
                    docker rm -f selenium-hub selenium-chrome || true
                    docker run -d --name selenium-hub --network ${NETWORK_NAME} -p 4444:4444 selenium/hub:4.21.0
                    docker run -d --name selenium-chrome --network ${NETWORK_NAME} \
                        -e SE_EVENT_BUS_HOST=selenium-hub \
                        -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
                        -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
                        selenium/node-chrome:4.21.0
                    sleep 15
                    docker build -t ${SELENIUM_IMG}:latest -f Dockerfile.selenium .
                    docker run --rm --network ${NETWORK_NAME} ${SELENIUM_IMG}:latest
                '''
            }
            post {
                always {
                    sh 'docker rm -f selenium-hub selenium-chrome || true'
                }
            }
        }
    }
    post {
        success { echo '✅ Pipeline completed successfully!' }
        failure { echo '❌ Pipeline failed. Check logs.' }
        always  { sh 'rm -rf venv || true' }
    }
}
