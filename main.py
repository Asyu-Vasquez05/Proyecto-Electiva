import sys
from models import Usuario, Producto
import database
import utils

# --- Funciones de Gestión de Usuarios (Usuario Admin) ---
def menu_usuarios(usuarios):
    while True:
        utils.limpiar_pantalla()
        print("=== GESTIÓN DE USUARIOS (ADMIN) ===")
        print("1. Crear Usuario")
        print("2. Listar Usuarios")
        print("3. Eliminar Usuario")
        print("4. Volver al Menú Principal")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            crear_usuario(usuarios)
        elif opcion == '2':
            listar_usuarios(usuarios)
        elif opcion == '3':
            eliminar_usuario(usuarios)
        elif opcion == '4':
            break
        else:
            print("Opción inválida.")
            utils.esperar_tecla()

def crear_usuario(usuarios):
    print("\n--- Crear Nuevo Usuario ---")
    try:
        id_nuevo = len(usuarios) + 1 # Generar ID simple
        username = input("Nombre de usuario: ")
        # Validar si ya existe
        if any(u.username == username for u in usuarios):
            print("Error: El usuario ya existe.")
            utils.esperar_tecla()
            return

        password = input("Contraseña: ")
        print("Roles disponibles: 1. Admin, 2. Operador")
        rol_op = input("Seleccione rol (1/2): ")
        rol = "Admin" if rol_op == '1' else "Operador"
        
        nuevo_usuario = Usuario(id_nuevo, username, password, rol)
        usuarios.append(nuevo_usuario)
        database.guardar_usuarios(usuarios)
        print("Usuario creado exitosamente.")
    except Exception as e:
        print(f"Error al crear usuario: {e}")
    utils.esperar_tecla()

def listar_usuarios(usuarios):
    print("\n--- Lista de Usuarios ---")
    print(f"{'ID':<5} {'Username':<20} {'Rol':<10}")
    print("-" * 40)
    for u in usuarios:
        print(f"{u.id:<5} {u.username:<20} {u.role:<10}")
    utils.esperar_tecla()

def eliminar_usuario(usuarios):
    listar_usuarios(usuarios)
    try:
        uid = utils.validar_entero("Ingrese ID del usuario a eliminar: ")
        # Prevenir auto-eliminación o eliminar al último admin podría ser una validación extra
        usuario_a_borrar = next((u for u in usuarios if u.id == uid), None)
        
        if usuario_a_borrar:
            if usuario_a_borrar.username == 'admin':
                print("No se puede eliminar al superusuario 'admin'.")
            else:    
                usuarios.remove(usuario_a_borrar)
                database.guardar_usuarios(usuarios)
                print("Usuario eliminado.")
        else:
            print("Usuario no encontrado.")
    except Exception as e:
        print(f"Error: {e}")
    utils.esperar_tecla()

# --- Funciones de Gestión de Inventario ---
def menu_inventario(inventario, rol_usuario):
    while True:
        utils.limpiar_pantalla()
        print(f"=== GESTIÓN DE INVENTARIO ({rol_usuario.upper()}) ===")
        print("1. Ver Inventario")
        print("2. Buscar Producto")
        if rol_usuario == 'Admin':
            print("3. Agregar Producto")
            print("4. Editar Stock/Precio")
            print("5. Eliminar Producto")
        print("0. Volver al Menú Principal")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            utils.limpiar_pantalla()
            utils.mostrar_tabla_inventario(inventario)
            utils.esperar_tecla()
        elif opcion == '2':
            buscar_producto(inventario)
        elif opcion == '3' and rol_usuario == 'Admin':
            agregar_producto(inventario)
        elif opcion == '4' and rol_usuario == 'Admin':
            editar_producto(inventario)
        elif opcion == '5' and rol_usuario == 'Admin':
            eliminar_producto(inventario)
        elif opcion == '0':
            break
        else:
            print("Opción inválida o permisos insuficientes.")
            utils.esperar_tecla()

def buscar_producto(inventario):
    termino = input("Ingrese nombre o categoría a buscar: ").lower()
    resultados = [p for p in inventario if termino in p.nombre.lower() or termino in p.categoria.lower()]
    utils.mostrar_tabla_inventario(resultados)
    utils.esperar_tecla()

