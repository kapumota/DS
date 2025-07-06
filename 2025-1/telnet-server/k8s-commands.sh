#!/usr/bin/env bash
set -euo pipefail

# 1. Información del cluster
echo "Info del Cluster"
minikube kubectl cluster-info

# 2. Explicación de labels
echo "Explica deployment.metadata.labels"
minikube kubectl -- explain deployment.metadata.labels

# 3. Despliegue de recursos
echo " Aplicando manifiestos"
minikube kubectl -- apply -f kubernetes/

# 4. Inspección de deployments, pods y servicios
echo "Deployment, Pods, Services"
minikube kubectl -- get deployments.apps telnet-server
minikube kubectl -- get pods -l app=telnet-server
minikube kubectl -- get services -l app=telnet-server

# 5. Abre el túnel en background
echo " Empieza el tunel en background"
minikube tunnel & TUNNEL_PID=$!
echo "Tunnel PID: $TUNNEL_PID"

# 6. Verificación de servicios y endpoints
echo " Servicios & endpoints"
minikube kubectl -- get services telnet-server
minikube kubectl -- get endpoints -l app=telnet-server
minikube kubectl -- get pods -l app=telnet-server

# 7. Simula caída de un pod y recuperación
echo "Eliminación Pod"
POD=$(minikube kubectl -- get pods -l app=telnet-server -o jsonpath='{.items[0].metadata.name}')
minikube kubectl -- delete pod "$POD"
minikube kubectl -- get pods -l app=telnet-server

# 8. Escalado del deployment
echo "Despliegue a escala de 3 replicas"
minikube kubectl -- scale deployment telnet-server --replicas=3
minikube kubectl -- get deployments.apps telnet-server

# 9. Logs de los pods
echo " Logs Pod"
FIRST_POD=$(minikube kubectl -- get pods -l app=telnet-server -o name | head -n1 | cut -d'/' -f2)
minikube kubectl -- logs "$FIRST_POD" --all-containers=true --prefix=true

# 10. Cierre del túnel
echo "Fin del tunel"
kill "$TUNNEL_PID" || true