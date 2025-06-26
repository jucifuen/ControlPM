import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.main import app
from src.models.user import db
import json

with app.test_client() as client:
    with app.app_context():
        db.create_all()
        
        # Registrar usuario
        register_data = {
            'nombre': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'rol': 'administrador'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(register_data),
                             content_type='application/json')
        print('Register response:', response.status_code, response.get_json())
        
        # Login
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        print('Login response:', response.status_code, response.get_json())
        
        if response.status_code == 200:
            token = response.get_json()['token']
            print('Token:', token[:50] + '...')
            
            # Probar ruta protegida
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get('/api/users', headers=headers)
            print('Protected route response:', response.status_code, response.get_json())
        else:
            print('Login failed, cannot test protected route')

