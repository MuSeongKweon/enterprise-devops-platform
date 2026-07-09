# 🚀 Enterprise DevOps Platform

> **Production-oriented cloud-native platform built under real-world resource constraints**  
> AWS EKS · Terraform · ArgoCD · Kubernetes · Python Flask · Redis

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat&logo=argo&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazon-aws&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)

---

## 📌 Problem Statement

Most DevOps tutorials assume unlimited resources. This project asks a harder question:

> **Can a production-grade GitOps pipeline — MSA, event-driven communication, IaC — run reliably on t3.micro ($0.0104/hr)?**

The answer required deliberate trade-offs in architecture, observability, and tooling selection.

---

## 🏗️ Architecture

```
Developer (local)
      │
      │  git push
      ▼
  GitHub (main branch)         ← Single Source of Truth
      │
      │  webhook / polling
      ▼
  ArgoCD (GitOps CD)           ← Drift detection + self-healing
      │
      │  kubectl apply
      ▼
  AWS EKS (Kubernetes Cluster)
  ├── Payment Service (Flask)  ── publishes event ──▶ Redis Pub/Sub
  └── Notification Service (Flask) ◀── subscribes ──── Redis Pub/Sub
```

**Infrastructure Layer (Terraform-managed):**
- VPC + Subnet (public/private isolation)
- EKS Cluster + NodeGroup (t3.micro)
- IAM Roles + Security Groups

---

## ⚙️ Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Infra provisioning | Terraform | Reproducible, version-controlled infra |
| Container orchestration | Kubernetes (EKS) | Industry standard for MSA |
| Continuous deployment | ArgoCD | Git as the only deployment trigger |
| Messaging | Redis Pub/Sub | Lightweight; fits memory constraints |
| Application | Python Flask | Minimal footprint on constrained nodes |

---

## 🧠 Key Engineering Decisions

### 1. GitOps over CI/CD push model
Chose ArgoCD pull-based deployment so Kubernetes state is always reconciled with Git. Any manual `kubectl apply` will be detected and reverted — enforcing config consistency without human discipline.

### 2. Redis Pub/Sub over Kafka
On t3.micro (1 vCPU, 1GB RAM), Kafka's JVM overhead (~512MB baseline) is prohibitive.  
Redis Pub/Sub delivers sub-millisecond latency with ~10MB footprint — the right tool for the constraint.

**Known limitation:** No message persistence. If the notification subscriber is down, events are lost. Documented as a future migration target (→ Kafka).

### 3. Removed Prometheus + Grafana
Monitoring stack consumed more RAM than the application itself, causing OOMKill events on the node.  
Decision: prioritize core service stability. Added structured logging as a lightweight alternative.

> **Takeaway:** Architectural decisions are never tool-agnostic. Resource budget is a first-class constraint.

---

## 🔄 Runtime Flow

```
User action
    │
    ▼
Payment Service  ──[publish: "payment.completed"]──▶  Redis
                                                          │
                                                          ▼
                                              Notification Service
                                              (logs / triggers alert)
```

---

## 🧪 Test Scenario

| Step | Action | Expected Result |
|---|---|---|
| 1 | `POST /pay` to Payment Service | Event published to Redis channel |
| 2 | Redis delivers to Notification subscriber | Notification log appears |
| 3 | `git push` new K8s manifest | ArgoCD detects diff, auto-deploys within ~30s |
| 4 | Manual `kubectl` change to cluster | ArgoCD detects drift, reverts to Git state |

---

## 🚀 Getting Started

### Prerequisites
- AWS CLI configured
- Terraform >= 1.3
- kubectl
- ArgoCD CLI

### 1. Provision Infrastructure
```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

### 2. Connect to EKS
```bash
aws eks update-kubeconfig --region ap-northeast-2 --name <cluster-name>
```

### 3. Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 4. Apply Application Manifests
```bash
kubectl apply -f k8s/
```

---

## 📌 Roadmap

| Priority | Item |
|---|---|
| High | CI pipeline (GitHub Actions) — lint, test, image build |
| High | Replace Redis Pub/Sub with Kafka (message durability) |
| Medium | API Gateway / Ingress controller |
| Medium | Prometheus + Grafana (on higher-resource node) |
| Low | Service Mesh (Istio/Linkerd) for mTLS |

---

## 💡 What This Project Demonstrates

- End-to-end GitOps pipeline design and operation
- MSA deployment on Kubernetes with IaC-managed infrastructure
- Real-world architectural trade-off analysis under hard constraints
- Async event-driven communication pattern (Pub/Sub)
