pipeline {
    agent any

    environment {
        IMAGE_NAME = 'ci-cd'
        KUBECONFIG = credentials('aacbb3c7-a44f-4d16-9c02-629b5a1b06ca') // Jenkins credential ID for kubeconfig file
        DOCKER_CREDENTIALS = credentials('7bad115c-917e-4cbd-9354-32dd83bd4b2b') // Jenkins credential ID for docker
    }

    parameters {
        string(name: 'REGISTRY', defaultValue: '', description: 'registry name')
    }

    stages {
        stage('Build and Test') {
            steps {

                // Install Python dependencies
                withPythonEnv('python') {
                    sh('python -m pip install -r requirements.txt')
                }

                // Lint python
                sh('make lint')

                // Run bandit
                sh('make bandit')
                
                // Run unit and integration tests
                sh('python -m unittest discover -s . -p "test_*.py"')

                // Run coverage reporting
                sh('make coverage')
            }
        }

        stage('Build Image') {
            steps{
                script {
                    app = docker.build("${DOCKER_CREDENTIALS_USR}/ci-cd")
                    docker.withRegistry("https://registry.hub.docker.com", "${DOCKER_CREDENTIALS}"){
                        app.push("latest")
                    }
                }
                
            }
            
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Apply Kubernetes manifests using kubectl
                sh('export IMAGE=$DOCKER_CREDENTIALS_USR/ci-cd:latest; kubectl --kubeconfig $KUBECONFIG apply -f deployment.yaml')
                sh('kubectl --kubeconfig $KUBECONFIG apply -f service.yaml')
                
                // Check Kubernetes pods' status
                sh('kubectl get pods')
            }
        }
    }

    post {
        always {
            // Archive test results and coverage reports
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
            junit '**/test-results.xml'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}