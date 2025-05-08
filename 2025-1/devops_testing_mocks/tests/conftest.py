import pytest
from unittest.mock import Mock
from decimal import Decimal
from devops_testing.models import User
from devops_testing.repositories import InMemoryUserRepository, InMemoryPaymentRepository
from devops_testing.gateway import DummyGateway
from devops_testing.services import PaymentService

# Fixtures 
@pytest.fixture
def user_repo():
    return InMemoryUserRepository()

@pytest.fixture
def payment_repo():
    return InMemoryPaymentRepository()

@pytest.fixture
def test_user(user_repo):
    user = User(username="kapumota", email="kapumota@example.com")
    user.credit(Decimal("100"))
    user_repo.add(user)
    return user

@pytest.fixture
def fake_gateway_success():
    return DummyGateway(should_succeed=True)

@pytest.fixture
def fake_gateway_fail():
    return DummyGateway(should_succeed=False)

@pytest.fixture
def payment_service(fake_gateway_success, payment_repo, user_repo):
    return PaymentService(fake_gateway_success, payment_repo, user_repo)
