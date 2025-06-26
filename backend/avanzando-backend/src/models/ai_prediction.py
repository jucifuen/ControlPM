from src.models.user import db
from datetime import datetime
import enum
import json

class PredictionType(enum.Enum):
    PROJECT_COMPLETION = 'project_completion'
    BUDGET_OVERRUN = 'budget_overrun'
    RISK_PROBABILITY = 'risk_probability'
    RESOURCE_UTILIZATION = 'resource_utilization'
    KPI_FORECAST = 'kpi_forecast'

class PredictionStatus(enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class AIPrediction(db.Model):
    __tablename__ = 'ai_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    prediction_type = db.Column(db.Enum(PredictionType), nullable=False)
    status = db.Column(db.Enum(PredictionStatus), nullable=False, default=PredictionStatus.PENDING)
    input_data = db.Column(db.Text)  # JSON con datos de entrada
    prediction_result = db.Column(db.Text)  # JSON con resultado
    confidence_score = db.Column(db.Float)  # Puntuación de confianza 0-1
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relaciones
    project = db.relationship('Proyecto', backref='ai_predictions')
    
    def set_input_data(self, data):
        """Establece los datos de entrada como JSON"""
        self.input_data = json.dumps(data)
    
    def get_input_data(self):
        """Obtiene los datos de entrada desde JSON"""
        return json.loads(self.input_data) if self.input_data else {}
    
    def set_prediction_result(self, result):
        """Establece el resultado de la predicción como JSON"""
        self.prediction_result = json.dumps(result)
        self.status = PredictionStatus.COMPLETED
        self.completed_at = datetime.utcnow()
    
    def get_prediction_result(self):
        """Obtiene el resultado de la predicción desde JSON"""
        return json.loads(self.prediction_result) if self.prediction_result else {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'prediction_type': self.prediction_type.value,
            'status': self.status.value,
            'input_data': self.get_input_data(),
            'prediction_result': self.get_prediction_result(),
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

# Funciones de IA simuladas (en producción usar modelos reales)
class AIEngine:
    @staticmethod
    def predict_project_completion(project_data):
        """Predice la fecha de finalización del proyecto"""
        # Simulación de predicción basada en progreso actual
        current_progress = project_data.get('progress', 0)
        days_elapsed = project_data.get('days_elapsed', 30)
        
        if current_progress > 0:
            estimated_total_days = (days_elapsed / current_progress) * 100
            remaining_days = estimated_total_days - days_elapsed
        else:
            remaining_days = 90  # Default
        
        return {
            'estimated_completion_days': max(1, int(remaining_days)),
            'completion_probability': min(0.95, 0.6 + (current_progress / 100) * 0.3),
            'risk_factors': ['resource_availability', 'scope_changes'] if current_progress < 50 else []
        }
    
    @staticmethod
    def predict_budget_overrun(project_data):
        """Predice la probabilidad de sobrecosto"""
        budget_used_pct = project_data.get('budget_used_percentage', 0)
        progress_pct = project_data.get('progress_percentage', 0)
        
        if progress_pct > 0:
            burn_rate = budget_used_pct / progress_pct
            projected_total_cost = burn_rate * 100
            overrun_probability = max(0, min(1, (projected_total_cost - 100) / 50))
        else:
            overrun_probability = 0.3  # Default moderate risk
        
        return {
            'overrun_probability': overrun_probability,
            'projected_cost_percentage': min(200, projected_total_cost) if progress_pct > 0 else 100,
            'recommended_actions': [
                'Review resource allocation',
                'Optimize processes',
                'Consider scope reduction'
            ] if overrun_probability > 0.5 else []
        }
    
    @staticmethod
    def predict_risk_impact(risk_data):
        """Predice el impacto de riesgos"""
        probability = risk_data.get('probability', 0.5)
        impact = risk_data.get('impact', 0.5)
        mitigation_effectiveness = risk_data.get('mitigation_effectiveness', 0.3)
        
        adjusted_probability = probability * (1 - mitigation_effectiveness)
        risk_score = adjusted_probability * impact
        
        return {
            'adjusted_probability': adjusted_probability,
            'risk_score': risk_score,
            'priority_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low',
            'mitigation_recommendations': [
                'Increase monitoring frequency',
                'Develop contingency plan',
                'Assign dedicated owner'
            ] if risk_score > 0.6 else []
        }
    
    @staticmethod
    def forecast_kpi_trend(kpi_data):
        """Predice tendencias de KPIs"""
        historical_values = kpi_data.get('historical_values', [])
        target_value = kpi_data.get('target_value', 100)
        
        if len(historical_values) < 2:
            return {'trend': 'insufficient_data', 'forecast': []}
        
        # Cálculo simple de tendencia
        recent_trend = (historical_values[-1] - historical_values[-2]) if len(historical_values) >= 2 else 0
        
        forecast = []
        current_value = historical_values[-1]
        
        for i in range(1, 6):  # Próximos 5 períodos
            projected_value = current_value + (recent_trend * i)
            forecast.append({
                'period': i,
                'projected_value': max(0, projected_value),
                'confidence': max(0.3, 0.9 - (i * 0.1))
            })
        
        return {
            'trend': 'increasing' if recent_trend > 0 else 'decreasing' if recent_trend < 0 else 'stable',
            'trend_strength': abs(recent_trend) / max(1, abs(current_value)),
            'forecast': forecast,
            'target_achievement_probability': min(1, max(0, 0.5 + (current_value - target_value) / target_value))
        }

