pipeline {
    agent any

    environment {
        CONDA_ENV = 'mlip'
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                echo 'In Python, this stage is usually for packaging or skipping.'
                '''
            }
        }

        stage('Set Up Conda Environment') {
            steps {
                sh '''
                echo "Activating conda environment: $CONDA_ENV"
                conda info --envs
                conda run -n $CONDA_ENV python --version
                '''
            }
        }

        stage('Run API in Background') {
            steps {
                sh '''
                echo "Starting the Flask API..."

                # Start the API in the background
                nohup conda run -n $CONDA_ENV python src/recommender_api.py > api.log 2>&1 &

                # Wait for the API to be ready
                for i in {1..10}; do
                    echo "Waiting for API to be up..."
                    curl -s http://localhost:8082/recommend/1 && break
                    sleep 2
                done
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                echo "Running tests with pytest..."
                conda run -n $CONDA_ENV pytest --disable-warnings
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
            sh '''
            pkill -f recommender_api.py || true
            '''
        }
    }
}
