.PHONY: build run stop clean publish

# Nombre de la imagen del microservicio
IMAGE_NAME := ejemplo-microservice
# Versión de la imagen (se puede sobreescribir al invocar: make build IMAGE_TAG=1.2.3)
IMAGE_TAG ?= 0.1.0
# Registro remoto para publicación (por defecto GitHub Container Registry)
REGISTRY ?= ghcr.io/your-org

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

run:
	docker run -d \
		-p 80:80 \
		--name $(IMAGE_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)

stop:
	docker stop $(IMAGE_NAME) && docker rm $(IMAGE_NAME)

clean:
	docker image prune -f

publish:
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
