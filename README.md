# 🚀 Enterprise DevOps Platform (Lightweight MSA + GitOps)

## 📌 Overview

This project demonstrates a lightweight, production-oriented DevOps platform built on AWS EKS, implementing:

- Microservices Architecture (MSA)
- Event-driven communication (Redis Pub/Sub)
- GitOps-based continuous deployment (ArgoCD)
- Infrastructure as Code (Terraform)

The goal is to design and operate a real-world cloud-native system under constrained resources (t3.micro), focusing on architectural decisions and trade-offs.

---

## 🧱 Architecture

GitHub (main)
↓
ArgoCD (GitOps CD)
↓
Kubernetes (EKS)
├ Payment Service (Publisher)
├ Notification Service (Subscriber)
└ Redis (Message Broker)

---

## ⚙️ Tech Stack

### Infrastructure
- AWS EKS
- Terraform (VPC, Subnet, EKS, NodeGroup)

### Container & Orchestration
- Docker
- Kubernetes

### DevOps / CD
- ArgoCD (GitOps-based deployment)

### Application
- Python (Flask-based microservices)
- Redis (Pub/Sub messaging)

---

## 🧠 Key Concepts

### 1. Microservices Architecture (MSA)

- Services are independently deployed
- Loose coupling via event-driven communication
- Scalable and extensible system design

---

### 2. Event-Driven Architecture

Payment Service → Redis → Notification Service
- Payment service publishes events
- Notification service subscribes and reacts
- Asynchronous, decoupled communication

---

### 3. GitOps Deployment

- GitHub = Single Source of Truth
- ArgoCD continuously syncs Git → Kubernetes
git push → ArgoCD → automatic deployment
- No manual `kubectl apply`
- Drift detection & self-healing

---

## 🔄 System Workflow

1. Developer updates code locally
2. Push to GitHub (main branch)
3. ArgoCD detects changes
4. Kubernetes resources automatically updated
5. Services deployed

Runtime flow:
User action → Payment Service → Redis → Notification Service

---

## 🧪 Test Scenario (Realistic)

### ✅ Scenario: Payment Event

1. User triggers payment
2. Payment service publishes event: “payment completed”
3. Redis delivers event
4. Notification service receives event
5. Notification is generated

---

## ⚠️ Design Trade-offs

### Redis Pub/Sub

Pros
- Lightweight
- Fast (in-memory)
- Simple to implement

Cons
- No message persistence
- No replay capability
- Message loss if subscriber is down

⸻

### Monitoring Decision

Initially, Prometheus + Grafana was deployed.

However:
- t3.micro (1GB RAM) environment caused resource exhaustion
- Monitoring stack consumed more resources than application

👉 Decision:
- Removed monitoring stack
- Focused on core service stability and GitOps pipeline

⸻

## 💡 Key Learnings
- GitOps enables fully automated deployment without manual intervention
- Infrastructure scaling is critical when adding observability components
- Redis Pub/Sub is effective for lightweight event-driven systems
- Resource constraints directly impact architectural decisions

⸻

## 📌 Future Improvements
- Replace Redis Pub/Sub with Kafka (durable messaging)
- Add Prometheus in higher-resource environment
- Implement API Gateway / Service Mesh
- Introduce CI pipeline (GitHub Actions)

⸻

## 🧠 What This Project Demonstrates
- End-to-end DevOps pipeline design
- Kubernetes-based MSA deployment
- GitOps workflow using ArgoCD
- Real-world trade-off decision making under constraints

⸻

## 🔥 Summary

This project implements a cloud-native DevOps platform combining:
- MSA + Event-driven architecture
- GitOps-based continuous delivery
- Infrastructure automation

→ Designed and operated with real-world constraints in mind.
