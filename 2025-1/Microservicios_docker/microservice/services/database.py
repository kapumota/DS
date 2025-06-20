from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional

import sqlite3

from microservice.utils.config import settings
from microservice.utils.logger import logger

DB_PATH = Path("app.db")


def init_db() -> None:
    """
    Inicializa la base de datos SQLite creando la tabla `items`
    si no existe todavía.
    """
    logger.info("Inicializando base de datos en %s", DB_PATH)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@contextmanager
def get_conn():
    """
    Context manager para obtener y cerrar una conexión SQLite.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def add_item(name: str, description: Optional[str] = None) -> int:
    """
    Inserta un nuevo ítem en la tabla `items` y devuelve su ID.

    :param name: Nombre único del ítem.
    :param description: Descripción opcional del ítem.
    :return: ID del ítem insertado.
    """
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        item_id = cursor.lastrowid
        logger.info("Ítem insertado: %s (id=%d)", name, item_id)
        return item_id


def list_items() -> List[Dict[str, Optional[str]]]:
    """
    Recupera todos los ítems de la tabla `items`.

    :return: Lista de diccionarios con keys id, name, description y created_at.
    """
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT id, name, description, created_at FROM items"
        )
        rows = cursor.fetchall()

    result = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3],
        }
        for row in rows
    ]
    logger.debug("Listado de ítems: %s", result)
    return result
