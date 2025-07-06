package telnet

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/mock"
)
// tcpServerMock simula un servidor TCP para pruebas
type tcpServerMock struct {
	mock.Mock
}

// Run es la implementación simulada del método Run del servidor TCP
func (t *tcpServerMock) Run() {
	fmt.Println("Función de notificación de carga simulada")
	t.Called()
}

// TestServerRun verifica que el método Run del servidor TCP sea llamado una vez
func TestServerRun(t *testing.T) {
	// Crear instancia del mock
	tcpServer := new(tcpServerMock)
	// Definir la expectativa: Run debe ser llamado exactamente una vez
	tcpServer.On("Run").Once()
	// Ejecutar el método Run simulado
	tcpServer.Run()
	// Comprobar que se cumplieron las expectativas del mock
	tcpServer.AssertExpectations(t)
}
