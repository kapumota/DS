"""Pruebas unitarias para el RuleProcessor refactorizado."""
from __future__ import annotations

from typing import Any
import pytest
from types import SimpleNamespace # Para crear objetos Rule en tests

# Importar clases y protocolos del módulo refactorizado y de conftest
from validator_module_refactored import (
    RuleProcessor,
    SafeConditionEvaluator,
    safe_eval as safe_eval_func, # Alias para la función si la tuvieras así
    Rule,
    # Los protocolos pueden no ser necesarios aquí si los fakes los implementan bien
)
from .conftest import ( # Importar fixtures específicos si es necesario o confiar en la auto-importación
    MemoryRuleSource,
    MemoryConfigSource,
    ListCapturingLogger,
    # Los fixtures definidos en conftest.py son generalmente auto-usados por pytest
)


# Las fixtures `refactored_processor`, `list_capturing_logger`, etc., se importan automáticamente desde conftest.py

def test_items_passing_validation(refactored_processor: RuleProcessor):
    """Prueba que los items que cumplen al menos una regla son retornados."""
    data = [
        {"value": 15, "name": "foo"},      # Pasa R001 (value > 10)
        {"value": 5, "name": "ok"},       # Pasa R002 (name == 'ok')
        {"value": 20, "name": "active_item", "status": "is_active_now"} # Pasa R001 y R003
    ]
    result = refactored_processor.process_rules(data)
    assert result == data # Todos deberían pasar
    assert len(result) == 3

def test_items_failing_validation(refactored_processor: RuleProcessor, list_capturing_logger: ListCapturingLogger):
    """Prueba que los items que no cumplen ninguna regla no se retornan y se loguea un error."""
    data = [
        {"value": 5, "name": "bar", "status": "inactive"}, # Falla todas las reglas
    ]
    result = refactored_processor.process_rules(data)
    assert result == []
    assert len(list_capturing_logger.errors) == 1
    assert "FALLO DE VALIDACIÓN REFACTORIZADO" in list_capturing_logger.errors[0]
    assert str(data[0]) in list_capturing_logger.errors[0]

def test_mixed_items_validation(refactored_processor: RuleProcessor, list_capturing_logger: ListCapturingLogger):
    """Prueba una mezcla de items que pasan y fallan."""
    data = [
        {"value": 100, "name": "super_ok", "status": "active"}, # Pasa R001, R002, R003
        {"value": 0, "name": "zero_value"},                     # Falla
    ]
    expected_passed = [data[0]]
    
    result = refactored_processor.process_rules(data)
    
    assert result == expected_passed
    assert len(list_capturing_logger.errors) == 1
    assert str(data[1]) in list_capturing_logger.errors[0]
    # Verificar que el logger info también registró el paso (si está habilitado en config)
    assert any(f"PASÓ la regla R001" in info_msg for info_msg in list_capturing_logger.infos)


def test_empty_data_input(refactored_processor: RuleProcessor, list_capturing_logger: ListCapturingLogger):
    """Prueba que una lista de datos vacía no produce errores y retorna vacío."""
    data: list[dict[str, Any]] = []
    result = refactored_processor.process_rules(data)
    assert result == []
    assert not list_capturing_logger.errors # No debería haber errores de validación

def test_no_rules_provided(sample_config_data: dict[str,Any], safe_evaluator: SafeConditionEvaluator, list_capturing_logger: ListCapturingLogger):
    """Prueba que si no hay reglas, ningún item pasa (a menos que la lógica cambie)."""
    empty_rule_source = MemoryRuleSource([]) # Sin reglas
    config_source = MemoryConfigSource(sample_config_data)
    
    processor = RuleProcessor(empty_rule_source, config_source, safe_evaluator, list_capturing_logger)
    data = [{"value": 100, "name": "item"}]
    
    result = processor.process_rules(data)
    assert result == []
    assert len(list_capturing_logger.errors) == 1 # Debería fallar la validación


# Pruebas de inyección de dependencias y estrategias


class AlwaysTrueEvaluator:
    def evaluate(self, condition_str: str, item: dict[str, Any]) -> bool:
        return True

class AlwaysFalseEvaluator:
    def evaluate(self, condition_str: str, item: dict[str, Any]) -> bool:
        return False

def test_setter_di_for_evaluator(refactored_processor: RuleProcessor, list_capturing_logger: ListCapturingLogger):
    """Prueba la inyección por setter para cambiar la estrategia de evaluación."""
    refactored_processor.set_condition_evaluator(AlwaysTrueEvaluator())
    data = [{"value": -999, "name": "whatever"}] # Debería pasar con AlwaysTrueEvaluator
    
    result = refactored_processor.process_rules(data)
    assert result == data
    assert not list_capturing_logger.errors # No deberían registrarse errores de validación

    list_capturing_logger.reset() # Limpiar logs para la siguiente aserción
    refactored_processor.set_condition_evaluator(AlwaysFalseEvaluator())
    result_false = refactored_processor.process_rules(data)
    assert result_false == []
    assert len(list_capturing_logger.errors) == 1

