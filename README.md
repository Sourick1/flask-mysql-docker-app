# 🚀 Flask + MySQL Deployment on AWS with CI/CD

A production-like DevOps project demonstrating deployment of a Flask application using Docker, Jenkins CI/CD, and AWS services.

---

## 📌 Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL (AWS RDS)
- **Containerization:** Docker
- **CI/CD:** Jenkins
- **Cloud:** AWS EC2, RDS, S3
- **Version Control:** Git & GitHub

---

## 🧩 Architecture

User → EC2 (Flask App in Docker) → RDS (MySQL)  → S3 (File Storage)

---

## ⚙️ Features

- Dockerized Flask application
- Jenkins CI/CD pipeline (build → test → deploy)
- AWS EC2 deployment
- AWS RDS for managed MySQL database
- AWS S3 integration using boto3
- Secure configuration using environment variables

---

## 🔄 CI/CD Pipeline Flow

1. Developer pushes code to GitHub
2. Jenkins webhook triggers pipeline
3. Jenkins builds Docker image
4. Image is deployed to EC2
5. Application connects to RDS
6. Files stored/retrieved from S3

---

## 🚀 Setup Instructions

### 1. Clone Repo
```bash
git clone https://github.com/Sourick1/flask-mysql-cicd-pipeline.git
cd flask-aws-devops-project

2. Configure Environment Variables

Create .env file:

DB_HOST=your-rds-endpoint
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-db-name



3. Run with Docker
docker-compose up --build

🎯 What I Learned
End-to-end CI/CD pipeline setup
Docker-based deployment workflows
AWS infrastructure integration (EC2, RDS, S3)
Real-world DevOps practices


📬 Connect with Me
LinkedIn: https://www.linkedin.com/in/sourick-chowdhury/
