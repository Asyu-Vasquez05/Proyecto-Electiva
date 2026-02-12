import unittest
import os
import json
import auth
import database

class TestPasswordRecovery(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for testing
        self.test_db = "test_usuarios.json"
        database.USUARIOS_FILE = self.test_db
        
        # Create a test user
        self.test_user = {
            "username": "testuser",
            "password_hash": auth._hash_password("password123"),
            "role": "operador"
        }
        database.guardar_datos(self.test_db, [self.test_user])

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_set_security_question(self):
        success, msg = auth.set_security_question("testuser", "Color favorito?", "Azul")
        self.assertTrue(success)
        
        users = database.cargar_datos(self.test_db)
        user = users[0]
        self.assertEqual(user["security_question"], "Color favorito?")
        self.assertNotEqual(user["security_answer_hash"], "Azul") # Should be hashed

    def test_verify_security_answer(self):
        auth.set_security_question("testuser", "Color favorito?", "Azul")
        
        is_correct = auth.verify_security_answer("testuser", "Azul")
        self.assertTrue(is_correct)
        
        is_correct = auth.verify_security_answer("testuser", "Rojo")
        self.assertFalse(is_correct)

    def test_reset_password(self):
        auth.reset_password("testuser", "newpassword")
        
        user = auth.login("testuser", "newpassword")
        self.assertIsNotNone(user)
        
        user = auth.login("testuser", "password123")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
