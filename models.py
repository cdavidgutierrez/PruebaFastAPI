from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Usuarios(Base):
   __tablename__ = 'usuario'
   id = Column(Integer, primary_key = True)
   nombre = Column(String(255))
   email = Column(String(255))
   contrasena = Column(String(255))
   #-------
   compras = relationship("Compras", back_populates="comprador")
   
class Productos(Base):
   __tablename__ = 'producto'
   id = Column(Integer, primary_key = True)
   nombre = Column(String(255))
   url = Column(String(255))
   #-------
   compras = relationship("Compras", back_populates="producto")

#------
class Compras(Base):
   __tablename__ = "compra"
   id = Column(Integer, primary_key = True)
   id_usuario = Column(Integer, ForeignKey("usuario.id"))
   id_producto = Column(Integer, ForeignKey("producto.id"))
   total_productos = Column(Integer)
   
   comprador = relationship("Usuarios", back_populates="compras")
   producto = relationship("Productos", back_populates="compras")

   
   
