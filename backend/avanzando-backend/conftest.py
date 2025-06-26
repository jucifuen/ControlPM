import pytest
import os
import sys
from src.main import app
from src.models.user import db

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

@pytest.fixture
def client():
    """Fixture para cliente de pruebas Flask"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    """Fixture para headers de autenticación"""
    # Crear usuario de prueba
    response = client.post('/api/auth/register', json={
        'nombre': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass123',
        'rol': 'administrador'
    })
    
    # Hacer login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_project_data():
    """Fixture con datos de proyecto de prueba"""
    return {
        'nombre': 'Proyecto de Prueba',
        'descripcion': 'Descripción del proyecto de prueba',
        'cliente_id': 1,
        'presupuesto_estimado': 100000,
        'fecha_inicio': '2024-01-01',
        'fecha_fin_estimada': '2024-12-31'
    }

