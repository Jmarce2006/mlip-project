pipeline {
    agent any

    environment {
        FLASK_PORT = "8082"
        CONDA_ENV = "mlip"
        CONDA_BIN = "/opt/conda/bin/conda"
    }

    stages {

        stage('Set Up Conda Environment') {
            steps {
                sh '''#!/bin/bash
                echo "Activating conda environment: $CONDA_ENV"
                $CONDA_BIN run -n $CONDA_ENV python --version
                '''
            }
        }

        stage('Run API in Background') {
            steps {
                sh '''#!/bin/bash
                echo "Starting the Flask API..."
                nohup $CONDA_BIN run -n $CONDA_ENV python src/recommender_api.py > flask.log 2>&1 &
                sleep 5  # wait for API to initialize
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                echo "Running tests with pytest..."
                $CONDA_BIN run -n $CONDA_ENV pytest --disable-warnings
                echo "Tests finished"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy step: Publish your model files or API, if applicable.'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'pkill -f recommender_api.py || true'
        }
    }
}
