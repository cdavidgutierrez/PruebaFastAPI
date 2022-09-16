from pyexpat import model
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize router
router = APIRouter()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.get("/")
def root():
    return {"Mensaje": "API"}

#status_code : respuesta positiva si se crea de manera adecuada el usuario.
@router.post("/Usuario", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def CreateUsuario(newUsuario: schemas.UsuarioCreate, session: Session = Depends(get_session)):

    Usuariodb = models.Usuarios(nombre = newUsuario.nombre,
                            email = newUsuario.email,
                            contrasena = newUsuario.contrasena
                            )
    session.add(Usuariodb)
    session.commit()
    session.refresh(Usuariodb)
    
    return Usuariodb

@router.get("/Usuario/{id}", response_model=schemas.Usuario)
def ReadUsuario(id: int, session: Session = Depends(get_session)):

    usuario = session.query(models.Usuarios).get(id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no hallado.")

    return usuario

@router.put("/Usuario/{id}", response_model=schemas.Usuario)
def UpdateUsuario(id: int,
                n_nombre: str,
                n_email: str,
                n_contrasena: str,
                session: Session = Depends(get_session)):

    usuario = session.query(models.Usuarios).get(id)

    if usuario:
        usuario.nombre = n_nombre
        usuario.email = n_email
        usuario.contrasena = n_contrasena
        session.commit()
    
    if not usuario:
        return HTTPException(status_code=404, detail=f"Usuario con id {id} no hallado.")
    
    return usuario

@router.delete("/Usuario/{id}")
def DeleteUsuario(id: int, session: Session = Depends(get_session)):

    usuario = session.query(models.Usuarios).get(id)

    if not usuario:
        return HTTPException(status_code=404, detail=f"Usuario con id {id} no hallado.")

    session.delete(usuario)
    session.commit()

    return f"Borrado usuario con id {id}"

@router.get("/Usuario", response_model = List[schemas.Usuario])
def ReadAllUsuarios(session: Session = Depends(get_session)):

    usuarios_list = session.query(models.Usuarios).all()

    return usuarios_list

@router.post("/Producto", status_code=status.HTTP_201_CREATED)
def CreateProducto(newProducto: schemas.ProductoCreate, session: Session = Depends(get_session)):

    Productodb = models.Productos(nombre = newProducto.nombre, url = newProducto.url)
    session.add(Productodb)
    session.commit()
    session.refresh(Productodb)
    return Productodb

@router.get("/Producto/{id}")
def ReadProducto(id: int, session: Session = Depends(get_session)):

    producto = session.query(models.Productos).get(id)

    if not producto:
        raise HTTPException(status_code=404, detail=f"Producto con id {id} no hallado.")

    return producto

@router.put("/Producto/{id}")
def UpdateProducto(id: int, n_nombre: str, n_url: str, session: Session = Depends(get_session)):

    producto = session.query(models.Productos).get(id)

    if producto:
        producto.nombre = n_nombre
        producto.url = n_url
        session.commit()
    if not producto:
        raise HTTPException(status_code=404, detail=f"Producto con id {id} no hallado.")

    return producto

@router.delete("/Producto/{id}")
def DeleteProducto(id: int, session: Session = Depends(get_session)):

    producto = session.query(models.Productos).get(id)

    if producto:
        session.delete(producto)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Producto con id {id} no hallado.")

    return f"Borrado producto con id {id}"

@router.get("/Producto", response_model = List[schemas.Producto])
def ReadAllProductos(session: Session = Depends(get_session)):

    productos_list = session.query(models.Productos).all()
    
    return productos_list


@router.post("/Compra", response_model=schemas.Compra, status_code=status.HTTP_201_CREATED)
def CreateCompra(newCompra: schemas.CompraCreate, session: Session = Depends(get_session)):

    Compradb = models.Compras(id_usuario = newCompra.id_usuario,
                            id_producto = newCompra.id_producto,
                            total_productos = newCompra.total_productos
                            )
    session.add(Compradb)
    session.commit()
    session.refresh(Compradb)
    
    return Compradb

@router.get("/Compra/{id}", response_model=schemas.Compra)
def ReadCompra(id: int, session: Session = Depends(get_session)):

    compra = session.query(models.Compras).get(id)
    if not compra:
        raise HTTPException(status_code=404, detail=f"Compra con id {id} no hallado.")
    
    return compra

@router.put("/Compra/{id}")
def UpdateCompra(id: int, n_id_usuario: int, n_id_producto: int, n_total_productos: int,
                 session: Session = Depends(get_session)):
    
    compra = session.query(models.Compras).get(id)

    if not compra:
        raise HTTPException(status_code=404, detail=f"Compra con id {id} no hallado.")
    
    compra.id_usuario = n_id_usuario
    compra.id_producto = n_id_producto
    compra.total_productos = n_total_productos
    session.commit()

    return compra

@router.delete("/Compra/{id}")
def DeleteCompra(id: int, session: Session = Depends(get_session)):

    compra = session.query(models.Compras).get(id)

    if not compra:
        raise HTTPException(status_code=404, detail=f"Compra con id {id} no hallado.")
    
    session.delete(compra)
    session.commit()

    return f"Borrado producto con id {id}"

@router.get("/Compra", response_model=List[schemas.Compra])
def ReadAllCompras(session: Session = Depends(get_session)):

    compras_list = session.query(models.Compras).all()

    return compras_list