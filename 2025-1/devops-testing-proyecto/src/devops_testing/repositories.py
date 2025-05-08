"""Capa de repositorios (abstracciones + implementación in‑memory).

Aplica DIP: las partes altas del sistema dependen de la abstracción Repository, no
de detalles concretos. LSP se cumple al proveer InMemoryUserRepository que mantiene
la misma interfaz pública.
"""

from abc import ABC, abstractmethod
from typing import Protocol, Dict, List
from .models import User, Payment

class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def get(self, username: str) -> User: ...

class PaymentRepository(Protocol):
    def add(self, payment: Payment) -> None: ...
    def list_by_user(self, user_id: str) -> List[Payment]: ...

class InMemoryUserRepository:
    """Implementación simple para demo (cumple UserRepository)."""
    def __init__(self) -> None:
        self._db: Dict[str, User] = {}

    def add(self, user: User) -> None:
        if user.username in self._db:
            raise KeyError("usuario duplicado")
        self._db[user.username] = user

    def get(self, username: str) -> User:
        return self._db[username]

class InMemoryPaymentRepository:
    """Implementación simple para demo."""
    def __init__(self) -> None:
        self._by_user: Dict[str, List[Payment]] = {}

    def add(self, payment: Payment) -> None:
        self._by_user.setdefault(payment.user_id, []).append(payment)

    def list_by_user(self, user_id: str) -> List[Payment]:
        return self._by_user.get(user_id, [])
