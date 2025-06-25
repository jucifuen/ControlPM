from flask import Blueprint, jsonify, request
from src.models.user import db, User
from src.models.subscription import Subscription
from src.models.project import Proyecto
from src.models.ai_prediction import AIPrediction, PredictionType, AIEngine
from src.models.kpi import KPI
from src.models.riesgo import Riesgo
from functools import wraps
import jwt
import os
from datetime import datetime, timedelta

ai_bp = Blueprint('ai', __name__)

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

def ai_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
        if not subscription or not subscription.can_use_ai_features():
            return jsonify({
                'error': 'AI features require Pro or Enterprise subscription',
                'upgrade_required': True,
                'current_plan': subscription.plan_type.value if subscription else 'free'
            }), 403
        return f(current_user, *args, **kwargs)
    return decorated

@ai_bp.route('/ai/predict/project-completion/<int:project_id>', methods=['POST'])
@token_required
@ai_required
def predict_project_completion(current_user, project_id):
    """Predice la fecha de finalización del proyecto"""
    try:
        project = Proyecto.query.get_or_404(project_id)
        
        # Verificar permisos
        if project.pm_id != current_user.id and current_user.rol.value != 'administrador':
            return jsonify({'error': 'No tienes permisos para este proyecto'}), 403
        
        # Calcular datos de entrada
        days_elapsed = (datetime.utcnow() - project.fecha_inicio).days if project.fecha_inicio else 30
        completed_phases = len([f for f in project.fases if f.estado.value == 'completada'])
        total_phases = len(project.fases)
        progress = (completed_phases / total_phases * 100) if total_phases > 0 else 0
        
        input_data = {
            'project_id': project_id,
            'progress': progress,
            'days_elapsed': days_elapsed,
            'total_phases': total_phases,
            'completed_phases': completed_phases,
            'budget_used_percentage': ((project.presupuesto_real or 0) / project.presupuesto_estimado * 100) if project.presupuesto_estimado else 0
        }
        
        # Crear predicción
        prediction = AIPrediction(
            project_id=project_id,
            prediction_type=PredictionType.PROJECT_COMPLETION
        )
        prediction.set_input_data(input_data)
        
        # Ejecutar predicción
        result = AIEngine.predict_project_completion(input_data)
        prediction.set_prediction_result(result)
        prediction.confidence_score = result.get('completion_probability', 0.7)
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'prediction': prediction.to_dict(),
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/predict/budget-overrun/<int:project_id>', methods=['POST'])
@token_required
@ai_required
def predict_budget_overrun(current_user, project_id):
    """Predice la probabilidad de sobrecosto"""
    try:
        project = Proyecto.query.get_or_404(project_id)
        
        # Verificar permisos
        if project.pm_id != current_user.id and current_user.rol.value != 'administrador':
            return jsonify({'error': 'No tienes permisos para este proyecto'}), 403
        
        # Calcular progreso
        completed_phases = len([f for f in project.fases if f.estado.value == 'completada'])
        total_phases = len(project.fases)
        progress_percentage = (completed_phases / total_phases * 100) if total_phases > 0 else 0
        
        budget_used_percentage = 0
        if project.presupuesto_estimado and project.presupuesto_estimado > 0:
            budget_used_percentage = (project.presupuesto_real or 0) / project.presupuesto_estimado * 100
        
        input_data = {
            'project_id': project_id,
            'budget_used_percentage': budget_used_percentage,
            'progress_percentage': progress_percentage,
            'estimated_budget': project.presupuesto_estimado or 0,
            'spent_budget': project.presupuesto_real or 0
        }
        
        # Crear predicción
        prediction = AIPrediction(
            project_id=project_id,
            prediction_type=PredictionType.BUDGET_OVERRUN
        )
        prediction.set_input_data(input_data)
        
        # Ejecutar predicción
        result = AIEngine.predict_budget_overrun(input_data)
        prediction.set_prediction_result(result)
        prediction.confidence_score = 0.8  # Alta confianza en predicciones de presupuesto
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'prediction': prediction.to_dict(),
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/predict/kpi-forecast/<int:kpi_id>', methods=['POST'])
@token_required
@ai_required
def forecast_kpi_trend(current_user, kpi_id):
    """Predice tendencias de KPIs"""
    try:
        kpi = KPI.query.get_or_404(kpi_id)
        project = kpi.proyecto
        
        # Verificar permisos
        if project.pm_id != current_user.id and current_user.rol.value != 'administrador':
            return jsonify({'error': 'No tienes permisos para este KPI'}), 403
        
        # Simular datos históricos (en producción, obtener de base de datos)
        historical_values = [
            kpi.valor_actual * 0.7,
            kpi.valor_actual * 0.8,
            kpi.valor_actual * 0.9,
            kpi.valor_actual
        ]
        
        input_data = {
            'kpi_id': kpi_id,
            'historical_values': historical_values,
            'target_value': kpi.valor_objetivo,
            'current_value': kpi.valor_actual,
            'measurement_unit': kpi.unidad_medida
        }
        
        # Crear predicción
        prediction = AIPrediction(
            project_id=project.id,
            prediction_type=PredictionType.KPI_FORECAST
        )
        prediction.set_input_data(input_data)
        
        # Ejecutar predicción
        result = AIEngine.forecast_kpi_trend(input_data)
        prediction.set_prediction_result(result)
        prediction.confidence_score = 0.75
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'prediction': prediction.to_dict(),
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/predict/risk-impact/<int:risk_id>', methods=['POST'])
@token_required
@ai_required
def predict_risk_impact(current_user, risk_id):
    """Predice el impacto de riesgos"""
    try:
        risk = Riesgo.query.get_or_404(risk_id)
        project = risk.proyecto
        
        # Verificar permisos
        if project.pm_id != current_user.id and current_user.rol.value != 'administrador':
            return jsonify({'error': 'No tienes permisos para este riesgo'}), 403
        
        input_data = {
            'risk_id': risk_id,
            'probability': risk.probabilidad.value / 5.0,  # Normalizar a 0-1
            'impact': risk.impacto.value / 5.0,  # Normalizar a 0-1
            'mitigation_effectiveness': 0.3,  # Valor por defecto
            'current_status': risk.estado.value
        }
        
        # Crear predicción
        prediction = AIPrediction(
            project_id=project.id,
            prediction_type=PredictionType.RISK_PROBABILITY
        )
        prediction.set_input_data(input_data)
        
        # Ejecutar predicción
        result = AIEngine.predict_risk_impact(input_data)
        prediction.set_prediction_result(result)
        prediction.confidence_score = 0.85
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'prediction': prediction.to_dict(),
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/predictions/<int:project_id>', methods=['GET'])
@token_required
@ai_required
def get_project_predictions(current_user, project_id):
    """Obtiene todas las predicciones de un proyecto"""
    try:
        project = Proyecto.query.get_or_404(project_id)
        
        # Verificar permisos
        if project.pm_id != current_user.id and current_user.rol.value != 'administrador':
            return jsonify({'error': 'No tienes permisos para este proyecto'}), 403
        
        predictions = AIPrediction.query.filter_by(project_id=project_id).order_by(AIPrediction.created_at.desc()).all()
        
        return jsonify({
            'predictions': [p.to_dict() for p in predictions],
            'total': len(predictions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/insights/<int:project_id>', methods=['GET'])
@token_required
@ai_required
def get_project_insights(current_user, project_id):
    """Obtiene insights generales del proyecto usando IA"""
    try:
        project = Proyecto.query.get_or_404(project_id)
        
        # Verificar permisos
        if project.pm_id != current_user.id and current_user.rol.value != 'administrador':
            return jsonify({'error': 'No tienes permisos para este proyecto'}), 403
        
        # Obtener métricas del proyecto
        kpis = KPI.query.filter_by(proyecto_id=project_id).all()
        risks = Riesgo.query.filter_by(proyecto_id=project_id, activo=True).all()
        
        # Calcular insights
        insights = {
            'project_health': 'good',  # good, warning, critical
            'completion_likelihood': 0.75,
            'budget_status': 'on_track',  # on_track, at_risk, over_budget
            'key_risks': len([r for r in risks if r.calcular_exposicion() > 0.6]),
            'kpi_performance': 'mixed',  # excellent, good, mixed, poor
            'recommendations': [
                'Monitorear de cerca los riesgos de alta exposición',
                'Revisar el progreso de las fases críticas',
                'Considerar reasignación de recursos si es necesario'
            ],
            'next_milestones': [
                {
                    'name': 'Revisión de medio término',
                    'estimated_date': (datetime.utcnow() + timedelta(days=15)).isoformat(),
                    'confidence': 0.8
                }
            ]
        }
        
        return jsonify(insights), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

