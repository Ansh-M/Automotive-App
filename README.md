Deploy Automotive App to Kubernetes

A complete DevOps implementation for containerising and deploying an Automotive PHP Laravel Application onto a Kubernetes cluster (Minikube) using Docker and CI/CD pipelines with zero-downtime rolling updates.

📌 Project Overview

This project focuses on deploying a Laravel-based Automotive Web Application into a Kubernetes environment using Minikube.

The entire workflow demonstrates how a traditional PHP application can be transformed into a containerised, scalable, and production-ready system.

The key highlight of this project is zero-downtime Rolling Updates, ensuring that users never experience service interruption during deployments.

✨ Key Features
⚙️ Containerised Laravel application using Docker
🔄 Zero-downtime Rolling Updates in Kubernetes
🚀 CI/CD pipeline using GitHub Actions / Jenkins
📦 Deployment on Minikube (local Kubernetes cluster)
🌐 Kubernetes Service for external access
❤️ Health-check-based deployment strategy
🔐 Secure credential management using secrets
🛠️ Tech Stack
Category	Technology
Application	PHP, Laravel
Containerization	Docker
Orchestration	Kubernetes (Minikube)
CI/CD	GitHub Actions / Jenkins
Version Control	Git, GitHub
📂 Project Structure
Automotive-App-Kubernetes/
│
├── Dockerfile
├── .dockerignore
├── README.md
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
└── .github/
    └── workflows/
        └── deploy.yml
⚙️ Prerequisites

Make sure you have the following installed:

Docker
Minikube
kubectl
Git
PHP & Composer (for Laravel setup)
🚀 Deployment Steps
Step 1 — Clone the Repository
git clone https://github.com/your-username/Automotive-App-Kubernetes.git
cd Automotive-App-Kubernetes
Step 2 — Start Minikube
minikube start
Step 3 — Build Docker Image
docker build -t automotive-app:latest .
Step 4 — Apply Kubernetes Manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
Step 5 — Check Running Pods
kubectl get pods
kubectl get services
Step 6 — Access the Application
minikube service automotive-service
🔄 CI/CD Pipeline Stages
Stage 1 — Checkout
Pull latest code from repository
Stage 2 — Build Docker Image
Create container image of Laravel app
Stage 3 — Push Image
Push image to Docker Hub
Stage 4 — Deploy to Kubernetes
Apply deployment and service manifests
Stage 5 — Verify Deployment
Ensure pods are running and healthy
⚡ Zero-Downtime Rolling Updates

The deployment uses a Kubernetes rolling update strategy:

replicas: 2
maxSurge: 1
maxUnavailable: 0

This ensures:

New pods are created before old ones are removed
Application remains available at all times
No service interruption during updates
🔐 Secrets Configuration

Store sensitive data securely:

Docker credentials
Kubernetes configs
API keys


Use:

GitHub Secrets OR
Kubernetes Secrets
📈 Future Improvements
🔧 Add Horizontal Pod Autoscaling
📊 Integrate monitoring (Prometheus & Grafana)
🔐 Implement HTTPS with Ingress
🚀 Deploy on cloud (AWS EKS / GCP GKE)
👨‍💻 Project Details
Division: D2
Group: 04D2
Project No: DO-16
Subject: DevOps

👥 Team Members
Sr No	Name	Enrollment Number
01  Ameya Dole	        EN22CS301111
02  Amishi Talwar	      EN22CS301112
03  Ansh Mundra	        EN22CS301142
04  Anuj Devnani 	      EN22CS301164
05  Arpith Shukla       EN22CS301203
  
🏫 Institution
Medicaps University
Datagami Skill-Based Course
Academic Year: 2025–2026

🙌 Mentor
Prof. Akshay Saxena
