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
        # El logger se crea internamente -> imposible de intercambiar en pruebas
        self._logger = logging.getLogger("LegacyRuleProcessor")
        self._logger.setLevel(logging.INFO)
        # Evitar añadir múltiples handlers si se instancia varias veces en un mismo run
        if not self._logger.hasHandlers():
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)
        self._logger.info("RuleProcessor Legacy inicializado.")

        # La configuración y las reglas se obtienen directamente -> acoplamiento fuerte
        self._config = self._get_external_config()
        self._rules = self._load_rules()


    # Métodos privados auxiliares que atan la clase a implementaciones concretas
    # ---------------------------------------------------------------------

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
            return {"threshold": 0, "enable_detailed_logging": False, "version": "default-legacy"}

    def _evaluate_condition(self, condition_str: str, item: dict) -> bool:
        """
        **ZONA DE PELIGRO LEGACY** – usa `eval()` directamente sobre cadenas entrantes.
        Esto es extremadamente inseguro y propenso a errores.
        """
        try:
            # ADVERTENCIA: 100% inseguro – esta es *exactamente* la forma de NO hacerlo.
            # Se pasa `item` al contexto de eval para que las condiciones puedan acceder a sus claves.
            # Ej: condition_str = "item['value'] > 10 and item['name'].startswith('A')"
            return bool(eval(condition_str, {"__builtins__": {}}, {"item": item})) # noqa: S307
        except Exception as exc:
            self._logger.error(f"Error evaluando condición '{condition_str}' en {item}: {exc}")
            return False
    # API Pública 
    # ------------------------------------------------------------------

    def process_rules(self, data: list[dict]) -> list[dict]:
        """
        Retorna una lista de elementos que satisfacen *al menos una* regla.
        Los elementos que no coinciden se registran como fallos de validación.
        """
        if not isinstance(data, list):
            self._logger.error("La entrada de datos debe ser una lista de diccionarios.")
            return []

        self._logger.info(f"Procesando {len(data)} elementos con {len(self._rules)} reglas.")
        valid_items: list[dict] = []

        for item_index, element in enumerate(data):
            if not isinstance(element, dict):
                self._logger.warning(f"Elemento en índice {item_index} no es un diccionario, saltando: {element}")
                continue

            passed_at_least_one_rule = False
            for rule in self._rules:
                condition = rule.get("condition")
                if not condition:
                    self._logger.warning(f"Regla {rule.get('id', 'Desconocida')} no tiene condición, saltando.")
                    continue

                if self._evaluate_condition(condition, element):
                    passed_at_least_one_rule = True
                    if self._config.get("enable_detailed_logging"):
                        self._logger.info(f"Elemento {element} PASÓ la regla {rule.get('id')}: {rule.get('description')}")
                    break  # Pasa a la siguiente_elemento si una regla se cumple (ANY)

            if passed_at_least_one_rule:
                valid_items.append(element)
            else:
                self._logger.error(f"FALLO DE VALIDACIÓN para el elemento: {element}")

        self._logger.info(f"Procesamiento completado. {len(valid_items)} elementos válidos de {len(data)}.")
        return valid_items

if __name__ == '__main__':
    # Ejemplo de uso del módulo legacy
    # Crear un archivo rules.conf de ejemplo
    example_rules_content = [
        {"id": "CONF001", "description": "Valor debe ser mayor que 50 desde archivo", "condition": "item['value'] > 50"},
        {"id": "CONF002", "description": "Nombre debe ser 'config_test' desde archivo", "condition": "item['name'] == 'config_test'"}
    ]
    try:
        with open("rules.conf", "w", encoding="utf-8") as f:
            json.dump(example_rules_content, f)
    except IOError:
        print("No se pudo crear rules.conf para el ejemplo.")

    processor = RuleProcessor()
    sample_data = [
        {"value": 15, "name": "item1"},               # Pasa LGC001 (value > 10)
        {"value": 5, "name": "test"},                # Pasa LGC002 (name == 'test')
        {"value": 100, "name": "config_test"},       # Si rules.conf existe, pasa CONF001 y CONF002
        {"value": 5, "name": "another"},             # Falla todas las reglas (legacy)
        {"value": 60, "name": "archivo_ok", "status": "active"} # Pasa CONF001 (si existe) o LGC001 y LGC003
    ]
    print(f"Configuración Legacy: {processor._config}")
    print(f"Reglas Legacy: {processor._rules}")
    validated_data = processor.process_rules(sample_data)
    print(f"Datos validados: {validated_data}")

    # Limpiar rules.conf si se creó
    # import os
    # if Path("rules.conf").exists(): os.remove("rules.conf")
