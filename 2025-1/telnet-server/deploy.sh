#!/usr/bin/env bash
set -euo pipefail

# 1. Inicia Minikube con driver Docker
minikube start --driver=docker

# 2. Apunta Docker al daemon de Minikube
eval "$(minikube -p minikube docker-env --shell bash)"

# 3. Comprueba versiones
docker version

# 4. Construye la imagen
docker build -t dftd/telnet-server:v1 .

# 5. Lista la imagen
docker image ls dftd/telnet-server:v1

# 6. (Versión 2) Arranca el contenedor exponiendo en todas las interfaces
docker run -p 0.0.0.0:2323:2323 -d \
  --name telnet-server \
  dftd/telnet-server:v1

# 7. Lista contenedores
docker container ls -f name=telnet-server

# 8. Para, inspecciona y borra el contenedor
docker container stop telnet-server
docker inspect telnet-server
docker container rm telnet-server

# 9. Info interna del contenedor
docker run -p 2323:2323 -d --name telnet-server dftd/telnet-server:v1
docker exec telnet-server env
docker exec -it telnet-server /bin/sh

# 10. Historial y métricas
docker history dftd/telnet-server:v1
docker stats --no-stream telnet-server

# 11. Prueba de conexión
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"
echo "Telnet a localhost:"
telnet localhost 2323
echo "Telnet a Minikube IP:"
telnet $MINIKUBE_IP 2323

# 12. Logs
docker logs telnet-server
