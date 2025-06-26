import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.main import app
from src.models.user import db
import json

with app.test_client() as client:
    with app.app_context():
        db.create_all()
        
        # Simular el setup_user_and_token de las pruebas
        print("=== Registrando usuario administrador ===")
        register_admin_data = {
            'nombre': 'Admin Projects Test',
            'email': 'admin_projects@example.com',
            'password': 'password123',
            'rol': 'administrador'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(register_admin_data),
                             content_type='application/json')
        print('Register admin response:', response.status_code, response.get_json())
        
        print("\n=== Login de usuario administrador ===")
        login_admin_data = {
            'email': 'admin_projects@example.com',
            'password': 'password123'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_admin_data),
                             content_type='application/json')
        print('Login admin response:', response.status_code, response.get_json())
        
        if response.status_code == 200:
            admin_token = response.get_json()['token']
            print('Admin token:', admin_token[:50] + '...')
            
            print("\n=== Creando cliente usando token del administrador ===")
            cliente_data = {
                'nombre': 'Cliente E2E',
                'sector': 'Tecnología'
            }
            response = client.post('/api/users',
                                 data=json.dumps(cliente_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {admin_token}'})
            print('Create client response:', response.status_code, response.get_json())
            
            print("\n=== Probando ruta de proyectos ===")
            response = client.get('/api/projects', headers={'Authorization': f'Bearer {admin_token}'})
            print('Get projects response:', response.status_code, response.get_json())
        else:
            print('Login failed, cannot continue')

