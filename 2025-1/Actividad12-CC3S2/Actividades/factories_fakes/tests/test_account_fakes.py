"""
Casos de prueba TestAccountModel
"""
import pytest
import sys
import os

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db
from models.account import Account, DataValidationError
from factories import AccountFactory

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Configura la base de datos antes de las pruebas"""
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(autouse=True)
def clean_tables():
    """Trunca las tablas antes de cada prueba"""
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

class TestAccountModel:
    """Pruebas para el Modelo Account"""

    def test_crear_todas_las_cuentas(self):
        """Prueba la creación de múltiples Cuentas"""
        for _ in range(10):
            account = AccountFactory()
            account.create()
        assert len(Account.all()) == 10

    def test_crear_una_cuenta(self):
        """Prueba la creación de una Cuenta usando datos conocidos"""
        account = AccountFactory()
        account.create()
        assert len(Account.all()) == 1

    def test_repr(self):
        """Prueba la representación de una cuenta"""
        account = AccountFactory(name="Foo")
        assert str(account) == "<Account 'Foo'>"

    def test_to_dict(self):
        """Prueba la serialización de una cuenta a un diccionario"""
        account = AccountFactory()
        result = account.to_dict()
        assert account.name == result["name"]
        assert account.email == result["email"]
        assert account.phone_number == result["phone_number"]
        assert account.disabled == result["disabled"]
        assert account.date_joined == result["date_joined"]

    def test_from_dict(self):
        """Prueba la deserialización de una cuenta desde un diccionario"""
        data = AccountFactory().to_dict()
        account = Account()
        account.from_dict(data)
        assert account.name == data["name"]
        assert account.email == data["email"]
        assert account.phone_number == data["phone_number"]
        assert account.disabled == data["disabled"]

    def test_actualizar_una_cuenta(self):
        """Prueba la actualización de una Cuenta usando datos conocidos"""
        account = AccountFactory()
        account.create()
        assert account.id is not None
        account.name = "Rumpelstiltskin"
        account.update()
        found = Account.find(account.id)
        assert found.name == account.name

    def test_id_invalido_al_actualizar(self):
        """Prueba la actualización con un ID inválido"""
        account = AccountFactory()
        account.id = None
        with pytest.raises(DataValidationError):
            account.update()

    def test_eliminar_una_cuenta(self):
        """Prueba la eliminación de una Cuenta usando datos conocidos"""
        account = AccountFactory()
        account.create()
        assert len(Account.all()) == 1
        account.delete()
        assert len(Account.all()) == 0
