import json
from datetime import date
from src.models.user import User, UserRole, db

class TestProjectsE2E:
    """Pruebas End-to-End para las APIs de proyectos"""
    
    def setup_user_and_token(self, client, test_name="default"):
        """Helper para crear usuario administrador, cliente y obtener token"""
        # Usar email único basado en el nombre de la prueba
        unique_email = f'admin_projects_{test_name}@example.com'
        
        # Registrar usuario administrador
        register_admin_data = {
            'nombre': f'Admin Projects Test {test_name}',
            'email': unique_email,
            'password': 'password123',
            'rol': 'administrador'
        }
        client.post('/api/auth/register',
                   data=json.dumps(register_admin_data),
                   content_type='application/json')
        
        # Login de usuario administrador
        login_admin_data = {
            'email': unique_email,
            'password': 'password123'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_admin_data),
                             content_type='application/json')
        admin_token = response.get_json()['token']

        # Crear cliente usando el token del administrador
        cliente_data = {
            'nombre': f'Cliente E2E {test_name}',
            'sector': 'Tecnología'
        }
        response = client.post('/api/users',
                             data=json.dumps(cliente_data),
                             content_type='application/json',
                             headers={'Authorization': f'Bearer {admin_token}'})
        assert response.status_code == 201
        cliente_id = response.get_json()['user']['id']
        
        return admin_token, cliente_id
    
    def test_create_project_flow(self, client):
        """Prueba el flujo completo de creación de proyecto"""
        token, cliente_id = self.setup_user_and_token(client, "create_project")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Crear proyecto
        project_data = {
            "nombre": "Proyecto E2E Test",
            "descripcion": "Proyecto para pruebas E2E",
            "cliente_id": cliente_id,
            "presupuesto_estimado": 100000,
            "fecha_inicio": "2024-01-01",
            "fecha_fin": "2024-12-31"
        }
        
        response = client.post('/api/projects',
                             data=json.dumps(project_data),
                             content_type='application/json',
                             headers=headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Proyecto creado exitosamente'
        assert 'project' in data
        assert data['project']['nombre'] == 'Proyecto E2E Test'
        assert data['project']['estado'] == 'activo'
    
    def test_get_projects(self, client):
        """Prueba obtener lista de proyectos"""
        token, _ = self.setup_user_and_token(client, "get_projects")
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get('/api/projects', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'projects' in data
        assert isinstance(data['projects'], list)
    
    def test_get_project_by_id(self, client):
        """Prueba obtener proyecto específico por ID"""
        token, cliente_id = self.setup_user_and_token(client, "get_project_by_id")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear proyecto primero
        project_data = {
            "nombre": "Proyecto para obtener",
            "descripcion": "Proyecto para prueba de obtención",
            "cliente_id": cliente_id,
            "presupuesto_estimado": 50000
        }
        
        response = client.post('/api/projects',
                             data=json.dumps(project_data),
                             content_type='application/json',
                             headers=headers)
        project_id = response.get_json()['project']['id']
        
        # Obtener proyecto por ID
        response = client.get(f'/api/projects/{project_id}', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'project' in data
        assert data['project']['nombre'] == 'Proyecto para obtener'
        assert 'fases' in data['project']
    
    def test_update_project(self, client):
        """Prueba actualizar proyecto"""
        token, cliente_id = self.setup_user_and_token(client, "update_project")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear proyecto primero
        project_data = {
            "nombre": "Proyecto para actualizar",
            "descripcion": "Proyecto para prueba de actualización",
            "cliente_id": cliente_id,
            "presupuesto_estimado": 75000
        }
        
        response = client.post('/api/projects',
                             data=json.dumps(project_data),
                             content_type='application/json',
                             headers=headers)
        project_id = response.get_json()['project']['id']
        
        # Actualizar proyecto
        update_data = {
            "nombre": "Proyecto actualizado",
            "descripcion": "Descripción actualizada",
            "presupuesto_estimado": 100000
        }
        
        response = client.put(f'/api/projects/{project_id}',
                            data=json.dumps(update_data),
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Proyecto actualizado exitosamente'
        assert data['project']['nombre'] == 'Proyecto actualizado'
    
    def test_delete_project(self, client):
        """Prueba eliminar proyecto"""
        token, cliente_id = self.setup_user_and_token(client, "delete_project")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear proyecto primero
        project_data = {
            "nombre": "Proyecto para eliminar",
            "descripcion": "Proyecto para prueba de eliminación",
            "cliente_id": cliente_id,
            "presupuesto_estimado": 25000
        }
        
        response = client.post('/api/projects',
                             data=json.dumps(project_data),
                             content_type='application/json',
                             headers=headers)
        project_id = response.get_json()['project']['id']
        
        # Eliminar proyecto
        response = client.delete(f'/api/projects/{project_id}', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Proyecto eliminado exitosamente'
    
    def test_project_phases_flow(self, client):
        """Prueba flujo de fases de proyecto"""
        token, cliente_id = self.setup_user_and_token(client, "project_phases")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear proyecto
        project_data = {
            "nombre": "Proyecto con fases",
            "descripcion": "Proyecto para prueba de fases",
            "cliente_id": cliente_id,
            "presupuesto_estimado": 80000
        }
        
        response = client.post('/api/projects',
                             data=json.dumps(project_data),
                             content_type='application/json',
                             headers=headers)
        project_id = response.get_json()['project']['id']
        
        # Obtener proyecto con fases
        response = client.get(f'/api/projects/{project_id}', headers=headers)
        project_data = response.get_json()['project']
        
        assert len(project_data['fases']) == 5  # 5 fases por defecto
        
        # Avanzar primera fase
        phase_id = project_data['fases'][0]['id']
        advance_data = {"avance": 50}
        
        response = client.post(f'/api/projects/{project_id}/phases/{phase_id}/advance',
                             data=json.dumps(advance_data),
                             content_type='application/json',
                             headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Fase actualizada exitosamente'
        assert data['fase']['avance'] == 50

