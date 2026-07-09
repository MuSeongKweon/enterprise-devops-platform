# ArgoCD GitOps Configuration

This directory contains ArgoCD Application manifests for GitOps-based Kubernetes deployment.

## Architecture

```
Git push → ArgoCD detects diff → Auto sync → K8s cluster updated
```

ArgoCD continuously monitors this repository. When a manifest in `k8s/` changes, ArgoCD automatically reconciles the cluster state to match Git.

## Applications

| App | Manifest | Target Namespace |
|-----|----------|-----------------|
| payment-service | `payment-app.yaml` | default |
| notification-service | `notification-app.yaml` | default |

## Setup

### 1. Install ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Apply Application manifests

```bash
kubectl apply -f argocd/payment-app.yaml
kubectl apply -f argocd/notification-app.yaml
```

### 3. Verify sync status

```bash
kubectl get applications -n argocd
```

## Sync Policy

Both applications are configured with:

- **automated.prune: true** — removes K8s resources deleted from Git
- **automated.selfHeal: true** — reverts manual changes made directly to the cluster
- **CreateNamespace: true** — auto-creates target namespace if absent

## Testing GitOps

To verify automated sync, update `replicas` in any manifest under `k8s/` and push to `main`:

```bash
# Edit k8s/payment_deployment.yaml: replicas: 1 → replicas: 3
git add k8s/payment_deployment.yaml
git commit -m "scale: increase payment-service replicas to 3"
git push origin main
# ArgoCD detects the diff within ~3 minutes and applies automatically
```
