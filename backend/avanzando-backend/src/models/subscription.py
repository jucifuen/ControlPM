from src.models.user import db
from datetime import datetime, timedelta
import enum

class PlanType(enum.Enum):
    FREE = 'free'
    PRO = 'pro'
    ENTERPRISE = 'enterprise'

class SubscriptionStatus(enum.Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    CANCELLED = 'cancelled'
    TRIAL = 'trial'

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_type = db.Column(db.Enum(PlanType), nullable=False, default=PlanType.FREE)
    status = db.Column(db.Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.ACTIVE)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    trial_end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', backref='subscription')
    
    def __init__(self, user_id, plan_type=PlanType.FREE):
        self.user_id = user_id
        self.plan_type = plan_type
        if plan_type == PlanType.FREE:
            self.status = SubscriptionStatus.ACTIVE
        else:
            # Iniciar con trial de 14 días para planes pagos
            self.status = SubscriptionStatus.TRIAL
            self.trial_end_date = datetime.utcnow() + timedelta(days=14)
    
    def is_active(self):
        """Verifica si la suscripción está activa"""
        if self.status == SubscriptionStatus.CANCELLED:
            return False
        if self.status == SubscriptionStatus.EXPIRED:
            return False
        if self.status == SubscriptionStatus.TRIAL:
            return datetime.utcnow() <= self.trial_end_date
        if self.end_date and datetime.utcnow() > self.end_date:
            self.status = SubscriptionStatus.EXPIRED
            db.session.commit()
            return False
        return True
    
    def get_limits(self):
        """Retorna los límites según el plan"""
        limits = {
            PlanType.FREE: {
                'max_projects': 3,
                'max_users_per_project': 5,
                'max_kpis_per_project': 10,
                'max_risks_per_project': 15,
                'max_resources_per_project': 20,
                'ai_features': False,
                'advanced_analytics': False,
                'export_formats': ['PDF'],
                'integrations': [],
                'storage_gb': 1
            },
            PlanType.PRO: {
                'max_projects': 25,
                'max_users_per_project': 25,
                'max_kpis_per_project': 50,
                'max_risks_per_project': 100,
                'max_resources_per_project': 200,
                'ai_features': True,
                'advanced_analytics': True,
                'export_formats': ['PDF', 'Excel', 'CSV'],
                'integrations': ['Slack', 'Teams', 'Email'],
                'storage_gb': 10
            },
            PlanType.ENTERPRISE: {
                'max_projects': -1,  # Ilimitado
                'max_users_per_project': -1,
                'max_kpis_per_project': -1,
                'max_risks_per_project': -1,
                'max_resources_per_project': -1,
                'ai_features': True,
                'advanced_analytics': True,
                'export_formats': ['PDF', 'Excel', 'CSV', 'PowerBI'],
                'integrations': ['Slack', 'Teams', 'Email', 'Jira', 'Trello', 'Asana'],
                'storage_gb': 100
            }
        }
        return limits.get(self.plan_type, limits[PlanType.FREE])
    
    def can_create_project(self, current_count):
        """Verifica si puede crear un nuevo proyecto"""
        if not self.is_active():
            return False
        limits = self.get_limits()
        max_projects = limits['max_projects']
        return max_projects == -1 or current_count < max_projects
    
    def can_use_ai_features(self):
        """Verifica si puede usar funcionalidades de IA"""
        return self.is_active() and self.get_limits()['ai_features']
    
    def can_use_advanced_analytics(self):
        """Verifica si puede usar analytics avanzados"""
        return self.is_active() and self.get_limits()['advanced_analytics']
    
    def upgrade_to_pro(self):
        """Actualiza a plan Pro"""
        self.plan_type = PlanType.PRO
        self.status = SubscriptionStatus.ACTIVE
        self.start_date = datetime.utcnow()
        self.end_date = datetime.utcnow() + timedelta(days=30)  # Mensual
        self.trial_end_date = None
        self.updated_at = datetime.utcnow()
    
    def upgrade_to_enterprise(self):
        """Actualiza a plan Enterprise"""
        self.plan_type = PlanType.ENTERPRISE
        self.status = SubscriptionStatus.ACTIVE
        self.start_date = datetime.utcnow()
        self.end_date = datetime.utcnow() + timedelta(days=365)  # Anual
        self.trial_end_date = None
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_type': self.plan_type.value,
            'status': self.status.value,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'trial_end_date': self.trial_end_date.isoformat() if self.trial_end_date else None,
            'is_active': self.is_active(),
            'limits': self.get_limits()
        }