def test_logger_interaction_with_mock(memory_rule_source: MemoryRuleSource, memory_config_source: MemoryConfigSource, safe_evaluator: SafeConditionEvaluator, mocker: Any):
    """Prueba la interacción con el logger usando pytest-mock (spy)."""
    # Usar un logger mockeado en lugar de ListCapturingLogger para esta prueba específica
    mock_logger = mocker.MagicMock(spec=ListCapturingLogger) # O spec=Logger si tienes un protocolo Logger bien definido
    
    processor = RuleProcessor(memory_rule_source, memory_config_source, safe_evaluator, mock_logger)
    
    failing_item = {"value": 1, "name": "fail_item"}
    data = [failing_item]
    
    processor.process_rules(data)
    
    # Verificar que el método error del logger fue llamado con los argumentos esperados
    mock_logger.error.assert_called_once_with("FALLO DE VALIDACIÓN REFACTORIZADO para el elemento: %s", failing_item)
    mock_logger.info.assert_any_call("Procesamiento refactorizado completado. 0 elementos válidos.")

# Pruebas directas para SafeConditionEvaluator
@pytest.mark.parametrize(
    "condition, item, expected_result",
    [
        ("value > 10", {"value": 15}, True),
        ("value > 10", {"value": 5}, False),
        ("value > 10", {"value": 10}, False),
        ("name == 'test'", {"name": "test"}, True),
        ("name == 'test'", {"name": "Test"}, False), # Sensible a mayúsculas
        ("name == \"test_double_quotes\"", {"name": "test_double_quotes"}, True),
        ("amount < 100", {"amount": 50}, True),
        ("amount < 100", {"amount": 100}, False),
        ("description contains 'active'", {"description": "item is active"}, True),
        ("description contains 'prod'", {"description": "item is active"}, False),
        ("has_key extra_field", {"extra_field": "exists"}, True),
        ("has_key missing_field", {"value": 1}, False),
        # Casos de error o malformados
        ("value >> 10", {"value": 15}, False), # Operador desconocido
        ("name === 'oops'", {"name": "oops"}, False), # Operador desconocido
        ("value > text", {"value": 10}, False), # ValueError en int()
        ("field_not_in_item > 10", {"other_field": 1}, False), # Campo no en item
        ("malformed condition", {}, False), # Condición malformada (pocas partes)
        ("field operator_only", {"field": 1}, False), # Condición malformada (sin valor de comparación)
    ]
)
def test_safe_condition_evaluator_logic(condition: str, item: dict[str,Any], expected_result: bool, list_capturing_logger: ListCapturingLogger):
    """Prueba la lógica de SafeConditionEvaluator con varios casos."""
    evaluator = SafeConditionEvaluator(logger=list_capturing_logger) # Usar logger para verificar warnings/errors si es necesario
    assert evaluator.evaluate(condition, item) == expected_result
    # Podrías añadir aserciones sobre list_capturing_logger.warnings/errors para casos malformados

# Pruebas con @xfail y @skip

@pytest.mark.xfail(reason="Simula un escenario donde el config_source podría fallar en obtener un 'critical_threshold' necesario para una regla futura, aunque no se use ahora.")
def test_missing_critical_threshold_in_config_xfail(memory_rule_source: MemoryRuleSource, safe_evaluator: SafeConditionEvaluator, list_capturing_logger: ListCapturingLogger):
    """
    Prueba un escenario donde la configuración podría estar incompleta.
    Aunque SafeConditionEvaluator no use 'critical_threshold' directamente ahora,
    esta prueba marca una dependencia potencial futura.
    """
    # Configuración que omite un campo 'critical_threshold'
    broken_config_data = {"version": "test-broken-config"} 
    broken_config_source = MemoryConfigSource(broken_config_data)

    # Regla hipotética que podría depender de 'critical_threshold' indirectamente
    # (a través de una lógica más compleja en el evaluador o el procesador)
    # Por ahora, la prueba simplemente se ejecutará y se espera que falle (xfail)
    # si alguna lógica futura intentara acceder a current_config.get('critical_threshold')
    # y no lo manejara adecuadamente.

    processor = RuleProcessor(
        rule_source=memory_rule_source,
        config_source=broken_config_source,
        evaluator=safe_evaluator,
        logger=list_capturing_logger
    )
    data = [{"value": 1, "name": "x"}]
    processor.process_rules(data) # Ejecutar el proceso
    
    # En un caso real, aquí podría haber una aserción que falle si el umbral es crucial.
    # Por ejemplo, si el logger registrara un error específico sobre el umbral faltante.
    # assert "critical_threshold no encontrado" in list_capturing_logger.warnings
    # Como es xfail, no necesitamos que falle activamente AHORA, sino que documentamos
    # una posible fragilidad. Si la prueba PASA inesperadamente, pytest lo reportará como XPASS.
    # Para hacerla fallar explícitamente si se quisiera testear el xfail:
    # if 'critical_threshold' not in broken_config_source.get_config():
    #     pytest.fail("critical_threshold no está en la config, como se esperaba para xfail")


@pytest.mark.skip(reason="Esta prueba requeriría una base de datos real para cargar reglas con dependencias complejas, no disponible en CI/entorno de prueba local.")
def test_complex_rule_dependencies_from_database_skipped(): # noqa: D401
    """Simula una prueba que no se puede ejecutar sin un recurso externo (BBDD)."""
    # Lógica que intentaría conectar a una BBDD y fallaría:
    # db_connector = RealDatabaseConnector("user", "pass", "proddb")
    # rules = db_connector.get_rules_with_dependencies()
    # assert len(rules) > 0
    raise RuntimeError("Esta prueba intentaría acceder a una base de datos real.")