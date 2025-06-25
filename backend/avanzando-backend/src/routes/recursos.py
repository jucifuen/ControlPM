from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.recurso import Recurso, TipoRecurso, EstadoRecurso
from src.models.project import Proyecto
from datetime import datetime

recursos_bp = Blueprint('recursos', __name__)

@recursos_bp.route('/api/recursos', methods=['GET'])
def get_recursos():
    try:
        proyecto_id = request.args.get('proyecto_id')
        tipo = request.args.get('tipo')
        
        query = Recurso.query.filter_by(activo=True)
        if proyecto_id:
            query = query.filter_by(proyecto_id=proyecto_id)
        if tipo:
            query = query.filter_by(tipo=TipoRecurso(tipo))
        
        recursos = query.all()
        return jsonify([recurso.to_dict() for recurso in recursos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recursos_bp.route('/api/recursos', methods=['POST'])
def create_recurso():
    try:
        data = request.get_json()
        
        # Validar que el proyecto existe
        proyecto = Proyecto.query.get(data['proyecto_id'])
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        recurso = Recurso(
            proyecto_id=data['proyecto_id'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            tipo=TipoRecurso(data['tipo']),
            cantidad_requerida=float(data['cantidad_requerida']),
            cantidad_asignada=float(data.get('cantidad_asignada', 0)),
            unidad_medida=data['unidad_medida'],
            costo_unitario=float(data.get('costo_unitario', 0)),
            fecha_inicio=datetime.fromisoformat(data['fecha_inicio']) if data.get('fecha_inicio') else None,
            fecha_fin=datetime.fromisoformat(data['fecha_fin']) if data.get('fecha_fin') else None,
            usuario_asignado_id=data.get('usuario_asignado_id'),
            observaciones=data.get('observaciones', '')
        )
        
        recurso.calcular_costo_total()
        recurso.actualizar_estado()
        
        db.session.add(recurso)
        db.session.commit()
        
        return jsonify({
            'message': 'Recurso creado exitosamente',
            'recurso': recurso.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recursos_bp.route('/api/recursos/<int:recurso_id>', methods=['GET'])
def get_recurso(recurso_id):
    try:
        recurso = Recurso.query.get_or_404(recurso_id)
        return jsonify(recurso.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recursos_bp.route('/api/recursos/<int:recurso_id>', methods=['PUT'])
def update_recurso(recurso_id):
    try:
        recurso = Recurso.query.get_or_404(recurso_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            recurso.nombre = data['nombre']
        if 'descripcion' in data:
            recurso.descripcion = data['descripcion']
        if 'tipo' in data:
            recurso.tipo = TipoRecurso(data['tipo'])
        if 'cantidad_requerida' in data:
            recurso.cantidad_requerida = float(data['cantidad_requerida'])
        if 'cantidad_asignada' in data:
            recurso.cantidad_asignada = float(data['cantidad_asignada'])
        if 'unidad_medida' in data:
            recurso.unidad_medida = data['unidad_medida']
        if 'costo_unitario' in data:
            recurso.costo_unitario = float(data['costo_unitario'])
        if 'fecha_inicio' in data:
            recurso.fecha_inicio = datetime.fromisoformat(data['fecha_inicio']) if data['fecha_inicio'] else None
        if 'fecha_fin' in data:
            recurso.fecha_fin = datetime.fromisoformat(data['fecha_fin']) if data['fecha_fin'] else None
        if 'usuario_asignado_id' in data:
            recurso.usuario_asignado_id = data['usuario_asignado_id']
        if 'observaciones' in data:
            recurso.observaciones = data['observaciones']
        if 'estado' in data:
            recurso.estado = EstadoRecurso(data['estado'])
        
        recurso.calcular_costo_total()
        recurso.actualizar_estado()
        recurso.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Recurso actualizado exitosamente',
            'recurso': recurso.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recursos_bp.route('/api/recursos/<int:recurso_id>', methods=['DELETE'])
def delete_recurso(recurso_id):
    try:
        recurso = Recurso.query.get_or_404(recurso_id)
        recurso.activo = False
        recurso.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Recurso eliminado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recursos_bp.route('/api/recursos/dashboard/<int:proyecto_id>', methods=['GET'])
def get_recursos_dashboard(proyecto_id):
    try:
        recursos = Recurso.query.filter_by(proyecto_id=proyecto_id, activo=True).all()
        
        # Estadísticas generales
        total_recursos = len(recursos)
        costo_total = sum([r.costo_total for r in recursos])
        
        # Recursos por tipo
        recursos_por_tipo = {}
        costo_por_tipo = {}
        for tipo in TipoRecurso:
            recursos_tipo = [r for r in recursos if r.tipo == tipo]
            recursos_por_tipo[tipo.value] = len(recursos_tipo)
            costo_por_tipo[tipo.value] = sum([r.costo_total for r in recursos_tipo])
        
        # Recursos por estado
        recursos_por_estado = {}
        for estado in EstadoRecurso:
            count = len([r for r in recursos if r.estado == estado])
            recursos_por_estado[estado.value] = count
        
        # Utilización promedio
        utilizacion_promedio = sum([r.porcentaje_asignacion() for r in recursos]) / len(recursos) if recursos else 0
        
        # Recursos críticos (baja asignación)
        recursos_criticos = [r for r in recursos if r.porcentaje_asignacion() < 50]
        
        return jsonify({
            'resumen': {
                'total_recursos': total_recursos,
                'costo_total': costo_total,
                'utilizacion_promedio': utilizacion_promedio,
                'recursos_criticos': len(recursos_criticos)
            },
            'recursos_por_tipo': recursos_por_tipo,
            'costo_por_tipo': costo_por_tipo,
            'recursos_por_estado': recursos_por_estado,
            'recursos_criticos': [r.to_dict() for r in recursos_criticos[:5]]  # Top 5
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recursos_bp.route('/api/recursos/asignacion/<int:proyecto_id>', methods=['GET'])
def get_asignacion_recursos(proyecto_id):
    try:
        recursos = Recurso.query.filter_by(proyecto_id=proyecto_id, activo=True).all()
        
        # Datos para gráfico de asignación
        datos_asignacion = []
        for recurso in recursos:
            datos_asignacion.append({
                'nombre': recurso.nombre,
                'tipo': recurso.tipo.value,
                'requerido': recurso.cantidad_requerida,
                'asignado': recurso.cantidad_asignada,
                'porcentaje': recurso.porcentaje_asignacion(),
                'estado': recurso.estado.value
            })
        
        return jsonify({
            'datos_asignacion': datos_asignacion
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

