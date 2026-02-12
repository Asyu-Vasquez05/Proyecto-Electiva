import json

class Usuario:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        return Usuario(data["id"], data["username"], data["password"], data["role"])

class Producto:
    def __init__(self, id, nombre, categoria, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        return Producto(data["id"], data["nombre"], data["categoria"], data["cantidad"], data["precio"])
