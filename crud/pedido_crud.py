from sqlalchemy.orm import Session
from models import Pedido, Cliente


class PedidoCRUD:

    @staticmethod
    def crear_pedido(db: Session, cliente_id: int, descripcion: str):
        cliente = db.query(Cliente).get(cliente_id)
        if cliente:
            pedido = Pedido(descripcion=descripcion, cliente=cliente)
            db.add(pedido)
            db.commit()
            db.refresh(pedido)
            return pedido
        return None

    @staticmethod
    def leer_pedidos(db: Session):
        return db.query(Pedido).all()

    @staticmethod
    def actualizar_pedido(db: Session, pedido_id: int, nueva_descripcion: str):
        pedido = db.query(Pedido).get(pedido_id)
        if pedido:
            pedido.descripcion = nueva_descripcion
            db.commit()
            db.refresh(pedido)
            return pedido
        return None

    @staticmethod
    def borrar_pedido(db: Session, pedido_id: int):
        pedido = db.query(Pedido).get(pedido_id)
        if pedido:
            db.delete(pedido)
            db.commit()
            return pedido
        return None
