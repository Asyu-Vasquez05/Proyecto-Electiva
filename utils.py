import os

def limpiar_pantalla():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar_tecla():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")

def validar_entero(mensaje):
    """Solicita un entero al usuario y valida la entrada."""
    while True:
        try:
            val = int(input(mensaje))
            if val < 0:
                print("Por favor ingrese un número positivo.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número entero.")

def validar_float(mensaje):
    """Solicita un número decimal al usuario y valida la entrada."""
    while True:
        try:
            val = float(input(mensaje))
            if val < 0:
                print("Por favor ingrese un número positivo.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número decimal.")

def mostrar_tabla_inventario(inventario):
    """Muestra el inventario en formato de tabla."""
    if not inventario:
        print("El inventario está vacío.")
        return
    
    print("-" * 80)
    print(f"{'ID':<5} {'Nombre':<20} {'Categoría':<15} {'Cantidad':<10} {'Precio':<10}")
    print("-" * 80)
    for p in inventario:
        print(f"{p.id:<5} {p.nombre[:18]:<20} {p.categoria[:13]:<15} {p.cantidad:<10} ${p.precio:<9.2f}")
    print("-" * 80)
