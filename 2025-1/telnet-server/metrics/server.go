package metrics

import (
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	// connectionsProcessed cuenta el número total de conexiones procesadas
	connectionsProcessed = promauto.NewCounter(prometheus.CounterOpts{
		Name: "telnet_server_connection_total",
		Help: "El número total de conexiones",
	})
	// connectionErrors cuenta el número total de errores de conexión
	connectionErrors = promauto.NewCounter(prometheus.CounterOpts{
		Name: "telnet_server_connection_errors_total",
		Help: "El número total de errores",
	})
	// unknownCommands cuenta el número total de comandos desconocidos ingresados
	unknownCommands = promauto.NewCounter(prometheus.CounterOpts{
		Name: "telnet_server_unknown_commands_total",
		Help: "El número total de comandos desconocidos ingresados",
	})

	// connectionsActive representa el número de conexiones activas
	connectionsActive = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "telnet_server_active_connections",
		Help: "El número de conexiones activas",
	})
)

// MetricServer mantiene el estado de nuestro servidor de métricas Prometheus
type MetricServer struct {
	port     string
	endPoint string
	logger   *log.Logger
}

// New crea un nuevo servidor de métricas
func New(port string, logger *log.Logger) *MetricServer {
	return &MetricServer{port: port, endPoint: "/metrics", logger: logger}
}

// ListenAndServeMetrics inicia el servidor HTTP para exponer las métricas
func (m *MetricServer) ListenAndServeMetrics() {
	http.Handle(m.endPoint, promhttp.Handler())
	m.logger.Printf("Endpoint de métricas escuchando en %s\n", m.port)
	http.ListenAndServe(m.port, nil)
}

// IncrementConnectionErrors incrementa en 1 el contador de errores de conexión
func (m *MetricServer) IncrementConnectionErrors() {
	connectionErrors.Inc()
}

// IncrementConnectionsProcessed incrementa en 1 el contador de conexiones procesadas
func (m *MetricServer) IncrementConnectionsProcessed() {
	connectionsProcessed.Inc()
}

// IncrementUnknownCommands incrementa en 1 el contador de comandos desconocidos
func (m *MetricServer) IncrementUnknownCommands(cmd string) {
	unknownCommands.Inc()
}

// IncrementActiveConnections incrementa en 1 la métrica de conexiones activas
func (m *MetricServer) IncrementActiveConnections() {
	connectionsActive.Inc()
}

// DecrementActiveConnections decrementa en 1 la métrica de conexiones activas
func (m *MetricServer) DecrementActiveConnections() {
	connectionsActive.Dec()
}
