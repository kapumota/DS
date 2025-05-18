"""Fixtures de Pytest compartidos para la suite de pruebas de RuleProcessor."""
from __future__ import annotations

import logging
from types import SimpleNamespace # Usado para crear objetos 'Rule' simples
from typing import Any, Iterable, List, Dict # Corregido List y Dict a minúsculas

import pytest

# Importar clases y protocolos del módulo refactorizado
from validator_module_refactored import (
    Rule,
    RuleSource,
    ConfigSource,
    ConditionEvaluator,
    Logger,
    RuleProcessor,
    SafeConditionEvaluator, # Importar la implementación por defecto
    _NullLogger
)


# Implementaciones Fake/Stub usadas como dependencias en las pruebas


class MemoryRuleSource:
    """Fuente de reglas en memoria para pruebas."""
    def __init__(self, rules_data: list[dict[str, Any]]):
        # Convertir dicts a objetos que implementan el protocolo Rule (usando SimpleNamespace)
        self._rules = [
            SimpleNamespace(
                id=d.get("id", f"rule_{i}"),
                condition=d.get("condition", ""),
                description=d.get("description")
            ) for i, d in enumerate(rules_data)
        ]

    def get_rules(self) -> Iterable[Rule]:
        return self._rules

class MemoryConfigSource:
    """Fuente de configuración en memoria para pruebas."""
    def __init__(self, config_data: dict[str, Any]):
        self._config = config_data

    def get_config(self) -> dict[str, Any]:
        return self._config

class ListCapturingLogger:
    """Logger que captura mensajes en listas internas para aserciones."""
    def __init__(self):
        self.infos: list[str] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def _format_msg(self, msg: str, *args: Any) -> str:
        # logging.Logger hace esto internamente, lo simulamos
        return msg % args if args else msg

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.infos.append(self._format_msg(msg, *args))

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.errors.append(self._format_msg(msg, *args))

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.warnings.append(self._format_msg(msg, *args))

    def reset(self) -> None:
        self.infos.clear()
        self.errors.clear()
        self.warnings.clear()



# Fixtures de Pytest

@pytest.fixture
def sample_rules_data() -> list[dict[str, Any]]:
    """Datos de reglas de ejemplo."""
    return [
        {"id": "R001", "condition": "value > 10", "description": "Valor mayor que 10"},
        {"id": "R002", "condition": "name == 'ok'", "description": "Nombre es 'ok'"},
        {"id": "R003", "condition": "status contains 'active'", "description": "Estado contiene 'active'"}
    ]

@pytest.fixture
def sample_config_data() -> dict[str, Any]:
    """Datos de configuración de ejemplo."""
    return {"threshold": 10, "version": "test-1.0", "enable_detailed_logging_refactored": True}

@pytest.fixture
def memory_rule_source(sample_rules_data: list[dict[str, Any]]) -> RuleSource:
    """Fixture para una MemoryRuleSource preconfigurada."""
    return MemoryRuleSource(sample_rules_data)

@pytest.fixture
def memory_config_source(sample_config_data: dict[str, Any]) -> ConfigSource:
    """Fixture para una MemoryConfigSource preconfigurada."""
    return MemoryConfigSource(sample_config_data)

@pytest.fixture
def list_capturing_logger() -> ListCapturingLogger:
    """Fixture para el ListCapturingLogger."""
    return ListCapturingLogger()

@pytest.fixture
def safe_evaluator(list_capturing_logger: ListCapturingLogger) -> ConditionEvaluator:
    """Fixture para el SafeConditionEvaluator (estrategia por defecto)."""
    return SafeConditionEvaluator(logger=list_capturing_logger)

@pytest.fixture
def refactored_processor(
    memory_rule_source: RuleSource,
    memory_config_source: ConfigSource,
    safe_evaluator: ConditionEvaluator,
    list_capturing_logger: ListCapturingLogger
) -> RuleProcessor:
    """
    Fixture para un RuleProcessor refactorizado con dependencias inyectadas (constructor DI).
    """
    return RuleProcessor(
        rule_source=memory_rule_source,
        config_source=memory_config_source,
        evaluator=safe_evaluator,
        logger=list_capturing_logger,
    )

@pytest.fixture
def null_logger() -> Logger:
    return _NullLogger()