from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from microservice.services import business_logic
from microservice.utils.logger import logger

router = APIRouter(
    prefix="/api/items",
    tags=["items"]
)


class ItemIn(BaseModel):
    """
    Modelo de datos para la creación de un ítem.
    """
    name: str = Field(..., example="sample item", description="Nombre único del ítem")
    description: Optional[str] = Field(
        None, example="optional description", description="Descripción opcional del ítem"
    )


class ItemOut(ItemIn):
    """
    Modelo de datos para la respuesta de un ítem existente,
    incluye el campo `id`.
    """
    id: int = Field(..., description="Identificador único del ítem")


@router.post(
    "/",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo ítem"
)
def create_item(item: ItemIn) -> ItemOut:
    """
    Crea un ítem nuevo usando la lógica de negocio.
    :param item: Datos de entrada para el ítem.
    :return: Ítem creado con su ID asignado.
    """
    try:
        created = business_logic.create_item(item.name, item.description)
        return created
    except Exception as exc:
        logger.exception("Error al crear ítem")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@router.get(
    "/",
    response_model=List[ItemOut],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los ítems"
)
def list_items() -> List[ItemOut]:
    """
    Recupera la lista de todos los ítems existentes.
    :return: Lista de ítems.
    """
    try:
        return business_logic.get_all_items()
    except Exception as exc:
        logger.exception("Error al listar ítems")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener los ítems"
        )
