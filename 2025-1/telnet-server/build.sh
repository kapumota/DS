#!/usr/bin/env bash
set -e

echo "Corriendo pruebas..."

go test ./... -v # todos los test

echo "Building $IMAGE"
docker build -t $IMAGE .

if [[ -v $PUSH_IMAGE ]]; then 
    docker push $IMAGE
fi

