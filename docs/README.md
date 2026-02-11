# 🚀 AI-Powered Todo Chatbot (K8s Edition)

A **production-ready, secure, multi-user Todo application** enhanced with an **AI Chatbot** and orchestrated using **Kubernetes and Helm**.  
This project was developed as part of **GIAIC Hackathon 2 – Phase IV**.

---

## 🌟 Key Features

- **User Authentication**  
  Secure JWT-based registration and login with token refresh.

- **AI Chatbot Integration**  
  Manage your tasks through a conversational interface powered by OpenAI.

- **User Isolation**  
  Strict data isolation ensuring users only access their own todos.

- **Containerized Orchestration**  
  Fully Dockerized and deployed on Kubernetes (Minikube).

- **Automated Deployment**  
  Managed via Helm Charts for scalability and consistency.

- **Cloud Database**  
  Integrated with Neon Serverless PostgreSQL for persistent storage.

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | Next.js 15+ (App Router), Tailwind CSS |
| Backend | Python FastAPI, SQLModel (ORM) |
| AI / LLM | OpenAI API (GPT-4o) |
| Database | Neon PostgreSQL (Serverless) |
| DevOps | Docker, Kubernetes (K8s), Helm |

---

## 🚀 Phase IV: Kubernetes Deployment (Quick Start)

> **Prerequisites:** Minikube and Helm must be installed.

### 1️⃣ Load Images into Minikube

```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### 2️⃣ Install the Application using Helm

Navigate to the root folder and run:

```bash
helm install todo-app ./todo-chatbot
```

### 3️⃣ Port Forwarding (Access the App)

Open **two separate terminals**:

```bash
# Frontend (http://localhost:3000)
kubectl port-forward svc/todo-app-frontend 3000:3000
```

```bash
# Backend API (http://localhost:8000)
kubectl port-forward svc/todo-app-backend 8000:8000
```

---

## 📂 Project Structure

```plaintext
├── backend/            # FastAPI source code & Dockerfile
├── frontend/           # Next.js source code & Dockerfile
├── todo-chatbot/       # Helm Charts (Templates, Values, Charts)
│   ├── templates/      # K8s manifests (Deployment, Service, HPA)
│   └── values.yaml     # Global configurations
├── README.md           # Project documentation
└── .env.example        # Reference for environment variables
```

---

## 🛡️ Security & Scalability

- **Secrets Management**  
  Sensitive data like `DATABASE_URL` and `OPENAI_API_KEY` are managed via Kubernetes Secrets.

- **Autoscaling (HPA)**  
  Horizontal Pod Autoscaler configured to handle traffic spikes automatically.

- **Resource Limits**  
  CPU and Memory limits defined in Helm templates to ensure cluster stability.

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/api/v1/login` | Get JWT Access Token |
| GET | `/api/v1/todos` | Fetch all todos for logged-in user |
| POST | `/api/v1/chat` | Interact with the AI Chatbot |
| GET | `/health` | Kubernetes Liveness / Readiness probe |

---

## 🎥 Demo & Submission

- **Walkthrough Video:**  [Click here for Demo](https://notebooklm.google.com/notebook/67e60409-d229-4175-8606-b092b840e0d3?artifactId=14c8270c-7e93-488d-acfd-c74948473a0a)
---

## 👨‍💻 Developed By

**Muhammad Suleman**  
GIAIC – 4th Quarter
