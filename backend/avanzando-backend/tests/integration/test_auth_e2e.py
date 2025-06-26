import pytest
import json
from src.models.user import User, UserRole, db

class TestAuthE2E:
    """Pruebas End-to-End para las APIs de autenticación"""
    
    def test_register_login_flow(self, client):
        """Prueba el flujo completo de registro y login"""
        # Datos de registro
        register_data = {
            'nombre': 'Usuario Test E2E',
            'email': 'e2e@example.com',
            'password': 'password123',
            'rol': 'pm'
        }
        
        # 1. Registro de usuario
        response = client.post('/api/auth/register', 
                             data=json.dumps(register_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Usuario creado exitosamente'
        assert 'user' in data
        assert data['user']['email'] == 'e2e@example.com'
        assert data['user']['rol'] == 'pm'
        
        # 2. Login con credenciales correctas
        login_data = {
            'email': 'e2e@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == 'e2e@example.com'
        
        # No retornar nada para evitar warning de pytest
    
    def test_register_duplicate_email(self, client):
        """Prueba registro con email duplicado"""
        # Crear primer usuario
        register_data = {
            'nombre': 'Usuario 1',
            'email': 'duplicate@example.com',
            'password': 'password123',
            'rol': 'pm'
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(register_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        # Intentar crear segundo usuario con mismo email
        register_data['nombre'] = 'Usuario 2'
        response = client.post('/api/auth/register',
                             data=json.dumps(register_data),
                             content_type='application/json')
        
        assert response.status_code == 409  # Conflict, no Bad Request
        data = response.get_json()
        assert 'error' in data
    
    def test_login_invalid_credentials(self, client):
        """Prueba login con credenciales inválidas"""
        # Crear usuario
        register_data = {
            'nombre': 'Usuario Test',
            'email': 'valid@example.com',
            'password': 'password123',
            'rol': 'pm'
        }
        
        client.post('/api/auth/register',
                   data=json.dumps(register_data),
                   content_type='application/json')
        
        # Login con contraseña incorrecta
        login_data = {
            'email': 'valid@example.com',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        
        # Login con email inexistente
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_register_validation(self, client):
        """Prueba validaciones en el registro"""
        # Registro sin nombre
        register_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'rol': 'pm'
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(register_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        
        # Registro sin email
        register_data = {
            'nombre': 'Test User',
            'password': 'password123',
            'rol': 'pm'
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(register_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        
        # Registro con rol inválido
        register_data = {
            'nombre': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'rol': 'invalid_role'
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(register_data),
                             content_type='application/json')
        
        assert response.status_code == 400

