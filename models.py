# Definición de modelos clases etc.
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    
    email = Column(String, primary_key=True)  # Email como clave primaria
    nombre = Column(String, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True )
    descripcion = Column(String, nullable=False)
    cliente_email = Column(String, ForeignKey('clientes.email', onupdate="CASCADE"), nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")

