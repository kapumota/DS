#!/usr/bin/env bash
set -euo pipefail

echo "Services: telnet-server"
minikube kubectl -- get services telnet-server

echo; echo "Historia Rollout: telnet-server"
minikube kubectl -- rollout history deployment telnet-server

echo; echo "A revision 1"
minikube kubectl -- rollout undo deployment telnet-server --to-revision=1

echo; echo " Pods despues de undo"
minikube kubectl -- get pods
