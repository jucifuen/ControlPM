from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.kpi import KPI, TipoKPI, EstadoKPI
from src.models.project import Proyecto
from datetime import datetime

kpis_bp = Blueprint('kpis', __name__)

@kpis_bp.route('/api/kpis', methods=['GET'])
def get_kpis():
    try:
        proyecto_id = request.args.get('proyecto_id')
        
        query = KPI.query.filter_by(activo=True)
        if proyecto_id:
            query = query.filter_by(proyecto_id=proyecto_id)
        
        kpis = query.all()
        return jsonify([kpi.to_dict() for kpi in kpis])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kpis_bp.route('/api/kpis', methods=['POST'])
def create_kpi():
    try:
        data = request.get_json()
        
        # Validar que el proyecto existe
        proyecto = Proyecto.query.get(data['proyecto_id'])
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        kpi = KPI(
            proyecto_id=data['proyecto_id'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            tipo=TipoKPI(data['tipo']),
            valor_objetivo=float(data['valor_objetivo']),
            valor_actual=float(data.get('valor_actual', 0)),
            unidad_medida=data['unidad_medida'],
            umbral_amarillo=float(data['umbral_amarillo']),
            umbral_rojo=float(data['umbral_rojo'])
        )
        
        kpi.calcular_estado()
        
        db.session.add(kpi)
        db.session.commit()
        
        return jsonify({
            'message': 'KPI creado exitosamente',
            'kpi': kpi.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@kpis_bp.route('/api/kpis/<int:kpi_id>', methods=['GET'])
def get_kpi(kpi_id):
    try:
        kpi = KPI.query.get_or_404(kpi_id)
        return jsonify(kpi.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kpis_bp.route('/api/kpis/<int:kpi_id>', methods=['PUT'])
def update_kpi(kpi_id):
    try:
        kpi = KPI.query.get_or_404(kpi_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            kpi.nombre = data['nombre']
        if 'descripcion' in data:
            kpi.descripcion = data['descripcion']
        if 'tipo' in data:
            kpi.tipo = TipoKPI(data['tipo'])
        if 'valor_objetivo' in data:
            kpi.valor_objetivo = float(data['valor_objetivo'])
        if 'valor_actual' in data:
            kpi.valor_actual = float(data['valor_actual'])
        if 'unidad_medida' in data:
            kpi.unidad_medida = data['unidad_medida']
        if 'umbral_amarillo' in data:
            kpi.umbral_amarillo = float(data['umbral_amarillo'])
        if 'umbral_rojo' in data:
            kpi.umbral_rojo = float(data['umbral_rojo'])
        
        kpi.calcular_estado()
        kpi.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'KPI actualizado exitosamente',
            'kpi': kpi.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@kpis_bp.route('/api/kpis/<int:kpi_id>', methods=['DELETE'])
def delete_kpi(kpi_id):
    try:
        kpi = KPI.query.get_or_404(kpi_id)
        kpi.activo = False
        kpi.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'KPI eliminado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@kpis_bp.route('/api/kpis/dashboard/<int:proyecto_id>', methods=['GET'])
def get_kpis_dashboard(proyecto_id):
    try:
        kpis = KPI.query.filter_by(proyecto_id=proyecto_id, activo=True).all()
        
        # Estadísticas generales
        total_kpis = len(kpis)
        kpis_verdes = len([k for k in kpis if k.estado == EstadoKPI.VERDE])
        kpis_amarillos = len([k for k in kpis if k.estado == EstadoKPI.AMARILLO])
        kpis_rojos = len([k for k in kpis if k.estado == EstadoKPI.ROJO])
        
        # KPIs por tipo
        kpis_por_tipo = {}
        for tipo in TipoKPI:
            kpis_tipo = [k for k in kpis if k.tipo == tipo]
            kpis_por_tipo[tipo.value] = {
                'total': len(kpis_tipo),
                'promedio_cumplimiento': sum([k.porcentaje_cumplimiento() for k in kpis_tipo]) / len(kpis_tipo) if kpis_tipo else 0
            }
        
        return jsonify({
            'resumen': {
                'total_kpis': total_kpis,
                'kpis_verdes': kpis_verdes,
                'kpis_amarillos': kpis_amarillos,
                'kpis_rojos': kpis_rojos,
                'porcentaje_verde': (kpis_verdes / total_kpis * 100) if total_kpis > 0 else 0
            },
            'kpis_por_tipo': kpis_por_tipo,
            'kpis': [kpi.to_dict() for kpi in kpis]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

