
"""Modelos de dominio"""
from dataclasses import dataclass, field
from uuid import uuid4
from decimal import Decimal

@dataclass
class User:
    username: str
    email: str
    id: str = field(default_factory=lambda: str(uuid4()))
    balance: Decimal = Decimal("0")

    def credit(self, amount: Decimal):
        self.balance += amount

    def debit(self, amount: Decimal):
        if amount > self.balance:
            raise ValueError("Fondos insuficientes")
        self.balance -= amount
