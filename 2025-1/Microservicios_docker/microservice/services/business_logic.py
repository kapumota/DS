from typing import Dict, List, Optional

from microservice.services import database
from microservice.utils.logger import logger


def create_item(name: str, description: Optional[str] = None) -> Dict[str, Optional[int or str]]:
    """
    Crea un nuevo ítem en la base de datos y devuelve su representación.

    :param name: Nombre único del ítem.
    :param description: Descripción opcional del ítem.
    :return: Diccionario con los campos 'id', 'name' y 'description'.
    """
    # Insertar el ítem y obtener su ID
    item_id = database.add_item(name, description)

    # Construir la respuesta
    item = {
        "id": item_id,
        "name": name,
        "description": description,
    }

    # Registrar la operación de negocio
    logger.info("Ítem creado por la lógica de negocio: %s", item)
    return item


def get_all_items() -> List[Dict[str, Optional[int or str]]]:
    """
    Recupera todos los ítems existentes en la base de datos.

    :return: Lista de diccionarios, cada uno con 'id', 'name', 'description' y 'created_at'.
    """
    try:
        items = database.list_items()
        logger.debug("Lógica de negocio obtuvo %d ítems", len(items))
        return items
    except Exception as exc:
        logger.exception("Error al recuperar los ítems")
        # En un escenario real, aquí se podría lanzar una excepción HTTP o propia
        return []
