import os
import database
import auth
import inventario
import time

def test_system():
    print("=== INICIANDO TEST AUTOMÁTICO ===")
    
    # 1. Limpieza inicial
    if os.path.exists(database.USUARIOS_FILE):
        os.remove(database.USUARIOS_FILE)
    if os.path.exists(database.INVENTARIO_FILE):
        os.remove(database.INVENTARIO_FILE)
        
    # 2. Inicialización
    database.inicializar_archivos()
    print("[PASS] Inicialización de archivos completada.")
    
    # 3. Test Login Admin
    admin_user = auth.login("admin", "admin")
    assert admin_user is not None, "Login admin falló"
    assert admin_user.role == "admin", "Rol de admin incorrecto"
    print("[PASS] Login Admin exitoso.")
    
    # 4. Gestión de Inventario
    # Agregar
    exito, msg = inventario.agregar_producto("Laptop", "Computacion", 1000.0, 10)
    assert exito, f"Fallo al agregar producto: {msg}"
    print("[PASS] Producto agregado.")
    
    productos = inventario.obtener_productos()
    assert len(productos) == 1, "Debería haber 1 producto"
    assert productos[0]["nombre"] == "Laptop", "Nombre de producto incorrecto"
    
    # Editar
    id_prod = productos[0]["id"]
    exito, msg = inventario.editar_producto(id_prod, precio=1200.0)
    assert exito, f"Fallo al editar: {msg}"
    productos = inventario.obtener_productos()
    assert productos[0]["precio"] == 1200.0, "Precio no actualizado"
    print("[PASS] Producto editado.")
    
    # Actualizar Stock
    exito, msg = inventario.actualizar_stock(id_prod, 15)
    assert exito, f"Fallo al actualizar stock: {msg}"
    productos = inventario.obtener_productos()
    assert productos[0]["cantidad"] == 15, "Stock no actualizado"
    print("[PASS] Stock actualizado.")
    
    # 5. Gestión de Usuarios
    exito, msg = auth.crear_usuario(admin_user, "operador1", "pass123", "operador")
    assert exito, f"Fallo al crear usuario: {msg}"
    print("[PASS] Usuario operador creado.")
    
    # Login Operador
    op_user = auth.login("operador1", "pass123")
    assert op_user is not None, "Login operador falló"
    assert op_user.role == "operador", "Rol de operador incorrecto"
    print("[PASS] Login Operador exitoso.")
    
    # Intento de crear usuario con operador (Simulado, ya que la UI bloquea esto, pero probamos la función)
    exito, msg = auth.crear_usuario(op_user, "test", "test", "admin")
    assert not exito, "Operador no debería poder crear usuarios"
    print("[PASS] Restricción de operador verificada.")

    # 6. Eliminar Producto
    exito, msg = inventario.eliminar_producto(id_prod)
    assert exito, f"Fallo al eliminar producto: {msg}"
    productos = inventario.obtener_productos()
    assert len(productos) == 0, "El inventario debería estar vacío"
    print("[PASS] Producto eliminado.")
    
    print("\n=== TODOS LOS TESTS PASARON EXITOSAMENTE ===")

if __name__ == "__main__":
    test_system()
