import database

def obtener_productos():
    """Retorna la lista de productos."""
    return database.cargar_datos(database.INVENTARIO_FILE)

def _guardar_productos(productos):
    """Guarda la lista de productos."""
    return database.guardar_datos(database.INVENTARIO_FILE, productos)

def buscar_producto_por_id(productos, id_producto):
    """Busca un producto por ID y retorna su índice y el producto."""
    for i, p in enumerate(productos):
        if p["id"] == id_producto:
            return i, p
    return -1, None

def agregar_producto(nombre, categoria, precio, cantidad):
    """Agrega un nuevo producto al inventario."""
    productos = obtener_productos()
    
    # Generar nuevo ID (max id + 1)
    if not productos:
        nuevo_id = 1
    else:
        nuevo_id = max(p["id"] for p in productos) + 1
        
    nuevo_producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "categoria": categoria,
        "precio": float(precio),
        "cantidad": int(cantidad)
    }
    
    productos.append(nuevo_producto)
    if _guardar_productos(productos):
        return True, f"Producto '{nombre}' agregado con ID {nuevo_id}."
    return False, "Error al guardar el producto."

def editar_producto(id_producto, nombre=None, categoria=None, precio=None):
    """Edita detalles de un producto (menos cantidad/stock)."""
    productos = obtener_productos()
    idx, producto = buscar_producto_por_id(productos, id_producto)
    
    if idx == -1:
        return False, "Producto no encontrado."
    
    if nombre:
        producto["nombre"] = nombre
    if categoria:
        producto["categoria"] = categoria
    if precio is not None:
        producto["precio"] = float(precio)
        
    productos[idx] = producto
    if _guardar_productos(productos):
        return True, "Producto actualizado exitosamente."
    return False, "Error al guardar los cambios."

def actualizar_stock(id_producto, nueva_cantidad):
    """Actualiza solo el stock de un producto."""
    productos = obtener_productos()
    idx, producto = buscar_producto_por_id(productos, id_producto)
    
    if idx == -1:
        return False, "Producto no encontrado."
    
    producto["cantidad"] = int(nueva_cantidad)
    productos[idx] = producto
    
    if _guardar_productos(productos):
        return True, "Stock actualizado exitosamente."
    return False, "Error al guardar el stock."

def eliminar_producto(id_producto):
    """Elimina un producto por su ID."""
    productos = obtener_productos()
    idx, producto = buscar_producto_por_id(productos, id_producto)
    
    if idx == -1:
        return False, "Producto no encontrado."
    
    productos.pop(idx)
    if _guardar_productos(productos):
        return True, "Producto eliminado exitosamente."
    return False, "Error al eliminar el producto."

def buscar_productos(termino):
    """Busca productos por nombre o categoría (case insensible)."""
    productos = obtener_productos()
    termino = termino.lower()
    resultado = [
        p for p in productos 
        if termino in p["nombre"].lower() or termino in p["categoria"].lower()
    ]
    return resultado
