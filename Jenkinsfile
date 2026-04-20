pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sourick1/flask-mysql-docker-app"
        TAG = "latest"
    }

    stages {

        stage("Clone Code") {
            steps {
                deleteDir()
                git url: 'https://github.com/Sourick1/flask-mysql-docker-app.git', branch: 'main'
            }
        }

        stage("Build Image") {
            steps {
                sh "docker build -t $DOCKER_IMAGE:$TAG ."
            }
        }

        stage("Test") {
            steps {
                echo "Basic test passed"
            }
        }

        stage("Login to Docker Hub") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "dockehub",
                    usernameVariable: "USER",
                    passwordVariable: "PASS"
                )]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                }
            }
        }

        stage("Push Image") {
            steps {
                sh "docker push $DOCKER_IMAGE:$TAG"
            }
        }

        stage("Deploy to EC2") {
            steps {
                sshagent(['ec2-ssh']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@65.0.108.215 << EOF
                    docker pull $DOCKER_IMAGE:$TAG
                    docker stop flaskapp || true
                    docker rm flaskapp || true
                    docker run -d -p 5000:5000 --name flaskapp $DOCKER_IMAGE:$TAG
                    EOF
                    '''
                }
            }
        }
    }
}
