import pytest
from datetime import datetime, timedelta
from src.models.user import User, UserRole, db
from src.models.subscription import Subscription, PlanType, SubscriptionStatus

class TestSubscriptionModel:
    """Pruebas unitarias para el modelo Subscription"""
    
    def test_create_free_subscription(self, client):
        """Prueba la creación de una suscripción gratuita"""
        with client.application.app_context():
            # Crear usuario
            user = User(
                nombre='Test User',
                email='test1@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            # Crear suscripción gratuita
            subscription = Subscription(user_id=user.id, plan_type=PlanType.FREE)
            db.session.add(subscription)
            db.session.commit()
            
            assert subscription.id is not None
            assert subscription.user_id == user.id
            assert subscription.plan_type == PlanType.FREE
            assert subscription.status == SubscriptionStatus.ACTIVE
            assert subscription.is_active()
    
    def test_create_pro_subscription_with_trial(self, client):
        """Prueba la creación de una suscripción Pro con trial"""
        with client.application.app_context():
            # Crear usuario
            user = User(
                nombre='Test User',
                email='test2@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            # Crear suscripción Pro (debe iniciar con trial)
            subscription = Subscription(user_id=user.id, plan_type=PlanType.PRO)
            db.session.add(subscription)
            db.session.commit()
            
            assert subscription.plan_type == PlanType.PRO
            assert subscription.status == SubscriptionStatus.TRIAL
            assert subscription.trial_end_date is not None
            assert subscription.trial_end_date > datetime.utcnow()
            assert subscription.is_active()
    
    def test_subscription_limits_free(self, client):
        """Prueba los límites del plan gratuito"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test3@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            subscription = Subscription(user_id=user.id, plan_type=PlanType.FREE)
            db.session.add(subscription)
            db.session.commit()
            
            limits = subscription.get_limits()
            
            assert limits['max_projects'] == 3
            assert limits['max_users_per_project'] == 5
            assert limits['max_kpis_per_project'] == 10
            assert limits['ai_features'] == False
            assert limits['advanced_analytics'] == False
            assert limits['storage_gb'] == 1
    
    def test_subscription_limits_pro(self, client):
        """Prueba los límites del plan Pro"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test4@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            subscription = Subscription(user_id=user.id, plan_type=PlanType.PRO)
            db.session.add(subscription)
            db.session.commit()
            
            limits = subscription.get_limits()
            
            assert limits['max_projects'] == 25
            assert limits['max_users_per_project'] == 25
            assert limits['max_kpis_per_project'] == 50
            assert limits['ai_features'] == True
            assert limits['advanced_analytics'] == True
            assert limits['storage_gb'] == 10
    
    def test_subscription_limits_enterprise(self, client):
        """Prueba los límites del plan Enterprise"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test5@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            subscription = Subscription(user_id=user.id, plan_type=PlanType.ENTERPRISE)
            db.session.add(subscription)
            db.session.commit()
            
            limits = subscription.get_limits()
            
            assert limits['max_projects'] == -1  # Ilimitado
            assert limits['max_users_per_project'] == -1
            assert limits['max_kpis_per_project'] == -1
            assert limits['ai_features'] == True
            assert limits['advanced_analytics'] == True
            assert limits['storage_gb'] == 100
    
    def test_can_create_project(self, client):
        """Prueba la verificación de límites de proyectos"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test6@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            # Plan gratuito con límite de 3 proyectos
            subscription = Subscription(user_id=user.id, plan_type=PlanType.FREE)
            db.session.add(subscription)
            db.session.commit()
            
            # Debe permitir crear proyectos hasta el límite
            assert subscription.can_create_project(0)  # 0 proyectos actuales
            assert subscription.can_create_project(1)  # 1 proyecto actual
            assert subscription.can_create_project(2)  # 2 proyectos actuales
            assert not subscription.can_create_project(3)  # 3 proyectos actuales (límite alcanzado)
            assert not subscription.can_create_project(4)  # Más del límite
    
    def test_ai_features_access(self, client):
        """Prueba el acceso a funcionalidades de IA"""
        with client.application.app_context():
            user1 = User(
                nombre='Test User 1',
                email='test7@example.com',
                rol=UserRole.PM
            )
            user1.set_password('testpass')
            db.session.add(user1)
            
            user2 = User(
                nombre='Test User 2',
                email='test8@example.com',
                rol=UserRole.PM
            )
            user2.set_password('testpass')
            db.session.add(user2)
            db.session.commit()
            
            # Plan gratuito - no debe tener acceso a IA
            free_sub = Subscription(user_id=user1.id, plan_type=PlanType.FREE)
            db.session.add(free_sub)
            
            # Plan Pro - debe tener acceso a IA
            pro_sub = Subscription(user_id=user2.id, plan_type=PlanType.PRO)
            db.session.add(pro_sub)
            db.session.commit()
            
            assert not free_sub.can_use_ai_features()
            assert not free_sub.can_use_advanced_analytics()
            
            assert pro_sub.can_use_ai_features()
            assert pro_sub.can_use_advanced_analytics()
    
    def test_upgrade_to_pro(self, client):
        """Prueba la actualización a plan Pro"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test9@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            # Crear suscripción gratuita
            subscription = Subscription(user_id=user.id, plan_type=PlanType.FREE)
            db.session.add(subscription)
            db.session.commit()
            
            # Actualizar a Pro
            subscription.upgrade_to_pro()
            db.session.commit()
            
            assert subscription.plan_type == PlanType.PRO
            assert subscription.status == SubscriptionStatus.ACTIVE
            assert subscription.end_date is not None
            assert subscription.trial_end_date is None
            assert subscription.is_active()
    
    def test_upgrade_to_enterprise(self, client):
        """Prueba la actualización a plan Enterprise"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test10@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            # Crear suscripción Pro
            subscription = Subscription(user_id=user.id, plan_type=PlanType.PRO)
            db.session.add(subscription)
            db.session.commit()
            
            # Actualizar a Enterprise
            subscription.upgrade_to_enterprise()
            db.session.commit()
            
            assert subscription.plan_type == PlanType.ENTERPRISE
            assert subscription.status == SubscriptionStatus.ACTIVE
            assert subscription.end_date is not None
            assert subscription.trial_end_date is None
            assert subscription.is_active()
    
    def test_subscription_to_dict(self, client):
        """Prueba la serialización de la suscripción"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test11@example.com',
                rol=UserRole.PM
            )
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            subscription = Subscription(user_id=user.id, plan_type=PlanType.PRO)
            db.session.add(subscription)
            db.session.commit()
            
            sub_dict = subscription.to_dict()
            
            assert sub_dict['user_id'] == user.id
            assert sub_dict['plan_type'] == 'pro'
            assert sub_dict['status'] == 'trial'
            assert sub_dict['is_active'] == True
            assert 'limits' in sub_dict
            assert 'id' in sub_dict

