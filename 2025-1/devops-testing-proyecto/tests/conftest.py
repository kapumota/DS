# tests/conftest.py
import pytest
from unittest.mock import Mock
from devops_testing.models import User
from devops_testing.repositories import (
    InMemoryUserRepository,
    InMemoryPaymentRepository,
)
from devops_testing.services import PaymentService
from devops_testing.config import Config
from tests.fakes import DummyGateway

#  Fixtures de repositorios y entidades básicas

@pytest.fixture
def user_repo():
    """Repositorio de usuarios (nuevo en cada test)."""
    return InMemoryUserRepository()

@pytest.fixture
def payment_repo():
    """Repositorio de pagos (nuevo en cada test)."""
    return InMemoryPaymentRepository()

@pytest.fixture
def test_user(user_repo):
    """Usuario de prueba inyectado en varios escenarios."""
    user = User(username="kapumota", email="kapumota@example.com")
    user_repo.add(user)
    return user

#  Fakes y servicios
@pytest.fixture
def fake_gateway():
    """Fake simple con Mock de unittest (éxito por defecto)."""
    gw = Mock()
    gw.charge.return_value = True
    return gw


@pytest.fixture
def payment_service(fake_gateway, payment_repo, user_repo):
    """
    Servicio principal construido con DI a partir de otros fixtures.
    Representa la variante 'interface-driven' + 'constructor standard'.
    """
    return PaymentService(fake_gateway, payment_repo, user_repo)

#  Variantes de DI

@pytest.fixture
def payment_service_factory():
    """
    Constructor-like: devuelve una función que fabrica PaymentService
    con un gateway fake parametrizable (Mock) y repos in-memory frescos.
    """
    def _make(gateway_success: bool = True):
        gw = Mock()
        gw.charge.return_value = gateway_success

        user_repo_local = InMemoryUserRepository()
        pay_repo_local = InMemoryPaymentRepository()

        service = PaymentService(gw, pay_repo_local, user_repo_local)
        return service, user_repo_local  # repo para poblar en el test

    return _make


@pytest.fixture
def dummy_gateway():
    """
    Interface-driven fake importado de tests/fakes.py
    Cumple estrictamente la interfaz PaymentGateway.
    """
    return DummyGateway()

#  Fixture-as-config (Config global inyectable)

@pytest.fixture(scope="session")
def app_config():
    """
    Config inmutable disponible en toda la sesión; ejemplo fixture-as-config.
    """
    return Config(currency_default="EUR", retries=1)
