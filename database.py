import json
import os

# Nombres de archivos
USUARIOS_FILE = "usuarios.json"
INVENTARIO_FILE = "inventario.json"

def inicializar_archivos():
    """Crea los archivos JSON si no existen con datos iniciales."""
    if not os.path.exists(USUARIOS_FILE):
        # Usuario admin por defecto (password: admin)
        data = [
            {
                "username": "admin",
                "password_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
                "role": "admin"
            }
        ]
        guardar_datos(USUARIOS_FILE, data)
        print(f"Archivo {USUARIOS_FILE} creado con usuario admin por defecto.")

    if not os.path.exists(INVENTARIO_FILE):
        guardar_datos(INVENTARIO_FILE, [])
        print(f"Archivo {INVENTARIO_FILE} creado vacío.")

def cargar_datos(archivo):
    """Carga datos desde un archivo JSON."""
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def guardar_datos(archivo, datos):
    """Guarda datos en un archivo JSON."""
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        return True
    except Exception as e:
        print(f"Error guardando {archivo}: {e}")
        return False
