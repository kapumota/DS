"""
Implementación refactorizada aplicando principios SOLID y Dependency Injection (DI).
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Iterable, Protocol, runtime_checkable

# Definición de protocolos para las dependencias (Abstracciones)
# ---------------------------------------------------------------------------

@runtime_checkable
class Rule(Protocol):
    """Define la estructura esperada para un objeto de regla."""
    id: str
    condition: str # La condición como cadena, la evaluación se delega.
    description: str | None = None # Opcional

@runtime_checkable
class RuleSource(Protocol):
    """Abstracción para una fuente de reglas. Retorna un iterable de objetos Rule."""
    def get_rules(self) -> Iterable[Rule]:
        ...

@runtime_checkable
class ConfigSource(Protocol):
    """Abstracción para una fuente de configuración. Retorna un diccionario o similar."""
    def get_config(self) -> dict[str, Any]:
        ...

@runtime_checkable
class ConditionEvaluator(Protocol):
    """
    Abstracción para la lógica de evaluación de condiciones.
    Evalúa una `condition` (str) contra un `item` (dict) y retorna True/False.
    """
    def evaluate(self, condition_str: str, item: dict[str, Any]) -> bool:
        ...

@runtime_checkable
class Logger(Protocol):
    """Abstracción para un logger, compatible con logging.Logger."""
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    # Se podrían añadir debug, critical, etc., si fueran necesarios.

# -------------------------------------------------------------------------
# Implementación concreta y segura para ConditionEvaluator (Estrategia)
# ---------------------------------------------------------------------------

class SafeConditionEvaluator:
    """
    Evaluador de condiciones seguro que interpreta un pequeño DSL.
    Nunca usa `eval()`. Puede ser extendido para necesidades más complejas.
    DSL Soportado:
        "<field_name> > <integer_value>"
        "<field_name> == <string_value_quoted_or_not>"
        "<field_name> < <integer_value>"
        "<field_name> contains <string_value>"
        "has_key <field_name>"
    """
    def __init__(self, logger: Logger | None = None):
        self._logger = logger or _NullLogger()

    def evaluate(self, condition_str: str, item: dict[str, Any]) -> bool:
        parts = condition_str.split(maxsplit=2)
        if len(parts) < 2:
            self._logger.warning(f"Condición malformada (pocas partes): '{condition_str}'")
            return False

        field = parts[0]
        operator = parts[1].lower()

        try:
            if operator == "has_key":
                 return field in item

            # Para operadores que necesitan un valor de comparación
            if len(parts) < 3:
                self._logger.warning(f"Condición malformada para operador '{operator}': '{condition_str}'")
                return False
            value_to_compare_str = parts[2]

            # Obtener el valor del item, si no existe, la condición generalmente es falsa
            # a menos que el operador sea específico para existencia (ej. 'is_missing')
            if field not in item:
                # self._logger.debug(f"Campo '{field}' no encontrado en el item para la condición '{condition_str}'")
                return False
            item_value = item[field]

            if operator == ">":
                return item_value > int(value_to_compare_str)
            if operator == "<":
                return item_value < int(value_to_compare_str)
            if operator == "==":
                # Intentar comparar como int si es posible, sino como string
                try:
                    return item_value == int(value_to_compare_str)
                except ValueError:
                     # Quitar comillas si es una cadena
                    return str(item_value) == value_to_compare_str.strip("'\"")
            if operator == "contains":
                return isinstance(item_value, str) and value_to_compare_str.strip("'\"") in item_value
            
            self._logger.warning(f"Operador desconocido '{operator}' en condición: '{condition_str}'")
            return False

        except ValueError: # Error en conversión de tipo, ej. int('abc')
            self._logger.error(f"Error de tipo al evaluar '{condition_str}' en {item}. ¿Comparación de tipos incorrecta?")
            return False
        except Exception as e: # Captura genérica para otros errores inesperados
            self._logger.error(f"Error inesperado al evaluar '{condition_str}' en {item}: {e}")
            return False

# ---------------------------------------------------------------------------
# Implementación de Null Object para Logger (Patrón Null Object)
# ---------------------------------------------------------------------------

class _NullLogger:
    """Logger que descarta todos los mensajes. Usado cuando no se inyecta un logger."""
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: pass
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: pass
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# RuleProcessor Refactorizado
# ---------------------------------------------------------------------------

class RuleProcessor:
    """
    Procesa una colección de `data` contra un conjunto de reglas.
    Todas las colaboraciones externas son inyectadas, haciendo la clase completamente testeable.
    """

    def __init__(
        self,
        rule_source: RuleSource,
        config_source: ConfigSource,
        evaluator: ConditionEvaluator, # Hacerlo no opcional, inyectar SafeConditionEvaluator por defecto si se desea fuera
        logger: Logger | None = None,  # Logger sigue siendo opcional, con fallback a NullLogger
    ) -> None:
        self._rule_source = rule_source
        self._config_source = config_source # Guardar la fuente, no solo el config, por si es dinámico
        self._evaluator = evaluator
        self._logger = logger or _NullLogger() # Late binding para el logger

        # Configuración podría ser cargada aquí o bajo demanda en process_rules si es dinámica
        # self._config = self._config_source.get_config()
        # self._logger.info(f"RuleProcessor Refactorizado inicializado con config: {self._config}")
        self._logger.info("RuleProcessor Refactorizado inicializado.")


    #  DI por constructor (arriba) 

    def set_condition_evaluator(self, evaluator: ConditionEvaluator) -> None: # noqa: D401
        """
        Inyección por Setter: permite cambiar la estrategia de evaluación en tiempo de ejecución.
        """
        self._logger.info(f"Cambiando ConditionEvaluator a: {type(evaluator).__name__}")
        self._evaluator = evaluator

    def set_logger(self, logger: Logger) -> None:
        """Permite cambiar el logger en tiempo de ejecución."""
        self._logger.info(f"Cambiando Logger a: {type(logger).__name__}")
        self._logger = logger

    # --------------------------------------------------------------------
    # API Pública (simple, enfocada en orquestación - SRP respetado)
    # --------------------------------------------------------------------

    def process_rules(self, data: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Retorna una lista de elementos que satisfacen *al menos una* regla.
        """
        current_config = self._config_source.get_config() # Obtener config fresca por si es dinámica
        rules = list(self._rule_source.get_rules()) # Obtener reglas frescas

        self._logger.info(f"Procesando datos con {len(rules)} reglas y config: {current_config.get('version', 'N/A')}")
        
        passed_items: list[dict[str, Any]] = []
        for item_index, item in enumerate(data):
            if not isinstance(item, dict):
                self._logger.warning(f"Elemento en índice {item_index} no es un diccionario, saltando: {item}")
                continue

            passed_at_least_one_rule = False
            for rule in rules:
                if self._evaluator.evaluate(rule.condition, item):
                    passed_at_least_one_rule = True
                    if current_config.get("enable_detailed_logging_refactored", False):
                        self._logger.info(f"Elemento {item} PASÓ la regla {rule.id}: {getattr(rule, 'description', 'N/A')}")
                    break # Pasa al siguiente item

            if passed_at_least_one_rule:
                passed_items.append(item)
            else:
                self._logger.error(f"FALLO DE VALIDACIÓN REFACTORIZADO para el elemento: {item}")
        
        self._logger.info(f"Procesamiento refactorizado completado. {len(passed_items)} elementos válidos.")
        return passed_items

# Ejemplo de una clase de regla concreta si no se usa SimpleNamespace o dicts directamente
# from dataclasses import dataclass
# @dataclass
# class SimpleRule:
# id: str
# condition: str
# description: str | None = None
