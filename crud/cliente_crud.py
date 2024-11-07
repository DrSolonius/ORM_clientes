from sqlalchemy.orm import Session
from models import Cliente

class ClienteCRUD:
    @staticmethod
    def crear_cliente(db: Session, nombre: str, email: str,edad:int):
        cliente_existente = db.query(Cliente).filter_by(email=email).first()
        if cliente_existente:
            print(f"El cliente con el email '{email}' ya existe.")
            return cliente_existente

        cliente = Cliente(nombre=nombre, email=email,edad=edad)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    @staticmethod
    def leer_clientes(db: Session):
        """Obtiene todos los clientes en la base de datos."""
        return db.query(Cliente).all()
    
    
    @staticmethod
    def actualizar_cliente(db: Session, email_actual: str, nuevo_nombre: str, nuevo_email: str = None, nueva_edad: int = None):
        # Buscar al cliente por su email actual
        cliente = db.query(Cliente).get(email_actual)
        if not cliente:
            print(f"No se encontró el cliente con el email '{email_actual}'.")
            return None

        # Si se quiere actualizar el email y es diferente
        if nuevo_email and nuevo_email != email_actual:
            # Crear un nuevo cliente con el nuevo email
            nuevo_cliente = Cliente(nombre=nuevo_nombre, email=nuevo_email, edad=nueva_edad)
            db.add(nuevo_cliente)
            db.commit()

            # Eliminar el cliente antiguo
            db.delete(cliente)
            db.commit()

            return nuevo_cliente
        else:
            # Si no cambia el email, solo actualiza los campos disponibles
            cliente.nombre = nuevo_nombre
            if nueva_edad is not None:
                cliente.edad = nueva_edad  # Actualiza la edad si se pasa el nuevo valor
            if nuevo_email and nuevo_email != email_actual:
                cliente.email = nuevo_email  # Si se pasa un nuevo email, se actualiza

            db.commit()  # Guarda los cambios en la base de datos
            db.refresh(cliente)  # Refresca el cliente con los nuevos valores
            return cliente


    @staticmethod
    def borrar_cliente(db: Session, email: str):
        cliente = db.query(Cliente).get(email)
        if cliente:
            db.delete(cliente)
            db.commit()
            return cliente
        return None


