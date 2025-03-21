"""
Clase Account
"""
import logging
from sqlalchemy.sql import func
from models import db

logger = logging.getLogger()


class DataValidationError(Exception):
    """Utilizada para errores de validación de datos al deserializar"""


class Account(db.Model):
    """Clase que representa una Cuenta"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(32), nullable=True)
    disabled = db.Column(db.Boolean(), nullable=False, default=False)
    date_joined = db.Column(db.Date, nullable=False, server_default=func.now())

    def __repr__(self):
        return '<Account %r>' % self.name

    def to_dict(self) -> dict:
        """Serializa la clase como un diccionario"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def from_dict(self, data: dict) -> None:
        """Establece atributos desde un diccionario"""
        for key, value in data.items():
            setattr(self, key, value)

    def create(self):
        """Crea una cuenta en la base de datos"""
        logger.info("Creando %s", self.name)
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Actualiza una cuenta en la base de datos"""
        logger.info("Guardando %s", self.name)
        if not self.id:
            raise DataValidationError("Se llamó a update sin un ID")
        db.session.commit()

    def delete(self):
        """Elimina una cuenta de la base de datos"""
        logger.info("Eliminando %s", self.name)
        db.session.delete(self)
        db.session.commit()

    ##################################################
    # Métodos de clase
    ##################################################

    @classmethod
    def all(cls) -> list:
        """Devuelve todas las cuentas en la base de datos"""
        logger.info("Procesando todas las cuentas")
        return cls.query.all()

    @classmethod
    def find(cls, account_id: int):
        """Encuentra una cuenta por su ID
        :param account_id: el id de la cuenta que se quiere encontrar
        :type account_id: int
        :return: una instancia con el account_id o None si no se encuentra
        :rtype: Account
        """
        logger.info("Buscando cuenta con id %s ...", account_id)
        return cls.query.get(account_id)
