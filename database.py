import json
import os
from models import Usuario, Producto

USUARIOS_FILE = "usuarios.json"
INVENTARIO_FILE = "inventario.json"

def cargar_usuarios():
    """Carga la lista de usuarios desde el archivo JSON."""
    if not os.path.exists(USUARIOS_FILE):
        return []
    try:
        with open(USUARIOS_FILE, 'r') as f:
            data = json.load(f)
            return [Usuario.from_dict(u) for u in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def guardar_usuarios(usuarios):
    """Guarda la lista de usuarios en el archivo JSON."""
    with open(USUARIOS_FILE, 'w') as f:
        json.dump([u.to_dict() for u in usuarios], f, indent=4)

def cargar_inventario():
    """Carga el inventario desde el archivo JSON."""
    if not os.path.exists(INVENTARIO_FILE):
        return []
    try:
        with open(INVENTARIO_FILE, 'r') as f:
            data = json.load(f)
            return [Producto.from_dict(p) for p in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def guardar_inventario(inventario):
    """Guarda el inventario en el archivo JSON."""
    with open(INVENTARIO_FILE, 'w') as f:
        json.dump([p.to_dict() for p in inventario], f, indent=4)

def inicializar_datos():
    """Crea datos iniciales si los archivos no existen."""
    if not os.path.exists(USUARIOS_FILE):
        # Crear usuario admin por defecto
        admin = Usuario(1, "admin", "admin123", "Admin")
        guardar_usuarios([admin])
        print("Usuario 'admin' creado por defecto (password: admin123).")