def agregar_producto(inventario):
    print("\n--- Agregar Producto ---")
    try:
        # ID autoincremental simple
        ultimo_id = inventario[-1].id if inventario else 0
        nuevo_id = ultimo_id + 1
        
        nombre = input("Nombre del producto: ")
        categoria = input("Categoría: ")
        cantidad = utils.validar_entero("Cantidad en stock: ")
        precio = utils.validar_float("Precio unitario: ")
        
        nuevo_prod = Producto(nuevo_id, nombre, categoria, cantidad, precio)
        inventario.append(nuevo_prod)
        database.guardar_inventario(inventario)
        print("Producto agregado exitosamente.")
    except Exception as e:
        print(f"Error al agregar producto: {e}")
    utils.esperar_tecla()

def editar_producto(inventario):
    utils.mostrar_tabla_inventario(inventario)
    id_prod = utils.validar_entero("Ingrese ID del producto a editar: ")
    producto = next((p for p in inventario if p.id == id_prod), None)
    
    if producto:
        print(f"Editando: {producto.nombre}")
        print("Deje en blanco para mantener el valor actual.")
        
        nuevo_nombre = input(f"Nombre ({producto.nombre}): ")
        if nuevo_nombre: producto.nombre = nuevo_nombre
        
        nueva_cat = input(f"Categoría ({producto.categoria}): ")
        if nueva_cat: producto.categoria = nueva_cat
        
        nueva_cant = input(f"Cantidad ({producto.cantidad}): ")
        if nueva_cant: 
            try:
                producto.cantidad = int(nueva_cant)
            except ValueError:
                print("Cantidad inválida, se mantiene la anterior.")
        
        nuevo_precio = input(f"Precio ({producto.precio}): ")
        if nuevo_precio:
            try:
                producto.precio = float(nuevo_precio)
            except ValueError:
                print("Precio inválido, se mantiene el anterior.")
                
        database.guardar_inventario(inventario)
        print("Producto actualizado.")
    else:
        print("Producto no encontrado.")
    utils.esperar_tecla()

def eliminar_producto(inventario):
    utils.mostrar_tabla_inventario(inventario)
    id_prod = utils.validar_entero("Ingrese ID del producto a eliminar: ")
    producto = next((p for p in inventario if p.id == id_prod), None)
    
    if producto:
        confirm = input(f"¿Seguro que desea eliminar '{producto.nombre}'? (s/n): ")
        if confirm.lower() == 's':
            inventario.remove(producto)
            database.guardar_inventario(inventario)
            print("Producto eliminado.")
    else:
        print("Producto no encontrado.")
    utils.esperar_tecla()

# --- Sistema de Login ---
def login(usuarios):
    intentos = 3
    while intentos > 0:
        utils.limpiar_pantalla()
        print("=== LOGIN ===")
        user_input = input("Usuario: ")
        pass_input = input("Contraseña: ")
        
        usuario = next((u for u in usuarios if u.username == user_input and u.password == pass_input), None)
        
        if usuario:
            return usuario
        else:
            print("Credenciales incorrectas.")
            intentos -= 1
            utils.esperar_tecla()
    
    return None

# --- Main Loop ---
def main():
    # Inicializar
    database.inicializar_datos()
    usuarios = database.cargar_usuarios()
    inventario = database.cargar_inventario()
    
    while True:
        usuario_actual = login(usuarios)
        
        if not usuario_actual:
            print("Demasiados intentos fallidos. Saliendo...")
            break
            
        # Loop del menú principal una vez logueado
        while True:
            utils.limpiar_pantalla()
            print(f"Bienvenido, {usuario_actual.username} ({usuario_actual.role})")
            print("1. Gestión de Inventario")
            if usuario_actual.role == 'Admin':
                print("2. Gestión de Usuarios")
            print("0. Cerrar Sesión")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == '1':
                menu_inventario(inventario, usuario_actual.role)
            elif opcion == '2' and usuario_actual.role == 'Admin':
                menu_usuarios(usuarios)
            elif opcion == '0':
                print("Cerrando sesión...")
                break # Sale al loop de login
            else:
                print("Opción inválida.")
                utils.esperar_tecla()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo del programa...")
        sys.exit(0)
