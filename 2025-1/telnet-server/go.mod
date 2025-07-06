// Módulo principal
module telnet-server

// Versión de Go que utiliza este módulo
go 1.17

// Dependencias directas
require (
    github.com/prometheus/client_golang v1.6.0    // cliente de Prometheus para Go
    github.com/stretchr/testify       v1.4.0    // librería de aserciones y utilidades para tests
)

// Dependencias indirectas (requeridas por las dependencias directas)
require (
    github.com/beorn7/perks                            v1.0.1    // indirecto: utilidades internas de Prometheus
    github.com/cespare/xxhash/v2                       v2.1.1    // indirecto: implementación de xxHash
    github.com/davecgh/go-spew                         v1.1.1    // indirecto: impresión detallada de estructuras Go
    github.com/golang/protobuf                         v1.4.0    // indirecto: soporte legacy de Protobuf
    github.com/matttproud/golang_protobuf_extensions   v1.0.1    // indirecto: extensiones para Protobuf
    github.com/pmezard/go-difflib                      v1.0.0    // indirecto: cálculo de diferencias entre textos
    github.com/prometheus/client_model                 v0.2.0    // indirecto: modelos de datos Prometheus
    github.com/prometheus/common                       v0.9.1    // indirecto: utilidades comunes de Prometheus
    github.com/prometheus/procfs                       v0.0.11   // indirecto: lectura de `/proc` en Linux
    github.com/stretchr/objx                            v0.1.1    // indirecto: manipulación de objetos JSON
    golang.org/x/sys                                   v0.0.0-20200420163511-1957bb5e6d1f // indirecto: llamadas al sistema específicas de plataforma
    google.golang.org/protobuf                         v1.21.0   // indirecto: API moderna de Protobuf
    gopkg.in/yaml.v2                                    v2.2.8    // indirecto: procesamiento de YAML
)
