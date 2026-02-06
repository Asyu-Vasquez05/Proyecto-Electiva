import os
import sys
import getpass
import time
import database
import auth
import inventario

# Intentar importar tabulate para tablas bonitas
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def limpiar_pantalla():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar_enter():
    input("\nPresione Enter para continuar...")

def mostrar_tabla(datos, headers):
    """Muestra una tabla formateada."""
    if not datos:
        print("\nNo hay datos para mostrar.")
        return

    # Convertir lista de dicts a lista de listas para tabulate
    if isinstance(datos[0], dict):
        filas = [[d.get(k, "") for k in headers] for d in datos]
    else:
        filas = datos

    if HAS_TABULATE:
        print(tabulate(filas, headers=headers, tablefmt="grid"))
    else:
        # Formato manual simple
        print("\n" + " | ".join(headers))
        print("-" * (len(headers) * 15))
        for fila in filas:
            print(" | ".join(str(item).ljust(15) for item in fila))

def solicitar_entero(mensaje):
    """Solicita un entero validado."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Por favor ingrese un número válido.")

def solicitar_flotante(mensaje):
    """Solicita un flotante validado."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Por favor ingrese un precio válido.")

def login():
    """Maneja el flujo de inicio de sesión."""
    while True:
        limpiar_pantalla()
        print("=== SISTEMA DE GESTIÓN DE INVENTARIO ===")
        print("1. Iniciar Sesión")
        print("2. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            username = input("Usuario: ")
            # getpass oculta la contraseña al escribir
            password = getpass.getpass("Contraseña: ")
            
            usuario = auth.login(username, password)
            if usuario:
                print(f"\nBienvenido, {usuario.username} ({usuario.role})")
                time.sleep(1)
                return usuario
            else:
                print("\nError: Credenciales incorrectas.")
                time.sleep(2)
        elif opcion == "2":
            print("Saliendo del sistema...")
            sys.exit()
        else:
            print("Opción inválida.")
            time.sleep(1)

def ver_inventario():
    productos = inventario.obtener_productos()
    headers = ["id", "nombre", "categoria", "precio", "cantidad"]
    print("\n--- INVENTARIO ACTUAL ---")
    mostrar_tabla(productos, headers)

def menu_admin(usuario):
    while True:
        limpiar_pantalla()
        print(f"=== PANEL DE ADMINISTRADOR ({usuario.username}) ===")
        print("1. Ver Inventario")
        print("2. Buscar Producto")
        print("3. Agregar Producto")
        print("4. Editar Producto")
        print("5. Eliminar Producto")
        print("6. Actualizar Stock")
        print("7. Crear Nuevo Usuario")
        print("8. Eliminar Usuario")
        print("9. Cerrar Sesión")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            ver_inventario()
            esperar_enter()
            
        elif opcion == "2":
            termino = input("Ingrese nombre o categoría a buscar: ")
            resultados = inventario.buscar_productos(termino)
            headers = ["id", "nombre", "categoria", "precio", "cantidad"]
            print(f"\nResultados para '{termino}':")
            mostrar_tabla(resultados, headers)
            esperar_enter()
            
        elif opcion == "3":
            print("\n--- AGREGAR PRODUCTO ---")
            nombre = input("Nombre: ")
            categoria = input("Categoría: ")
            precio = solicitar_flotante("Precio: ")
            cantidad = solicitar_entero("Cantidad Inicial: ")
            
            exito, msg = inventario.agregar_producto(nombre, categoria, precio, cantidad)
            print(msg)
            esperar_enter()
            
        elif opcion == "4":
            print("\n--- EDITAR PRODUCTO ---")
            ver_inventario()
            id_prod = solicitar_entero("\nID del producto a editar: ")
            
            print("Deje en blanco si no desea modificar el campo.")
            nombre = input("Nuevo Nombre: ")
            categoria = input("Nueva Categoría: ")
            precio_str = input("Nuevo Precio: ")
            
            # Convertir precio solo si no está vacío
            precio = float(precio_str) if precio_str.strip() else None
            
            # Filtrar valores vacíos
            nombre = nombre if nombre.strip() else None
            categoria = categoria if categoria.strip() else None
            
            exito, msg = inventario.editar_producto(id_prod, nombre, categoria, precio)
            print(msg)
            esperar_enter()
            
        elif opcion == "5":
            print("\n--- ELIMINAR PRODUCTO ---")
            ver_inventario()
            id_prod = solicitar_entero("\nID del producto a eliminar: ")
            
            confirm = input(f"¿Seguro que desea eliminar el ID {id_prod}? (s/n): ")
            if confirm.lower() == 's':
                exito, msg = inventario.eliminar_producto(id_prod)
                print(msg)
            else:
                print("Operación cancelada.")
            esperar_enter()
            
        elif opcion == "6":
            print("\n--- ACTUALIZAR STOCK ---")
            ver_inventario()
            id_prod = solicitar_entero("\nID del producto: ")
            nueva_cantidad = solicitar_entero("Nueva cantidad total: ")
            
            exito, msg = inventario.actualizar_stock(id_prod, nueva_cantidad)
            print(msg)
            esperar_enter()

        elif opcion == "7":
            print("\n--- CREAR USUARIO ---")
            new_user = input("Nuevo Usuario: ")
            new_pass = getpass.getpass("Contraseña: ")
            role = input("Rol (admin/operador): ").lower()
            
            if role not in ["admin", "operador"]:
                print("Error: Rol inválido. Use 'admin' o 'operador'.")
            else:
                exito, msg = auth.crear_usuario(usuario, new_user, new_pass, role)
                print(msg)
            esperar_enter()

        elif opcion == "8":
            print("\n--- ELIMINAR USUARIO ---")
            usuarios = database.cargar_datos(database.USUARIOS_FILE)
            headers = ["username", "role"]
            mostrar_tabla(usuarios, headers)
            
            user_to_del = input("\nUsuario a eliminar: ")
            exito, msg = auth.eliminar_usuario(usuario, user_to_del)
            print(msg)
            esperar_enter()
            
        elif opcion == "9":
            break
        else:
            print("Opción inválida.")
            time.sleep(1)

def menu_operador(usuario):
    while True:
        limpiar_pantalla()
        print(f"=== PANEL DE OPERADOR ({usuario.username}) ===")
        print("1. Ver Inventario")
        print("2. Buscar Producto")
        print("3. Actualizar Stock")
        print("4. Cerrar Sesión")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            ver_inventario()
            esperar_enter()
            
        elif opcion == "2":
            termino = input("Ingrese nombre o categoría a buscar: ")
            resultados = inventario.buscar_productos(termino)
            headers = ["id", "nombre", "categoria", "precio", "cantidad"]
            print(f"\nResultados para '{termino}':")
            mostrar_tabla(resultados, headers)
            esperar_enter()
            
        elif opcion == "3":
            print("\n--- ACTUALIZAR STOCK ---")
            ver_inventario()
            id_prod = solicitar_entero("\nID del producto: ")
            nueva_cantidad = solicitar_entero("Nueva cantidad total: ")
            
            exito, msg = inventario.actualizar_stock(id_prod, nueva_cantidad)
            print(msg)
            esperar_enter()
            
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")
            time.sleep(1)

def iniciar_programa():
    print("Inicializando sistema...")
    database.inicializar_archivos()
    time.sleep(1)
    
    while True:
        usuario_actual = login()
        
        if usuario_actual.role == "admin":
            menu_admin(usuario_actual)
        elif usuario_actual.role == "operador":
            menu_operador(usuario_actual)
        else:
            print(f"Error: Rol desconocido '{usuario_actual.role}'.")
            time.sleep(2)

if __name__ == "__main__":
    try:
        iniciar_programa()
    except KeyboardInterrupt:
        print("\n\nSaliendo del programa...")
        sys.exit()
