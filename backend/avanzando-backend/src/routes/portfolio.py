from flask import Blueprint, jsonify, request
from src.models.user import db, User
from src.models.project import Proyecto
from src.models.kpi import KPI
from src.models.riesgo import Riesgo
from src.models.recurso import Recurso
from functools import wraps
import jwt
import os
from sqlalchemy import func

portfolio_bp = Blueprint('portfolio', __name__)

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

@portfolio_bp.route('/portfolio', methods=['GET'])
@token_required
def get_portfolio_data(current_user):
    try:
        # Obtener proyectos según el rol del usuario
        if current_user.rol.value == 'administrador':
            projects = Proyecto.query.all()
        else:
            projects = Proyecto.query.filter_by(pm_id=current_user.id).all()
        
        # Calcular métricas del portafolio
        total_projects = len(projects)
        active_projects = len([p for p in projects if p.estado.value == 'activo'])
        completed_projects = len([p for p in projects if p.estado.value == 'completado'])
        
        total_budget = sum([p.presupuesto_estimado or 0 for p in projects])
        total_spent = sum([p.presupuesto_real or 0 for p in projects])
        
        # Obtener KPIs consolidados
        kpi_summary = []
        for project in projects:
            kpis = KPI.query.filter_by(proyecto_id=project.id).all()
            for kpi in kpis:
                kpi_summary.append({
                    'proyecto': project.nombre,
                    'nombre': kpi.nombre,
                    'valor_actual': kpi.valor_actual,
                    'valor_objetivo': kpi.valor_objetivo,
                    'estado': kpi.estado.value
                })
        
        # Obtener riesgos activos
        risk_summary = []
        for project in projects:
            risks = Riesgo.query.filter_by(proyecto_id=project.id, activo=True).all()
            for risk in risks:
                if risk.estado.value in ['identificado', 'en_mitigacion']:
                    risk_summary.append({
                        'proyecto': project.nombre,
                        'descripcion': risk.descripcion,
                        'exposicion': risk.calcular_exposicion(),
                        'estado': risk.estado.value
                    })
        
        # Obtener utilización de recursos
        resource_utilization = []
        for project in projects:
            resources = Recurso.query.filter_by(proyecto_id=project.id, activo=True).all()
            for resource in resources:
                resource_utilization.append({
                    'proyecto': project.nombre,
                    'nombre': resource.nombre,
                    'tipo': resource.tipo.value,
                    'disponibilidad': resource.disponibilidad.value,
                    'costo_total': resource.costo_total
                })
        
        # Preparar datos de proyectos para el frontend
        projects_data = []
        for project in projects:
            # Calcular progreso basado en fases completadas
            fases_completadas = len([f for f in project.fases if f.estado.value == 'completada'])
            total_fases = len(project.fases)
            progreso = (fases_completadas / total_fases * 100) if total_fases > 0 else 0
            
            projects_data.append({
                'id': project.id,
                'nombre': project.nombre,
                'descripcion': project.descripcion,
                'estado': project.estado.value,
                'presupuesto_estimado': project.presupuesto_estimado,
                'presupuesto_real': project.presupuesto_real,
                'progreso': progreso,
                'cliente_nombre': getattr(project.cliente, 'nombre', 'N/A') if project.cliente else 'N/A'
            })
        
        portfolio_data = {
            'totalProjects': total_projects,
            'activeProjects': active_projects,
            'completedProjects': completed_projects,
            'totalBudget': total_budget,
            'totalSpent': total_spent,
            'projects': projects_data,
            'kpiSummary': kpi_summary,
            'riskSummary': risk_summary,
            'resourceUtilization': resource_utilization
        }
        
        return jsonify(portfolio_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolio/analytics', methods=['GET'])
@token_required
def get_portfolio_analytics(current_user):
    try:
        # Obtener proyectos según el rol del usuario
        if current_user.rol.value == 'administrador':
            projects = Proyecto.query.all()
        else:
            projects = Proyecto.query.filter_by(pm_id=current_user.id).all()
        
        # Análisis temporal de proyectos
        monthly_data = db.session.query(
            func.strftime('%Y-%m', Proyecto.fecha_inicio).label('month'),
            func.count(Proyecto.id).label('count')
        ).filter(Proyecto.id.in_([p.id for p in projects])).group_by('month').all()
        
        # Análisis de presupuesto por proyecto
        budget_analysis = []
        for project in projects:
            if project.presupuesto_estimado:
                variance = ((project.presupuesto_real or 0) - project.presupuesto_estimado) / project.presupuesto_estimado * 100
                budget_analysis.append({
                    'proyecto': project.nombre,
                    'presupuestado': project.presupuesto_estimado,
                    'gastado': project.presupuesto_real or 0,
                    'varianza': variance
                })
        
        # Top riesgos por exposición
        top_risks = []
        for project in projects:
            risks = Riesgo.query.filter_by(proyecto_id=project.id, activo=True).all()
            for risk in risks:
                top_risks.append({
                    'proyecto': project.nombre,
                    'descripcion': risk.descripcion,
                    'exposicion': risk.calcular_exposicion()
                })
        
        top_risks.sort(key=lambda x: x['exposicion'], reverse=True)
        top_risks = top_risks[:10]  # Top 10 riesgos
        
        analytics_data = {
            'monthlyProjects': [{'month': m[0], 'count': m[1]} for m in monthly_data],
            'budgetAnalysis': budget_analysis,
            'topRisks': top_risks
        }
        
        return jsonify(analytics_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

