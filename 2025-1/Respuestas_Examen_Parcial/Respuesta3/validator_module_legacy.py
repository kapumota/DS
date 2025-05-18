"""
Implementación legacy que viola intencionalmente varios principios SOLID
y es difícil de probar unitariamente en aislamiento.
"""
import logging
import json
from pathlib import Path
import time # Para simular latencia en configuración externa

class RuleProcessor:
    """Procesa elementos de datos contra una lista de reglas codificada internamente o basada en archivos."""

    def __init__(self):
        # El logger se crea internamente ➜ imposible de intercambiar en pruebas
        self._logger = logging.getLogger("LegacyRuleProcessor")
        self._logger.setLevel(logging.INFO)
        # Evitar añadir múltiples handlers si se instancia varias veces en un mismo run
        if not self._logger.hasHandlers():
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)
        self._logger.info("RuleProcessor Legacy inicializado.")
        # La configuración y las reglas se obtienen directamente ➜ acoplamiento fuerte
        self._config = self._get_external_config()
        self._rules = self._load_rules()

    # Métodos privados auxiliares que atan la clase a implementaciones concretas

    def _load_rules(self) -> list[dict]:
        """Simula la lectura de un archivo rules.conf o recurre a una lista codificada."""
        rules_path = Path("rules.conf")
        if rules_path.exists():
            try:
                self._logger.info("Cargando reglas desde rules.conf...")
                with rules_path.open("r", encoding="utf-8") as fp:
                    return json.load(fp)
            except Exception as exc:
                self._logger.error(f"Error al leer rules.conf: {exc}. Usando reglas de fallback.")
        else:
            self._logger.info("rules.conf no encontrado. Usando reglas de fallback codificadas.")

        # Reglas de fallback codificadas internamente
        return [
            {"id": "LGC001", "description": "Valor debe ser mayor que 10", "condition": "item['value'] > 10"},
            {"id": "LGC002", "description": "Nombre debe ser 'test'", "condition": "item['name'] == 'test'"},
            {"id": "LGC003", "description": "Debe tener 'status' como 'active'", "condition": "item.get('status') == 'active'"}
        ]

    def _get_external_config(self) -> dict:
        """Simula obtener configuración de un servicio remoto que podría fallar o tener latencia."""
        self._logger.info("Obteniendo configuración externa...")
        try:
            # Simular una llamada de red con posible latencia
            time.sleep(0.01) # Pequeña demora para simular E/S
            # En un caso real, esto podría ser una llamada HTTP, consulta a BBDD, etc.
            # config = some_remote_service.get_config()
            # Aquí, simplemente la codificamos:
            return {"threshold": 42, "enable_detailed_logging": True, "version": "1.0-legacy"}
        except Exception as exc:
            self._logger.error(f"No se pudo obtener la configuración externa: {exc}. Usando config por defecto.")
