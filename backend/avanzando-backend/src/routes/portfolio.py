from flask import Blueprint, jsonify, request, make_response
from src.middleware.auth import token_required
from src.models.project import Proyecto
from src.models.user import User
from src.models.kpi import KPI
from src.models.riesgo import Riesgo
from src.models.recurso import Recurso
from datetime import datetime, timedelta
import json
import csv
import io

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolio', methods=['GET'])
@token_required
def get_portfolio_data(current_user):
    """Obtiene datos del portafolio con filtros mejorados"""
    try:
        # Obtener parámetros de filtro
        status_filter = request.args.get('status', 'all')
        client_filter = request.args.get('client', 'all')
        search_term = request.args.get('search', '')
        budget_filter = request.args.get('budget', 'all')
        
        # Query base de proyectos
        query = Proyecto.query
        
        # Aplicar filtros
        if status_filter != 'all':
            query = query.filter(Proyecto.estado == status_filter)
        
        if client_filter != 'all':
            query = query.filter(Proyecto.cliente_id == int(client_filter))
        
        if search_term:
            query = query.filter(Proyecto.nombre.ilike(f'%{search_term}%'))
        
        if budget_filter != 'all':
            if budget_filter == 'low':
                query = query.filter(Proyecto.presupuesto_estimado < 50000)
            elif budget_filter == 'medium':
                query = query.filter(Proyecto.presupuesto_estimado.between(50000, 200000))
            elif budget_filter == 'high':
                query = query.filter(Proyecto.presupuesto_estimado > 200000)
        
        # Obtener proyectos filtrados
        proyectos = query.all()
        
        # Calcular métricas
        total_projects = len(proyectos)
        active_projects = len([p for p in proyectos if p.estado == 'activo'])
        completed_projects = len([p for p in proyectos if p.estado == 'completado'])
        total_budget = sum([p.presupuesto_estimado or 0 for p in proyectos])
        total_spent = sum([p.presupuesto_gastado or 0 for p in proyectos])
        
        # KPIs resumidos
        kpi_summary = []
        for proyecto in proyectos[:5]:  # Top 5 proyectos
            kpis = KPI.query.filter_by(proyecto_id=proyecto.id).all()
            if kpis:
                avg_performance = sum([kpi.valor_actual for kpi in kpis]) / len(kpis)
                kpi_summary.append({
                    'project_name': proyecto.nombre,
                    'performance': round(avg_performance, 2),
                    'kpi_count': len(kpis)
                })
        
        # Resumen de riesgos
        risk_summary = []
        for proyecto in proyectos:
            riesgos = Riesgo.query.filter_by(proyecto_id=proyecto.id).all()
            high_risks = len([r for r in riesgos if r.nivel_impacto == 'alto'])
            if high_risks > 0:
                risk_summary.append({
                    'project_name': proyecto.nombre,
                    'high_risks': high_risks,
                    'total_risks': len(riesgos)
                })
        
        # Utilización de recursos
        resource_utilization = []
        recursos = Recurso.query.all()
        for recurso in recursos[:10]:  # Top 10 recursos
            proyectos_asignados = len([p for p in proyectos if recurso.id in [r.id for r in p.recursos]])
            resource_utilization.append({
                'name': recurso.nombre,
                'projects_assigned': proyectos_asignados,
                'utilization': min(100, (proyectos_asignados / 5) * 100)  # Máximo 5 proyectos por recurso
            })
        
        return jsonify({
            'totalProjects': total_projects,
            'activeProjects': active_projects,
            'completedProjects': completed_projects,
            'totalBudget': total_budget,
            'totalSpent': total_spent,
            'projects': [p.to_dict() for p in proyectos],
            'kpiSummary': kpi_summary,
            'riskSummary': risk_summary,
            'resourceUtilization': resource_utilization,
            'filters_applied': {
                'status': status_filter,
                'client': client_filter,
                'search': search_term,
                'budget': budget_filter
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolio/export', methods=['GET'])
@token_required
def export_portfolio_data(current_user):
    """Exporta datos del portafolio en diferentes formatos"""
    try:
        format_type = request.args.get('format', 'csv')
        
        # Obtener todos los proyectos
        proyectos = Proyecto.query.all()
        
        if format_type == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Headers
            writer.writerow(['ID', 'Nombre', 'Estado', 'Cliente', 'Presupuesto', 'Gastado', 'Progreso', 'Fecha Inicio', 'Fecha Fin'])
            
            # Data
            for proyecto in proyectos:
                writer.writerow([
                    proyecto.id,
                    proyecto.nombre,
                    proyecto.estado,
                    proyecto.cliente.nombre if proyecto.cliente else 'N/A',
                    proyecto.presupuesto_estimado or 0,
                    proyecto.presupuesto_gastado or 0,
                    f"{proyecto.progreso_general}%",
                    proyecto.fecha_inicio.strftime('%Y-%m-%d') if proyecto.fecha_inicio else 'N/A',
                    proyecto.fecha_fin.strftime('%Y-%m-%d') if proyecto.fecha_fin else 'N/A'
                ])
            
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = 'attachment; filename=portfolio-report.csv'
            return response
            
        elif format_type == 'json':
            data = {
                'export_date': datetime.now().isoformat(),
                'total_projects': len(proyectos),
                'projects': [p.to_dict() for p in proyectos]
            }
            
            response = make_response(json.dumps(data, indent=2))
            response.headers['Content-Type'] = 'application/json'
            response.headers['Content-Disposition'] = 'attachment; filename=portfolio-report.json'
            return response
            
        else:
            return jsonify({'error': 'Formato no soportado'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolio/clients', methods=['GET'])
@token_required
def get_portfolio_clients(current_user):
    """Obtiene lista de clientes para filtros"""
    try:
        clientes = User.query.filter_by(rol='cliente').all()
        return jsonify({
            'clients': [{'id': c.id, 'name': c.nombre} for c in clientes]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolio/metrics', methods=['GET'])
@token_required
def get_portfolio_metrics(current_user):
    """Obtiene métricas avanzadas del portafolio"""
    try:
        # Métricas de tiempo
        now = datetime.now()
        last_month = now - timedelta(days=30)
        
        proyectos_nuevos = Proyecto.query.filter(Proyecto.fecha_creacion >= last_month).count()
        proyectos_completados_mes = Proyecto.query.filter(
            Proyecto.estado == 'completado',
            Proyecto.fecha_actualizacion >= last_month
        ).count()
        
        # Métricas de presupuesto
        total_presupuesto = Proyecto.query.with_entities(
            Proyecto.presupuesto_estimado
        ).filter(Proyecto.presupuesto_estimado.isnot(None)).all()
        
        total_gastado = Proyecto.query.with_entities(
            Proyecto.presupuesto_gastado
        ).filter(Proyecto.presupuesto_gastado.isnot(None)).all()
        
        budget_efficiency = 0
        if total_presupuesto and total_gastado:
            total_budget_sum = sum([p[0] for p in total_presupuesto])
            total_spent_sum = sum([p[0] for p in total_gastado])
            budget_efficiency = (total_spent_sum / total_budget_sum) * 100 if total_budget_sum > 0 else 0
        
        return jsonify({
            'new_projects_this_month': proyectos_nuevos,
            'completed_projects_this_month': proyectos_completados_mes,
            'budget_efficiency': round(budget_efficiency, 2),
            'average_project_duration': 45,  # Placeholder - calcular real
            'resource_utilization_avg': 75   # Placeholder - calcular real
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

