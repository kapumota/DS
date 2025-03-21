## Ejemplo de prueba
# tests/test_carrito.py

import pytest
from src.carrito import Carrito, Producto
from src.factories import ProductoFactory

def test_agregar_producto_nuevo():
    """
    AAA:
    Arrange: Se crea un carrito y se genera un producto.
    Act: Se agrega el producto al carrito.
    Assert: Se verifica que el carrito contiene un item con el producto y cantidad 1.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Laptop", precio=1000.00)
    
    # Act
    carrito.agregar_producto(producto)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].producto.nombre == "Laptop"
    assert items[0].cantidad == 1


def test_agregar_producto_existente_incrementa_cantidad():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se agrega el mismo producto nuevamente aumentando la cantidad.
    Assert: Se verifica que la cantidad del producto se incrementa en el item.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Mouse", precio=50.00)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    carrito.agregar_producto(producto, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3


def test_remover_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con cantidad 3.
    Act: Se remueve una unidad del producto.
    Assert: Se verifica que la cantidad del producto se reduce a 2.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Teclado", precio=75.00)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act
    carrito.remover_producto(producto, cantidad=1)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 2


def test_remover_producto_completo():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se remueve la totalidad de la cantidad del producto.
    Assert: Se verifica que el producto es eliminado del carrito.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Monitor", precio=300.00)
    carrito.agregar_producto(producto, cantidad=2)
    
    # Act
    carrito.remover_producto(producto, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_actualizar_cantidad_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 5.
    Assert: Se verifica que la cantidad se actualiza correctamente.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Auriculares", precio=150.00)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    carrito.actualizar_cantidad(producto, nueva_cantidad=5)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 5


def test_actualizar_cantidad_a_cero_remueve_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 0.
    Assert: Se verifica que el producto se elimina del carrito.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Cargador", precio=25.00)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act
    carrito.actualizar_cantidad(producto, nueva_cantidad=0)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_calcular_total():
    """
    AAA:
    Arrange: Se crea un carrito y se agregan varios productos con distintas cantidades.
    Act: Se calcula el total del carrito.
    Assert: Se verifica que el total es la suma correcta de cada item (precio * cantidad).
    """
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Impresora", precio=200.00)
    producto2 = ProductoFactory(nombre="Escáner", precio=150.00)
    carrito.agregar_producto(producto1, cantidad=2)  # Total 400
    carrito.agregar_producto(producto2, cantidad=1)  # Total 150
    
    # Act
    total = carrito.calcular_total()
    
    # Assert
    assert total == 550.00


def test_aplicar_descuento():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con una cantidad determinada.
    Act: Se aplica un descuento del 10% al total.
    Assert: Se verifica que el total con descuento sea el correcto.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Tablet", precio=500.00)
    carrito.agregar_producto(producto, cantidad=2)  # Total 1000
    
    # Act
    total_con_descuento = carrito.aplicar_descuento(10)
    
    # Assert
    assert total_con_descuento == 900.00


def test_aplicar_descuento_limites():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act y Assert: Se verifica que aplicar un descuento fuera del rango [0, 100] genere un error.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Smartphone", precio=800.00)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(150)
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(-5)
