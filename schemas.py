from typing import List, Union
from pydantic import BaseModel


#Crear primero la entidad hija.
class CompraCreate(BaseModel):
    id_usuario: int
    id_producto: int
    total_productos: int 

class Compra(CompraCreate):
    id: int

    class Config:
        orm_mode = True

#Modelos para la parte de creación (sin id!)
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    contrasena: str
    #------
    compras: List[Compra] = []

class ProductoCreate(BaseModel):
    nombre: str
    url: str
    #------
    compras: List[Compra] = []


#Modelos con todos los campos.
class Usuario(UsuarioCreate):
    id: int

    class Config:
        orm_mode = True

class Producto(ProductoCreate):
    id: int

    class Config:
        orm_mode = True
