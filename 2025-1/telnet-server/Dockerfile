# Etapa de compilación
FROM golang:alpine AS build-env
ADD . /
RUN cd / && go build -o telnet-server

# Etapa final
FROM alpine:latest AS final
WORKDIR /app

# Puerto para el servidor Telnet (variable de entorno)
ENV TELNET_PORT 2323
# Puerto para el servidor de métricas (variable de entorno)
ENV METRIC_PORT 9000

# Copiar el binario compilado desde la etapa de compilación
COPY --from=build-env /telnet-server /app/

# Punto de entrada al contenedor
ENTRYPOINT ["./telnet-server"]
