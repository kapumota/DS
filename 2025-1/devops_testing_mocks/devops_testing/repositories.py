"""Repositorios en memoria para pruebas"""
from typing import Dict
from .models import User
from uuid import uuid4
from decimal import Decimal

class UserRepositoryInterface:
    def add(self, user: User): ...
    def get(self, username: str) -> User: ...

class PaymentRepositoryInterface:
    def record(self, user_id: str, amount): ...

class InMemoryUserRepository(UserRepositoryInterface):
    def __init__(self):
        self._store: Dict[str, User] = {}

    def add(self, user: User):
        if user.username in self._store:
            raise KeyError(user.username)
        self._store[user.username] = user

    def get(self, username: str) -> User:
        return self._store[username]

class InMemoryPaymentRepository(PaymentRepositoryInterface):
    def __init__(self):
        self._log = []

    def record(self, user_id: str, amount):
        self._log.append((user_id, amount))

    @property
    def log(self):
        return list(self._log)

