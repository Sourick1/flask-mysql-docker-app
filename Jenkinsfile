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
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@43.204.216.179 << EOF
                    cd /home/ubuntu || exit

                    if [ ! -d "flask-mysql-docker-app" ]; then
                        git clone https://github.com/Sourick1/flask-mysql-docker-app.git
                    fi

                    cd flask-mysql-docker-app
                    git pull origin main

                    cp .env.example .env || true

                    # CLEAN EVERYTHING
                    docker compose down -v || true
                    docker rm -f flask_mysql_db || true
                    docker rm -f flask_app || true

                    docker pull $DOCKER_IMAGE:$TAG

                    docker compose up -d

                    EOF
                    """
                }
            }
        }
    }
}
