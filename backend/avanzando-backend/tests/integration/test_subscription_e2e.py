import pytest
import json
from src.models.user import User, UserRole, db
from src.models.subscription import Subscription, PlanType

class TestSubscriptionE2E:
    """Pruebas End-to-End para las APIs de suscripción"""
    
    def setup_user_and_token(self, client, email="sub_test@example.com"):
        """Helper para crear usuario y obtener token"""
        register_data = {
            'nombre': 'Usuario Suscripción',
            'email': email,
            'password': 'password123',
            'rol': 'pm'
        }
        
        client.post('/api/auth/register',
                   data=json.dumps(register_data),
                   content_type='application/json')
        
        login_data = {
            'email': email,
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        return response.get_json()['token']
    
    def test_get_subscription_info(self, client):
        """Prueba obtener información de suscripción"""
        token = self.setup_user_and_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get('/api/subscription', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'subscription' in data
        assert data['subscription']['plan_type'] == 'free'
        assert data['subscription']['is_active'] == True
        assert 'limits' in data['subscription']
    
    def test_upgrade_to_pro(self, client):
        """Prueba upgrade a plan Pro"""
        token = self.setup_user_and_token(client, "pro_test@example.com")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Upgrade a Pro
        upgrade_data = {
            'plan_type': 'pro',
            'payment_method': 'credit_card'
        }
        
        response = client.post('/api/subscription/upgrade',
                             data=json.dumps(upgrade_data),
                             content_type='application/json',
                             headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Suscripción actualizada exitosamente'
        assert data['subscription']['plan_type'] == 'pro'
        assert data['subscription']['status'] == 'active'
        
        # Verificar nuevos límites
        limits = data['subscription']['limits']
        assert limits['max_projects'] == 25
        assert limits['ai_features'] == True
    
    def test_upgrade_to_enterprise(self, client):
        """Prueba upgrade a plan Enterprise"""
        token = self.setup_user_and_token(client, "enterprise_test@example.com")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Upgrade a Enterprise
        upgrade_data = {
            'plan_type': 'enterprise',
            'payment_method': 'credit_card'
        }
        
        response = client.post('/api/subscription/upgrade',
                             data=json.dumps(upgrade_data),
                             content_type='application/json',
                             headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['subscription']['plan_type'] == 'enterprise'
        
        # Verificar límites ilimitados
        limits = data['subscription']['limits']
        assert limits['max_projects'] == -1  # Ilimitado
        assert limits['ai_features'] == True
        assert limits['advanced_analytics'] == True
    
    def test_check_limits(self, client):
        """Prueba verificación de límites"""
        token = self.setup_user_and_token(client, "limits_test@example.com")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Verificar si puede crear proyecto (plan gratuito)
        response = client.get('/api/subscription/check-limits?action=create_project&current_count=0',
                            headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['allowed'] == True
        
        # Verificar límite alcanzado
        response = client.get('/api/subscription/check-limits?action=create_project&current_count=3',
                            headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['allowed'] == False
        assert 'message' in data
    
    def test_ai_features_access(self, client):
        """Prueba acceso a funcionalidades de IA"""
        # Usuario con plan gratuito
        token_free = self.setup_user_and_token(client, "ai_free@example.com")
        headers_free = {'Authorization': f'Bearer {token_free}'}
        
        response = client.get('/api/subscription/ai-access', headers=headers_free)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['ai_features'] == False
        assert data['advanced_analytics'] == False
        
        # Usuario con plan Pro
        token_pro = self.setup_user_and_token(client, "ai_pro@example.com")
        headers_pro = {'Authorization': f'Bearer {token_pro}'}
        
        # Upgrade a Pro primero
        upgrade_data = {'plan_type': 'pro', 'payment_method': 'credit_card'}
        client.post('/api/subscription/upgrade',
                   data=json.dumps(upgrade_data),
                   content_type='application/json',
                   headers=headers_pro)
        
        response = client.get('/api/subscription/ai-access', headers=headers_pro)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['ai_features'] == True
        assert data['advanced_analytics'] == True
    
    def test_subscription_history(self, client):
        """Prueba historial de suscripciones"""
        token = self.setup_user_and_token(client, "history_test@example.com")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Hacer upgrade para generar historial
        upgrade_data = {'plan_type': 'pro', 'payment_method': 'credit_card'}
        client.post('/api/subscription/upgrade',
                   data=json.dumps(upgrade_data),
                   content_type='application/json',
                   headers=headers)
        
        # Obtener historial
        response = client.get('/api/subscription/history', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'history' in data
        assert len(data['history']) > 0
        
        # Verificar que contiene el upgrade
        plan_types = [h['plan_type'] for h in data['history']]
        assert 'pro' in plan_types
    
    def test_invalid_upgrade(self, client):
        """Prueba upgrade inválido"""
        token = self.setup_user_and_token(client, "invalid_test@example.com")
        headers = {'Authorization': f'Bearer {token}'}
        
        # Intentar upgrade a plan inválido
        upgrade_data = {
            'plan_type': 'invalid_plan',
            'payment_method': 'credit_card'
        }
        
        response = client.post('/api/subscription/upgrade',
                             data=json.dumps(upgrade_data),
                             content_type='application/json',
                             headers=headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_unauthorized_subscription_access(self, client):
        """Prueba acceso no autorizado a APIs de suscripción"""
        # Sin token
        response = client.get('/api/subscription')
        assert response.status_code == 401
        
        response = client.post('/api/subscription/upgrade',
                             data=json.dumps({'plan_type': 'pro'}),
                             content_type='application/json')
        assert response.status_code == 401
        
        # Token inválido
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.get('/api/subscription', headers=headers)
        assert response.status_code == 401

