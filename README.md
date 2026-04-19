#  Flask + MySQL Two-Tier Application using Docker

## 📌 Overview

This project demonstrates a **two-tier architecture** using:

* **Flask** (Backend)
* **MySQL** (Database)
* **Docker & Docker Compose** (Containerization & Orchestration)

Users can submit messages through a web interface, which are stored in MySQL and displayed dynamically.

---

## 🏗️ Architecture

```
User → Flask App → MySQL Database
```

---

## 🐳 Tech Stack

* Python (Flask)
* MySQL
* Docker
* Docker Compose

---

## ⚙️ Prerequisites

Make sure you have:

* Docker installed
* Git installed (optional)

---

## 📂 Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/Sourick1/flask-mysql-docker-app.git
cd flask-mysql-docker-app
```

---

### 2. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` if needed.

---

### 3. Run Application

```bash
docker compose up -d --build
```

---

## 🌐 Access Application

* Frontend: http://localhost:5000

---

## 🗄️ Database Setup

If table not auto-created, run:

```sql
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    author VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔍 Verification

### Check containers

```bash
docker ps
```

### Check logs

```bash
docker logs flask_app
```

### Access MySQL manually

```bash
docker exec -it flask_mysql_db bash
mysql -u root -p
```

---

## 💾 Data Persistence

* Uses Docker volumes
* Data remains even after container restart

---

## 🌐 Docker Concepts Used

* Dockerfile
* Docker Compose
* Volumes
* Networking
* Environment Variables

---

## 🛠️ Run Without Docker Compose

### Build Image

```bash
docker build -t flaskapp .
```

### Create Network

```bash
docker network create twotier
```

### Run MySQL

```bash
docker run -d \
  --name mysql \
  --network=twotier \
  -e MYSQL_DATABASE=messagesdb \
  -e MYSQL_ROOT_PASSWORD=admin \
  -v mysql-data:/var/lib/mysql \
  mysql:8
```

### Run Flask

```bash
docker run -d \
  --name flaskapp \
  --network=twotier \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=admin \
  -e MYSQL_DB=messagesdb \
  -p 5000:5000 \
  flaskapp
```

---

## ⚠️ Challenges Faced

* Container communication issues → fixed using service names
* MySQL startup delay → handled with retry logic
* Volume persistence debugging

---


## Key Learnings

* Container isolation
* Service-to-service communication
* Debugging using Docker logs
* Managing multi-container applications

---

## 🧹 Cleanup

```bash
docker compose down
```

---

## 🚀 Future Improvements

* Add CI/CD pipeline (GitHub Actions)
* Deploy on AWS (EC2 / ECS)
* Add Nginx reverse proxy
* Add authentication

---

## 👨‍💻 Author

Sourick Chowdhury
