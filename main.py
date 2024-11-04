from database import get_session, engine, Base
from crud.cliente_crud import ClienteCRUD
from crud.pedido_crud import PedidoCRUD
from database import Base
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Función principal para el uso del CRUD
def main():
    # Crear una sesión
    db = next(get_session())

    # Intentar crear un cliente
    cliente = ClienteCRUD.crear_cliente(db, "Carlos Pérez", "carlos@example.com")
    if cliente:
        print(f"Cliente creado: {cliente.nombre} - {cliente.email}")
    else:
        print("El cliente ya existe con ese correo electrónico.")

    # Intentar crear un pedido para el cliente existente
    if cliente:
        pedido = PedidoCRUD.crear_pedido(db, cliente.id, "Pedido de muebles")
        if pedido:
            print(f"Pedido creado: {pedido.descripcion} para el cliente {cliente.nombre}")
        else:
            print("No se pudo crear el pedido.")

    # Leer todos los clientes en la base de datos
    print("\nClientes en la base de datos:")
    clientes = ClienteCRUD.leer_clientes(db)
    for c in clientes:
        print(f"- {c.nombre} ({c.email})")

    # Actualizar el nombre del cliente
    cliente_actualizado = ClienteCRUD.actualizar_cliente(db, cliente.id, "Carlos Gómez", "carlos@example.com")
    if cliente_actualizado:
        print(f"\nCliente actualizado: {cliente_actualizado.nombre} - {cliente_actualizado.email}")
    else:
        print("No se pudo actualizar el cliente (posiblemente el email ya está en uso).")

    # Borrar un pedido
    if pedido:
        PedidoCRUD.borrar_pedido(db, pedido.id)
        print(f"Pedido con ID {pedido.id} eliminado")

    # Cerrar la sesión
    db.close()

if __name__ == "__main__":
    main()
