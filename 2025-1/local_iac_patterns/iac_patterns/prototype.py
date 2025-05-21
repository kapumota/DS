"""Patrón Prototype

Permite clonar objetos Terraform y modificarlos de forma controlada,
sin alterar el original.
"""

import copy
from typing import Dict, Any

class ResourcePrototype:
    """
    Prototipo de recurso Terraform que puede ser clonado y modificado
    de forma independiente, siguiendo el patrón Prototype.
    """

    def __init__(self, resource_dict: Dict[str, Any]) -> None:
        """
        Inicializa el prototipo con un diccionario de recurso base.

        Args:
            resource_dict: Estructura dict que representa un recurso Terraform.
        """
        self._resource_dict = resource_dict

    def clone(self, mutator=lambda d: d) -> "ResourcePrototype":
        """
        Clona el recurso original aplicando una mutación opcional.

        Args:
            mutator: Función opcional que recibe el clon y puede modificarlo en el acto.

        Returns:
            Nuevo objeto `ResourcePrototype` que contiene el recurso clonado y modificado.
        """
        # Copia profunda para evitar mutaciones al recurso original
        new_dict = copy.deepcopy(self._resource_dict)

        # Aplica la función mutadora para modificar el clon si se desea
        mutator(new_dict)

        # Devuelve un nuevo prototipo con el contenido clonado
        return ResourcePrototype(new_dict)

    @property
    def data(self) -> Dict[str, Any]:
        """
        Acceso de solo lectura al recurso almacenado.

        Returns:
            Diccionario del recurso actual (clonado o original).
        """
        return self._resource_dict
