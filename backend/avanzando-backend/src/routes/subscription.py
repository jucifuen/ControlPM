from flask import Blueprint, jsonify, request
from src.models.user import db, User
from src.models.subscription import Subscription, PlanType, SubscriptionStatus
from src.models.project import Proyecto
from functools import wraps
import jwt
import os

subscription_bp = Blueprint('subscription', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, os.environ.get('SECRET_KEY', 'dev-secret-key'), algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@subscription_bp.route('/subscription', methods=['GET'])
@token_required
def get_subscription(current_user):
    """Obtiene la suscripción actual del usuario"""
    try:
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
        
        if not subscription:
            # Crear suscripción gratuita por defecto
            subscription = Subscription(user_id=current_user.id, plan_type=PlanType.FREE)
            db.session.add(subscription)
            db.session.commit()
        
        return jsonify(subscription.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/upgrade', methods=['POST'])
@token_required
def upgrade_subscription(current_user):
    """Actualiza la suscripción del usuario"""
    try:
        data = request.get_json()
        plan_type = data.get('plan_type')
        
        if plan_type not in ['pro', 'enterprise']:
            return jsonify({'error': 'Invalid plan type'}), 400
        
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
        
        if not subscription:
            subscription = Subscription(user_id=current_user.id)
            db.session.add(subscription)
        
        if plan_type == 'pro':
            subscription.upgrade_to_pro()
        elif plan_type == 'enterprise':
            subscription.upgrade_to_enterprise()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully upgraded to {plan_type}',
            'subscription': subscription.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/limits', methods=['GET'])
@token_required
def get_subscription_limits(current_user):
    """Obtiene los límites de la suscripción actual"""
    try:
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
        
        if not subscription:
            subscription = Subscription(user_id=current_user.id, plan_type=PlanType.FREE)
            db.session.add(subscription)
            db.session.commit()
        
        # Obtener uso actual
        project_count = Proyecto.query.filter_by(pm_id=current_user.id).count()
        
        limits = subscription.get_limits()
        usage = {
            'current_projects': project_count,
            'can_create_project': subscription.can_create_project(project_count),
            'can_use_ai': subscription.can_use_ai_features(),
            'can_use_advanced_analytics': subscription.can_use_advanced_analytics()
        }
        
        return jsonify({
            'limits': limits,
            'usage': usage,
            'subscription': subscription.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/subscription/check-limit/<feature>', methods=['GET'])
@token_required
def check_feature_limit(current_user, feature):
    """Verifica si el usuario puede usar una funcionalidad específica"""
    try:
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
        
        if not subscription:
            subscription = Subscription(user_id=current_user.id, plan_type=PlanType.FREE)
            db.session.add(subscription)
            db.session.commit()
        
        allowed = False
        message = ""
        
        if feature == 'create_project':
            project_count = Proyecto.query.filter_by(pm_id=current_user.id).count()
            allowed = subscription.can_create_project(project_count)
            if not allowed:
                limits = subscription.get_limits()
                message = f"Has alcanzado el límite de {limits['max_projects']} proyectos. Actualiza tu plan para crear más proyectos."
        
        elif feature == 'ai_features':
            allowed = subscription.can_use_ai_features()
            if not allowed:
                message = "Las funcionalidades de IA están disponibles solo en planes Pro y Enterprise."
        
        elif feature == 'advanced_analytics':
            allowed = subscription.can_use_advanced_analytics()
            if not allowed:
                message = "Los análisis avanzados están disponibles solo en planes Pro y Enterprise."
        
        else:
            return jsonify({'error': 'Unknown feature'}), 400
        
        return jsonify({
            'allowed': allowed,
            'message': message,
            'current_plan': subscription.plan_type.value,
            'upgrade_required': not allowed
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscription_bp.route('/plans', methods=['GET'])
def get_available_plans():
    """Obtiene información de todos los planes disponibles"""
    try:
        plans = {
            'free': {
                'name': 'Gratuito',
                'price': 0,
                'currency': 'USD',
                'billing': 'monthly',
                'features': [
                    'Hasta 3 proyectos',
                    '5 usuarios por proyecto',
                    '10 KPIs por proyecto',
                    '15 riesgos por proyecto',
                    '20 recursos por proyecto',
                    'Exportación PDF',
                    '1 GB de almacenamiento'
                ],
                'limits': {
                    'max_projects': 3,
                    'max_users_per_project': 5,
                    'max_kpis_per_project': 10,
                    'max_risks_per_project': 15,
                    'max_resources_per_project': 20,
                    'ai_features': False,
                    'advanced_analytics': False,
                    'storage_gb': 1
                }
            },
            'pro': {
                'name': 'Profesional',
                'price': 29,
                'currency': 'USD',
                'billing': 'monthly',
                'features': [
                    'Hasta 25 proyectos',
                    '25 usuarios por proyecto',
                    '50 KPIs por proyecto',
                    '100 riesgos por proyecto',
                    '200 recursos por proyecto',
                    'Funcionalidades de IA',
                    'Análisis avanzados',
                    'Exportación PDF, Excel, CSV',
                    'Integraciones (Slack, Teams)',
                    '10 GB de almacenamiento'
                ],
                'limits': {
                    'max_projects': 25,
                    'max_users_per_project': 25,
                    'max_kpis_per_project': 50,
                    'max_risks_per_project': 100,
                    'max_resources_per_project': 200,
                    'ai_features': True,
                    'advanced_analytics': True,
                    'storage_gb': 10
                }
            },
            'enterprise': {
                'name': 'Empresarial',
                'price': 99,
                'currency': 'USD',
                'billing': 'monthly',
                'features': [
                    'Proyectos ilimitados',
                    'Usuarios ilimitados',
                    'KPIs ilimitados',
                    'Riesgos ilimitados',
                    'Recursos ilimitados',
                    'Funcionalidades de IA avanzadas',
                    'Análisis predictivos',
                    'Todas las exportaciones',
                    'Todas las integraciones',
                    '100 GB de almacenamiento',
                    'Soporte prioritario'
                ],
                'limits': {
                    'max_projects': -1,
                    'max_users_per_project': -1,
                    'max_kpis_per_project': -1,
                    'max_risks_per_project': -1,
                    'max_resources_per_project': -1,
                    'ai_features': True,
                    'advanced_analytics': True,
                    'storage_gb': 100
                }
            }
        }
        
        return jsonify(plans), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

