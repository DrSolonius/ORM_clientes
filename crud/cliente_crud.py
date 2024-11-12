from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Cliente

class ClienteCRUD:
    @staticmethod
    def crear_cliente(db: Session, nombre: str, email: str, edad: int):
        cliente_existente = db.query(Cliente).filter_by(email=email).first()
        if cliente_existente:
            print(f"El cliente con el email '{email}' ya existe.")
            return cliente_existente

        cliente = Cliente(nombre=nombre, email=email, edad=edad)
        db.add(cliente)
        try:
            db.commit()
            db.refresh(cliente)
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error al crear el cliente: {e}")
            return None
        return cliente

    @staticmethod
    def leer_clientes(db: Session):
        """Obtiene todos los clientes en la base de datos."""
        return db.query(Cliente).all()

    @staticmethod
    def actualizar_cliente(db: Session, email_actual: str, nuevo_nombre: str, nuevo_email: str = None, edad: int = None):
        cliente = db.query(Cliente).get(email_actual)
        if not cliente:
            print(f"No se encontró el cliente con el email '{email_actual}'.")
            return None

        if nuevo_email and nuevo_email != email_actual:
            nuevo_cliente = Cliente(nombre=nuevo_nombre, email=nuevo_email, edad=edad)
            db.add(nuevo_cliente)
            try:
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error al actualizar el cliente con nuevo email: {e}")
                return None

            db.delete(cliente)
            try:
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error al eliminar el cliente antiguo: {e}")
                return None

            return nuevo_cliente
        else:
            cliente.nombre = nuevo_nombre
            cliente.edad = edad
            try:
                db.commit()
                db.refresh(cliente)
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error al actualizar el cliente: {e}")
                return None
            return cliente

    @staticmethod
    def borrar_cliente(db: Session, email: str):
        cliente = db.query(Cliente).get(email)
        if cliente:
            db.delete(cliente)
            try:
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error al borrar el cliente: {e}")
                return None
            return cliente
        return None
