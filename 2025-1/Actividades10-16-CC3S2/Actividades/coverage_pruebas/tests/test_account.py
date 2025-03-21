import json
import pytest
import sys
import os

# Ajustamos el path para que 'models' sea importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db
from models.account import Account, DataValidationError

# Variable global para almacenar los datos del fixture
ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    db.create_all()   # Crea las tablas según los modelos
    yield
    # Se ejecuta después de todas las pruebas
    db.session.close()


class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos (si fuera necesario limpiar algo adicional)"""
        pass

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        db.session.query(Account).delete()
        db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        db.session.remove()

    ######################################################################
    # Casos de prueba básicos
    ######################################################################

    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        assert len(Account.all()) == len(ACCOUNT_DATA)

    ######################################################################
    #  Nuevos casos de prueba para cobertura
    ######################################################################

    def test_to_dict(self):
        """Probar la serialización de Account a diccionario."""
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()  # Se crea en la BD para tener un 'id'

        result = account.to_dict()
        assert isinstance(result, dict)
        assert result["name"] == data["name"]
        assert result["email"] == data["email"]
        # Chequear que 'id' y 'date_joined' existan en el dict
        assert "id" in result
        assert "date_joined" in result

    def test_from_dict(self):
        """Probar la deserialización de un diccionario a una instancia de Account."""
        data = {
            "name": "Nuevo Usuario",
            "email": "nuevo@example.com",
            "phone_number": "1234567890",
            "disabled": True
        }
        account = Account()  # Instancia vacía
        account.from_dict(data)

        # Verificamos que los atributos hayan sido asignados
        assert account.name == data["name"]
        assert account.email == data["email"]
        assert account.phone_number == data["phone_number"]
        assert account.disabled == data["disabled"]

    def test_update_account_success(self):
        """Probar actualizar una cuenta existente."""
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()  # al crear se asigna un ID en la BD

        # Cambiamos un atributo
        account.name = "Nombre Actualizado"
        account.update()  # Debe funcionar sin error

        # Recuperamos de la BD para verificar cambios
        updated_account = Account.find(account.id)
        assert updated_account.name == "Nombre Actualizado"

    def test_update_account_no_id_error(self):
        """Probar que update lance DataValidationError si no hay ID."""
        # Creamos una cuenta *sin* guardarla en la BD
        account = Account(name="Usuario Sin ID", email="sinid@example.com")

        # update() debería lanzar excepción
        #with pytest.raises(DataValidationError):
        #    account.update()
        with pytest.raises(DataValidationError) as excinfo:
            account.update()
        assert "Actualización llamada con campo ID vacío" in str(excinfo.value)

    def test_delete_account(self):
        """Probar la eliminación de una cuenta existente."""
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()

        assert len(Account.all()) == 1  # Comprobación preliminar
        account.delete()
        assert len(Account.all()) == 0  # Debe haberse eliminado

    def test_find_account_exists(self):
        """Probar que find retorne la cuenta correcta si existe."""
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()

        found_account = Account.find(account.id)
        assert found_account is not None
        assert found_account.id == account.id
        assert found_account.name == account.name

    def test_find_account_not_exists(self):
        """Probar que find devuelva None cuando la cuenta no existe."""
        found_account = Account.find(999999)  # ID que no existe
        assert found_account is None

    # << NUEVO TEST PARA __repr__ >>
    def test_repr_account(self):
        """Probar la salida del método __repr__ de Account."""
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        # No es necesario crear en BD para probar __repr__ (pero se puede si se desea)
        representation = repr(account)
        expected = f"<Account '{data['name']}'>"
        assert representation == expected

