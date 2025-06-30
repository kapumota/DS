from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="User Service")

# "Base de datos" en memoria usando un diccionario
users: Dict[int, Dict] = {}

class User(BaseModel):
    id: int      # Identificador único del usuario
    name: str    # Nombre del usuario
    email: str   # Correo electrónico del usuario

@app.post("/users/", response_model=User)
def create_user(user: User):
    # Verifica que el usuario no exista ya
    if user.id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    # Guarda el usuario en la "base de datos"
    users[user.id] = user.dict()
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    # Comprueba si el usuario existe
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    # Devuelve los datos del usuario
    return users[user_id]

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    # Verifica que el usuario exista antes de actualizar
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    # Actualiza los datos del usuario
    users[user_id] = user.dict()
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # Comprueba que el usuario exista antes de eliminar
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    # Elimina el usuario de la "base de datos"
    del users[user_id]
    return {"detail": "User deleted"}

# Punto de comprobación de salud del servicio
@app.get("/health")
def health():
    return {"status": "ok"}
