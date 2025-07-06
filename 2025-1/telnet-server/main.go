package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	"telnet-server/metrics"
	"telnet-server/telnet"
)

var (
	// logger para la salida estándar con prefijo y marcas de tiempo
	logger = log.New(os.Stdout, "servidor-telnet: ", log.LstdFlags)
)

// telnetServerPort obtiene el puerto para el servidor Telnet desde la variable de entorno TELNET_PORT
// o usa el valor por defecto "2323"
func telnetServerPort() string {
	port, ok := os.LookupEnv("TELNET_PORT")
	if !ok {
		port = "2323"
	}
	return fmt.Sprintf(":%s", port)
}

// metricServerPort obtiene el puerto para el servidor de métricas desde la variable de entorno METRIC_PORT
// o usa el valor por defecto "9000"
func metricServerPort() string {
	port, ok := os.LookupEnv("METRIC_PORT")
	if !ok {
		port = "9000"
	}
	return fmt.Sprintf(":%s", port)
}

func main() {
	var info bool
	// bandera -i para imprimir los valores de entorno y salir
	flag.BoolVar(&info, "i", false, "Imprimir puertos desde ENV")
	flag.Parse()

	if info {
		fmt.Printf("Puerto Telnet: %s\nPuerto de métricas: %s\n", telnetServerPort(), metricServerPort())
		os.Exit(0)
	}

	// iniciar servidor de métricas Prometheus
	metricServer := metrics.New(metricServerPort(), logger)
	go metricServer.ListenAndServeMetrics()

	// iniciar servidor Telnet
	telnetServer := telnet.New(telnetServerPort(), metricServer, logger)
	telnetServer.Run()
}
