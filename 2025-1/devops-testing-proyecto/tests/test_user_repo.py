"""Pruebas unitarias para UserRepository (SRP: cada test => único camino feliz/fallo)."""

import pytest
from devops_testing.models import User
from devops_testing.repositories import InMemoryUserRepository

def test_add_and_get_user():
    repo = InMemoryUserRepository()
    user = User(username="kapu", email="kapu@example.com")
    repo.add(user)
    assert repo.get("kapu") == user

def test_add_duplicate_user_raises():
    repo = InMemoryUserRepository()
    user = User(username="kapu", email="kapu@example.com")
    repo.add(user)
    with pytest.raises(KeyError):
        repo.add(user)
