🚀 **Flask + MySQL Two-Tier Application with CI/CD (Docker + Jenkins + AWS)**

🔥 Fully automated CI/CD pipeline using Jenkins, Docker, Webhooks & AWS EC2

📌 Overview
This project demonstrates a complete DevOps workflow by building and deploying a two-tier application using:

Flask → Backend application
MySQL → Database
Docker & Docker Compose → Containerization
Jenkins → CI/CD Pipeline
GitHub Webhooks → Automation trigger
AWS EC2 → Deployment


👉 Fully automated pipeline:
Code Push → Build → Test → Deploy → Live Application

🏗️ Architecture
Developer (GitHub Push)→ GitHub Webhook → Jenkins → Build Docker Image→ Deploy to EC2 (Docker Compose)→ Flask App→ MySQL Database → User


⚙️ CI/CD Workflow
Developer pushes code to GitHub
GitHub Webhook triggers Jenkins pipeline
Jenkins executes:
Checkout code
Build Docker image
Run tests
Deploy containers using Docker Compose
Application is updated automatically on EC2

🐳 Tech Stack
Python (Flask)
MySQL
Docker
Docker Compose
Jenkins
AWS EC2
Git & GitHub Webhooks


📂 Project Setup (Local)
1. Clone Repository
git clone https://github.com/Sourick1/flask-mysql-cicd-pipeline.git
cd flask-mysql-docker-app

2. Setup Environment Variables
cp .env.example .env

3. Run Application
docker compose up -d --build
🌐 Access Application
Local: http://localhost:5000
EC2: http://<your-ec2-public-ip>:5000

🗄️ Database Setup

If the table is not auto-created:

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    author VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
🔍 Verification
docker ps
docker logs flask_app


💾 Data Persistence
Docker volumes are used
Data persists even after container restarts


🔄 Jenkins Pipeline Stages
✅ Checkout Code
✅ Build Docker Image
✅ Test
✅ Deploy to EC2


🔗 Webhook Integration
GitHub Webhook triggers Jenkins automatically
No manual build required
Ensures real-time CI/CD


⚠️ Challenges Faced
Port conflict issues (5000 already in use)
Containers not stopping properly
Webhook not triggering (URL issues)
Jenkins pipeline debugging
MySQL startup delay


🎯 Key Learnings
End-to-end CI/CD pipeline implementation
Docker multi-container orchestration
Webhook-based automation
Debugging real deployment issues
Integrating application + infrastructure

🧹 Cleanup
docker compose down -v

🚀 Future Improvements
Add Nginx reverse proxy
Use Docker Hub for versioning
Kubernetes deployment
Monitoring (Prometheus + Grafana)

👨‍💻 Author

Sourick Chowdhury
Aspiring DevOps Engineer
