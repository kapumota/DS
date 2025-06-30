from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Order Service")

# "Base de datos" en memoria usando un diccionario
orders: Dict[int, Dict] = {}

class Order(BaseModel):
    id: int        # Identificador único de la orden
    user_id: int   # Identificador del usuario que realiza la orden
    item: str      # Nombre del artículo pedido
    quantity: int  # Cantidad solicitada

@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    # Comprueba si la orden ya existe
    if order.id in orders:
        raise HTTPException(status_code=400, detail="Order already exists")
    # Guarda la orden en la "base de datos"
    orders[order.id] = order.dict()
    return order

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    # Verifica si la orden existe
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    # Devuelve la orden encontrada
    return orders[order_id]

@app.get("/orders/user/{user_id}", response_model=List[Order])
def get_orders_by_user(user_id: int):
    # Filtra todas las órdenes que correspondan al user_id dado
    user_orders = [o for o in orders.values() if o["user_id"] == user_id]
    return user_orders

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    # Comprueba si la orden existe antes de eliminar
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    # Elimina la orden de la "base de datos"
    del orders[order_id]
    return {"detail": "Order deleted"}

# Punto de comprobación de salud del servicio
@app.get("/health")
def health():
    return {"status": "ok"}
