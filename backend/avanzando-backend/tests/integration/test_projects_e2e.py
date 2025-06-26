import pytest
import json
from datetime import date
from src.models.user import User, UserRole, db

class TestProjectsE2E:
    """Pruebas End-to-End para las APIs de proyectos"""
    
    def setup_user_and_token(self, client):
        """Helper para crear usuario y obtener token"""
        register_data = {
            'nombre': 'PM Test',
            'email': 'pm_projects@example.com',
            'password': 'password123',
            'rol': 'pm'
        }
        
        client.post('/api/auth/register',
                   data=json.dumps(register_data),
                   content_type='application/json')
        
        login_data = {
            'email': 'pm_projects@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        return response.get_json()['token']
    
    def test_create_project_flow(self, client):
        """Prueba el flujo completo de creación de proyecto"""
        token = self.setup_user_and_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear cliente primero
        cliente_data = {
            'nombre': 'Cliente E2E',
            'sector': 'Tecnología'
        }
        
        response = client.post('/api/users',
                             data=json.dumps(cliente_data),
                             content_type='application/json',
                             headers=headers)
        
        assert response.status_code == 201
        cliente_id = response.get_json()['user']['id']
        
        # Crear proyecto
        project_data = {
            'nombre': 'Proyecto E2E Test',
            'descripcion': 'Proyecto para pruebas E2E',
            'cliente_id': cliente_id,
            'presupuesto_estimado': 100000,
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-12-31'
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
        
        return data['project']['id']
    
    def test_get_projects(self, client):
        """Prueba obtener lista de proyectos"""
        token = self.setup_user_and_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear algunos proyectos
        project_id = self.test_create_project_flow(client)
        
        # Obtener lista de proyectos
        response = client.get('/api/projects', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'projects' in data
        assert len(data['projects']) > 0
        
        # Verificar que el proyecto creado está en la lista
        project_names = [p['nombre'] for p in data['projects']]
        assert 'Proyecto E2E Test' in project_names
    
    def test_get_project_by_id(self, client):
        """Prueba obtener proyecto específico por ID"""
        token = self.setup_user_and_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        project_id = self.test_create_project_flow(client)
        
        # Obtener proyecto por ID
        response = client.get(f'/api/projects/{project_id}', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'project' in data
        assert data['project']['id'] == project_id
        assert data['project']['nombre'] == 'Proyecto E2E Test'
    
    def test_update_project(self, client):
        """Prueba actualizar proyecto"""
        token = self.setup_user_and_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        project_id = self.test_create_project_flow(client)
        
        # Actualizar proyecto
        update_data = {
            'nombre': 'Proyecto E2E Actualizado',
            'descripcion': 'Descripción actualizada',
            'estado': 'pausado'
        }
        
        response = client.put(f'/api/projects/{project_id}',
                            data=json.dumps(update_data),
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Proyecto actualizado exitosamente'
        assert data['project']['nombre'] == 'Proyecto E2E Actualizado'
        assert data['project']['estado'] == 'pausado'
    
    def test_delete_project(self, client):
        """Prueba eliminar proyecto"""
        token = self.setup_user_and_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        project_id = self.test_create_project_flow(client)
        
        # Eliminar proyecto
        response = client.delete(f'/api/projects/{project_id}', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Proyecto eliminado exitosamente'
        
        # Verificar que el proyecto ya no existe
        response = client.get(f'/api/projects/{project_id}', headers=headers)
        assert response.status_code == 404
    
    def test_project_phases_flow(self, client):
        """Prueba el flujo completo de fases de proyecto"""
        token = self.setup_user_and_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        project_id = self.test_create_project_flow(client)
        
        # Crear fase
        phase_data = {
            'nombre': 'Fase de Inicio',
            'descripcion': 'Primera fase del proyecto',
            'tipo': 'inicio',
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-03-31'
        }
        
        response = client.post(f'/api/projects/{project_id}/phases',
                             data=json.dumps(phase_data),
                             content_type='application/json',
                             headers=headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Fase creada exitosamente'
        phase_id = data['phase']['id']
        
        # Obtener fases del proyecto
        response = client.get(f'/api/projects/{project_id}/phases', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'phases' in data
        assert len(data['phases']) == 1
        assert data['phases'][0]['nombre'] == 'Fase de Inicio'
        
        # Actualizar fase
        update_phase_data = {
            'avance': 50,
            'descripcion': 'Fase actualizada'
        }
        
        response = client.put(f'/api/projects/{project_id}/phases/{phase_id}',
                            data=json.dumps(update_phase_data),
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['phase']['avance'] == 50
    
    def test_unauthorized_access(self, client):
        """Prueba acceso no autorizado a APIs de proyectos"""
        # Intentar acceder sin token
        response = client.get('/api/projects')
        assert response.status_code == 401
        
        response = client.post('/api/projects',
                             data=json.dumps({'nombre': 'Test'}),
                             content_type='application/json')
        assert response.status_code == 401
        
        # Intentar con token inválido
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.get('/api/projects', headers=headers)
        assert response.status_code == 401

