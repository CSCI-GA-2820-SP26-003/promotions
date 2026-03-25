# Kubernetes Local Setup

## Prerequisites
- Docker Desktop installed and running
- Minikube installed
- kubectl installed

## Setup

### 1. Start the local Kubernetes cluster
```bash
minikube start --driver=docker
```

### 2. Verify the cluster is running
```bash
kubectl get nodes
```

### 3. Verify kubectl can connect
```bash
kubectl cluster-info
```

### 4. Verify all pods are running
```bash
kubectl get pods --all-namespaces
```

## Acceptance Criteria Validation
- Local Kubernetes cluster created with Minikube
- Cluster accessible using kubectl
- Development environment supports Kubernetes commands