package telnet
import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"telnet-server/metrics"
	"time"
)

// TCPServer mantiene la estructura de nuestro servidor TCP
type TCPServer struct {
	addr    string
	server  net.Listener
	metrics *metrics.MetricServer
	logger  *log.Logger
}

// New crea un nuevo servidor Telnet
func New(addr string, metrics *metrics.MetricServer, logger *log.Logger) *TCPServer {
	return &TCPServer{addr: addr, metrics: metrics, logger: logger}
}

// Run inicia el servidor TCP
func (t *TCPServer) Run() {
	var err error
	// Abrir escucha TCP en la dirección indicada
	t.server, err = net.Listen("tcp", t.addr)
	defer t.Close()

	if err != nil {
		t.logger.Printf("Error al crear el listener en el puerto %s: %v", t.addr, err)
		os.Exit(1)
	}

	t.logger.Printf("telnet-server escuchando en %s\n", t.server.Addr())

	for {
		// Aceptar nuevas conexiones
		conn, err := t.server.Accept()
		if err != nil {
			err = errors.New("no se pudo aceptar la conexión")
			t.logger.Println(err)
			t.metrics.IncrementConnectionErrors()
			continue
		}
		if conn == nil {
			err = errors.New("no se pudo crear la conexión")
			t.logger.Println(err)
			t.metrics.IncrementConnectionErrors()
			continue
		}
		// Enviar banner de bienvenida
		conn.Write([]byte(banner() + "\n"))
		// Manejar la conexión en un goroutine separado
		go t.handleConnections(conn)
	}
}

// Close cierra el servidor TCP
func (t *TCPServer) Close() (err error) {
	return t.server.Close()
}

// handleConnections gestiona las solicitudes entrantes
func (t *TCPServer) handleConnections(conn net.Conn) {
	defer conn.Close()

	reader := bufio.NewReader(conn)

	// Obtener IP de origen
	srcIP := conn.RemoteAddr().(*net.TCPAddr).IP.String()
	t.logger.Printf("[IP=%s] Nueva sesión", srcIP)

	// Incrementar métricas
	t.metrics.IncrementConnectionsProcessed()
	t.metrics.IncrementActiveConnections()

	for {
		// Mostrar prompt
		conn.Write([]byte(">"))

		// Leer datos hasta salto de línea
		bytes, err := reader.ReadBytes(byte('\n'))
		if err != nil {
			if err != io.EOF {
				t.logger.Println("Error al leer datos:", err)
			}
			// Actualizar métricas y cerrar
			t.metrics.IncrementConnectionErrors()
			t.metrics.DecrementActiveConnections()
			return
		}

		// Procesar comando del cliente
		cmd := strings.TrimRight(string(bytes), "\r\n")
		switch cmd {
		case "quit", "q":
			// Comando de salida
			conn.Write([]byte("¡Hasta luego!\n"))
			t.logger.Printf("[IP=%s] Usuario cerró sesión", srcIP)
			t.metrics.DecrementActiveConnections()
			return
		case "date", "d":
			// Mostrar fecha y hora actual con formato y colores ANSI
			const layout = "Mon Jan 2 15:04:05 -0700 MST 2006"
			s := "\x1b[44;37;1m" + time.Now().Format(layout) + "\033[0m"
			conn.Write([]byte(s + "\n"))
		case "yell for sysop", "y":
			// Comando de llamada al sysop
			conn.Write([]byte("El sysop estará contigo en breve\n"))
		case "dftd":
			// Comando oculto
			conn.Write([]byte("¡Has desbloqueado el modo Dios!\n"))
		case "l", "list":
			// Mostrar lista de archivos con arte ASCII
			header := `
███████ ██ ██      ███████ ███████ 
██      ██ ██      ██      ██      
█████   ██ ██      █████   ███████ 
██      ██ ██      ██           ██ 
██      ██ ███████ ███████ ███████ 
                                   `

			fileList := `
        Nombre de archivo  Tamaño   Fecha   Descripción
------------------------------------------------------------------------------
    Ghoulbutsers         170K     1984    Basado en la película blockbuster.`

			conn.Write([]byte("\n" + header + "\n"))
			conn.Write([]byte(fileList + "\n"))
		case "w", "weather":
			// Simulación de clima con arte ASCII
			header := `
            ^^                   @@@@@@@@@
       ^^       ^^            @@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@              ^^
                           @@@@@@@@@@@@@@@@@@@@
 ~~~~ ~~ ~~~~~ ~~~~~~~~ ~~ &&&&&&&&&&&&&&&&&&&&&&&& ~~~~~~~ ~~~~~~~~~~~ ~~~
 ~         ~~   ~  ~       ~~~~~~~~~~~~~~~~~~~~ ~       ~~     ~~ ~
   ~      ~~      ~~ ~~ ~~  ~~~~~~~~~~~~~ ~~~~  ~     ~~~    ~ ~~~  ~ ~~
   ~  ~~     ~         ~      ~~~~~~  ~~ ~~~       ~~ ~ ~~  ~~ ~
 ~  ~       ~ ~      ~           ~~ ~~~~~~  ~      ~~  ~             ~~
       ~             ~        ~      ~      ~~   ~             ~

-------------------------------------------------------------------------

`
			// Pedir ciudad al usuario
			conn.Write([]byte("Ingresa la ciudad: "))
			reply := make([]byte, 1024)
			_, _ = conn.Read(reply)
			msg := fmt.Sprintf("El clima está soleado en %s", reply)
			conn.Write([]byte(msg + "\n"))
			conn.Write([]byte("\n" + header + "\n"))
		case "help", "?":
			// Mostrar ayuda de comandos
			command := "Ayuda de comandos:\n1) (q)uit -- salir\n2) (d)ate -- fecha y hora actual\n3) (y)ell for sysop -- llamar al sysop\n4) (?) help -- mostrar esta ayuda"
			conn.Write([]byte(command + "\n"))
		default:
			// Eco de comando desconocido
			newmessage := "comando desconocido: " + cmd
			// Incrementar métrica de comandos no reconocidos
			t.metrics.IncrementUnknownCommands(cmd)
			conn.Write([]byte(newmessage + "\n"))
		}

		// Registrar en bitácora el comando recibido
		t.logger.Printf("[IP=%s] Comando solicitado: %s", srcIP, bytes)
	}
}
