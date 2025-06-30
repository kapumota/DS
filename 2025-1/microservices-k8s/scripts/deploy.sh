#!/bin/bash
# Ayudante de despliegue: construye imágenes y aplica manifiestos de Kubernetes

# Construye la imagen del servicio de usuarios
docker build -t user-service:latest service-user

# Construye la imagen del servicio de órdenes
docker build -t order-service:latest service-order

# Aplica el despliegue del servicio de usuarios en Kubernetes
kubectl apply -f k8s/user-deployment.yaml

# Aplica el despliegue del servicio de órdenes en Kubernetes
kubectl apply -f k8s/order-deployment.yaml

# Mensaje final indicando que todo se ha desplegado
echo "¡Todos los servicios han sido desplegados!"
