#!/bin/bash
# Script para inicializar Minikube y desplegar servicios

echo "Iniciando Minikube..."
minikube start --driver=docker

echo "Construyendo imágenes Docker..."
# Configura el entorno Docker para usar el daemon de Minikube
eval "$(minikube -p minikube docker-env --shell bash)"
docker build -t user-service:latest service-user
docker build -t order-service:latest service-order

echo "Desplegando en Kubernetes..."
# Aplica las configuraciones de despliegue
kubectl apply -f k8s/user-deployment.yaml
kubectl apply -f k8s/order-deployment.yaml

echo "Servicios desplegados:"
# Muestra los servicios en el clúster
kubectl get svc
