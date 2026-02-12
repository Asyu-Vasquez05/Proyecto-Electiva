import hashlib
import database

class Usuario:
    def __init__(self, username, role):
        self.username = username
        self.role = role

def _hash_password(password):
    """Genera un hash SHA256 de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    """Verifica credenciales y retorna un objeto Usuario si son válidas."""
    usuarios = database.cargar_datos(database.USUARIOS_FILE)
    password_hash = _hash_password(password)
    
    for user in usuarios:
        if user["username"] == username and user["password_hash"] == password_hash:
            return Usuario(user["username"], user["role"])
    return None

def crear_usuario(admin_user, new_username, new_password, new_role):
    """Crea un nuevo usuario (Solo Admin)."""
    if admin_user.role != "admin":
        return False, "Error: Permisos insuficientes."
    
    usuarios = database.cargar_datos(database.USUARIOS_FILE)
    
    # Verificar si ya existe
    if any(u["username"] == new_username for u in usuarios):
        return False, "Error: El usuario ya existe."
    
    nuevo_usuario = {
        "username": new_username,
        "password_hash": _hash_password(new_password),
        "role": new_role
    }
    
    usuarios.append(nuevo_usuario)
    if database.guardar_datos(database.USUARIOS_FILE, usuarios):
        return True, "Usuario creado exitosamente."
    return False, "Error al guardar en la base de datos."

def eliminar_usuario(admin_user, username_to_delete):
    """Elimina un usuario (Solo Admin)."""
    if admin_user.role != "admin":
        return False, "Error: Permisos insuficientes."
    
    if username_to_delete == admin_user.username:
        return False, "Error: No puedes eliminarte a ti mismo."

    usuarios = database.cargar_datos(database.USUARIOS_FILE)
    usuarios_filtrados = [u for u in usuarios if u["username"] != username_to_delete]
    
    if len(usuarios) == len(usuarios_filtrados):
        return False, "Error: Usuario no encontrado."
    
    if database.guardar_datos(database.USUARIOS_FILE, usuarios_filtrados):
        return True, "Usuario eliminado exitosamente."
    return False, "Error al guardar en la base de datos."

def set_security_question(username, question, answer):
    """Establece la pregunta y respuesta de seguridad para un usuario."""
    usuarios = database.cargar_datos(database.USUARIOS_FILE)
    for user in usuarios:
        if user["username"] == username:
            user["security_question"] = question
            user["security_answer_hash"] = _hash_password(answer)
            if database.guardar_datos(database.USUARIOS_FILE, usuarios):
                return True, "Pregunta de seguridad actualizada."
            return False, "Error al guardar en la base de datos."
    return False, "Usuario no encontrado."

def get_security_question(username):
    """Obtiene la pregunta de seguridad de un usuario."""
    usuarios = database.cargar_datos(database.USUARIOS_FILE)
    for user in usuarios:
        if user["username"] == username:
            return user.get("security_question")
    return None

def verify_security_answer(username, answer):
    """Verifica si la respuesta a la pregunta de seguridad es correcta."""
    usuarios = database.cargar_datos(database.USUARIOS_FILE)
    answer_hash = _hash_password(answer)
    for user in usuarios:
        if user["username"] == username:
            return user.get("security_answer_hash") == answer_hash
    return False

def reset_password(username, new_password):
    """Restablece la contraseña del usuario."""
    usuarios = database.cargar_datos(database.USUARIOS_FILE)
    for user in usuarios:
        if user["username"] == username:
            user["password_hash"] = _hash_password(new_password)
            if database.guardar_datos(database.USUARIOS_FILE, usuarios):
                return True, "Contraseña restablecida exitosamente."
            return False, "Error al guardar en la base de datos."
    return False, "Usuario no encontrado."
