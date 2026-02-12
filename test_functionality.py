import database
from models import Usuario, Producto
import os

def test_persistence():
    print("Testing persistence...")
    
    # Clean up
    if os.path.exists("usuarios.json"): os.remove("usuarios.json")
    if os.path.exists("inventario.json"): os.remove("inventario.json")
    
    # Test initialization
    database.inicializar_datos()
    assert os.path.exists("usuarios.json")
    
    # Test User Loading
    usuarios = database.cargar_usuarios()
    assert len(usuarios) == 1
    assert usuarios[0].username == "admin"
    print("User persistence OK.")

    # Test Product Saving
    p1 = Producto(1, "Laptop", "Electronics", 10, 1500.00)
    database.guardar_inventario([p1])
    
    # Test Product Loading
    inventario = database.cargar_inventario()
    assert len(inventario) == 1
    assert inventario[0].nombre == "Laptop"
    print("Product persistence OK.")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_persistence()
