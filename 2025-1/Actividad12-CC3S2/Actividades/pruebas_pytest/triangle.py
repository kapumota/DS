def area_of_a_triangle(base: float, height: float) -> float:
    """Calcula el área de un triángulo"""

    # Verifica si tenemos los tipos de parámetros correctos
    if type(base) not in [int, float]:
        raise TypeError("La base debe ser un número")
    if type(height) not in [int, float]:
        raise TypeError("La altura debe ser un número")

    # Verifica si tenemos los valores correctos para los parámetros
    if base < 0:
        raise ValueError("La base debe ser un número positivo")
    if height < 0:
        raise ValueError("La altura debe ser un número positivo")

    return (base / 2) * height
