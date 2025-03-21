"""
Clase Account
"""
import logging
from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.sql import func
from models import db

logger = logging.getLogger()


class DataValidationError(Exception):
    """Se utiliza para errores de validación de datos al deserializar"""


class Account(db.Model):
    """Clase que representa una Cuenta"""

    __tablename__ = 'accounts'  # Asegúrate de definir el nombre de la tabla

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    phone_number = Column(String(32), nullable=True)
    disabled = Column(Boolean(), nullable=False, default=False)
    date_joined = Column(Date, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<Account '{self.name}'>"

    def to_dict(self) -> dict:
        """Serializa la clase como un diccionario"""
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data = {}
        for c in self.__table__.columns:
            data[c.name] = getattr(self, c.name)
        return data

    def from_dict(self, data: dict) -> None:
        """Establece los atributos desde un diccionario"""
        for key, value in data.items():
            setattr(self, key, value)

    def create(self):
        """Crea una Cuenta en la base de datos"""
        logger.info(f"Creando {self.name}")
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Actualiza una cuenta en la base de datos"""
        logger.info(f"Guardando {self.name}")
        if not self.id:
            raise DataValidationError("Actualización llamada con campo ID vacío")
        else:
            db.session.commit()
            return self


    def delete(self):
        """Elimina una Cuenta del almacén de datos"""
        logger.info(f"Eliminando {self.name}")
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls) -> list:
        """Devuelve todas las Cuentas en la base de datos"""
        logger.info("Procesando todas las Cuentas")
        stmt = db.select(cls)
        return db.session.execute(stmt).scalars().all()

    @classmethod
    def find(cls, account_id: int):
        """Encuentra una Cuenta por su ID

        :param account_id: el id de la Cuenta a encontrar
        :type account_id: int
        :return: una instancia con el account_id, o None si no se encuentra
        :rtype: Account
        """
        logger.info(f"Procesando búsqueda para id {account_id} ...")
        return db.session.get(cls, account_id)

