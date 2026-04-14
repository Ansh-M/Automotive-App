# AutoVerse 🚗
### DevOps Project DO-16 | Group 04D2 | Division D2

A lightweight automotive car showcase web app built with **Python Flask**, containerized with **Docker**, designed for Kubernetes deployment.

---

## 📌 Overview  

This project showcases a car showcase web application with modern DevOps practices including containerization and deployment readiness.

💡 **Key Highlight:**  
Lightweight app with clean UI and API support for car catalog browsing.

---

## ✨ Features  

- Car Catalog with multiple categories  
- Search & Filter functionality  
- Car Detail Page with booking option  
- REST API support  
- Dockerized Application  
- Ready for Kubernetes deployment  

---

## 🛠️ Tech Stack  

| Category | Technology |
|----------|-----------|
| Application | Python, Flask |
| Containerization | Docker |
| Orchestration | Kubernetes (Minikube) |
| CI/CD | GitHub Actions / Jenkins |
| Version Control | Git, GitHub |

---

## 🗂️ Project Structure  

```
autoverse/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── templates/
│   ├── index.html
│   └── detail.html
└── README.md
```

---

## ⚙️ Prerequisites  

- Python 3.11+  
- pip  
- Docker  
- Git  

---

## 🚀 Deployment Guide  

### 1️⃣ Clone the Repository  
git clone <your-repo-url>  
cd autoverse  

### 2️⃣ Run Locally  
pip install -r requirements.txt  
python app.py  

### 3️⃣ Run with Docker  
docker build -t autoverse:v1 .  
docker run -d -p 5000:5000 autoverse:v1  

---

## 🔄 CI/CD Pipeline  

- Checkout Code  
- Build Docker Image  
- Push to Docker Hub  
- Deploy to Kubernetes  

---

## ⚡ Zero-Downtime Strategy  

replicas: 2  
maxSurge: 1  
maxUnavailable: 0  

---

## 🔐 Secrets Management  

- Environment Variables  
- Secure API handling  

---

## 📈 Future Enhancements  

- Add authentication  
- Improve UI/UX  
- Deploy on cloud  
- Add monitoring tools  

---

## 👨‍💻 Project Info  

- Division: D2  
- Group: 04D2  
- Project No: DO-16  
- Subject: DevOps  

---

## 👥 Team Members  

- Ameya Dole - EN22CS301111
- Amishi Talwar - EN22CS301112 
- Ansh Mundra - EN22CS301142  
- Anuj Devnani - EN22CS301164 
- Arpith Shukla - EN22CS301203 

---

## 🏫 Institution  

Medicaps University  

---

## 🙌 Mentor  

Prof. Akshay Saxena  
