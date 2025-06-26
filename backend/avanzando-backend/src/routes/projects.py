from flask import Blueprint, request, jsonify
from src.models.user import db, User, UserRole
from src.models.project import Proyecto, Fase, TipoFase, EstadoProyecto
from src.middleware.auth import token_required, pm_required
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

def create_default_phases(proyecto_id):
    """Crear las fases por defecto para un proyecto"""
    fases_default = [
        {'tipo': TipoFase.INICIO, 'nombre': 'Inicio'},
        {'tipo': TipoFase.PLANEACION, 'nombre': 'Planeación'},
        {'tipo': TipoFase.EJECUCION, 'nombre': 'Ejecución'},
        {'tipo': TipoFase.SEGUIMIENTO_CONTROL, 'nombre': 'Seguimiento y Control'},
        {'tipo': TipoFase.CIERRE, 'nombre': 'Cierre'}
    ]
    
    for fase_data in fases_default:
        fase = Fase(
            proyecto_id=proyecto_id,
            tipo=fase_data['tipo'],
            nombre=fase_data['nombre']
        )
        db.session.add(fase)

@projects_bp.route('/projects', methods=['GET'])
@token_required
def get_projects(current_user):
    try:
        # Filtrar proyectos según el rol del usuario
        if current_user.rol == UserRole.ADMINISTRADOR or current_user.rol == UserRole.PM:
            proyectos = Proyecto.query.all()
        elif current_user.rol == UserRole.CLIENTE:
            proyectos = Proyecto.query.filter_by(cliente_id=current_user.cliente_id).all()
        else:
            # Para recursos, mostrar proyectos donde están asignados (implementar lógica más adelante)
            proyectos = []
        
        return jsonify({
            'projects': [proyecto.to_dict() for proyecto in proyectos]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects', methods=['POST'])
@token_required
@pm_required
def create_project(current_user):
    try:
        data = request.get_json()
        
        if not data or not data.get('nombre') or not data.get('cliente_id'):
            return jsonify({'error': 'Nombre y cliente_id son requeridos'}), 400
        
        # Crear nuevo proyecto
        nuevo_proyecto = Proyecto(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            cliente_id=data['cliente_id'],
            fecha_inicio=datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date() if data.get('fecha_inicio') else datetime.utcnow().date(),
            fecha_fin=datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data.get('fecha_fin') else None,
            presupuesto_estimado=data.get('presupuesto_estimado')
        )
        
        db.session.add(nuevo_proyecto)
        db.session.flush()  # Para obtener el ID del proyecto
        
        # Crear fases por defecto
        create_default_phases(nuevo_proyecto.id)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Proyecto creado exitosamente',
            'project': nuevo_proyecto.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
@token_required
def get_project(current_user, project_id):
    try:
        proyecto = Proyecto.query.get(project_id)
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        # Verificar permisos
        if current_user.rol == UserRole.CLIENTE and proyecto.cliente_id != current_user.cliente_id:
            return jsonify({'error': 'No tiene permisos para ver este proyecto'}), 403
        
        # Incluir fases del proyecto
        proyecto_dict = proyecto.to_dict()
        proyecto_dict['fases'] = [fase.to_dict() for fase in proyecto.fases]
        
        return jsonify({'project': proyecto_dict}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
@token_required
@pm_required
def update_project(current_user, project_id):
    try:
        proyecto = Proyecto.query.get(project_id)
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            proyecto.nombre = data['nombre']
        if 'descripcion' in data:
            proyecto.descripcion = data['descripcion']
        if 'estado' in data:
            proyecto.estado = EstadoProyecto(data['estado'])
        if 'fecha_fin' in data:
            proyecto.fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data['fecha_fin'] else None
        if 'presupuesto_estimado' in data:
            proyecto.presupuesto_estimado = data['presupuesto_estimado']
        
        proyecto.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Proyecto actualizado exitosamente',
            'project': proyecto.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<int:project_id>/phases/<int:phase_id>/advance', methods=['POST'])
@token_required
@pm_required
def advance_phase(current_user, project_id, phase_id):
    try:
        fase = Fase.query.filter_by(id=phase_id, proyecto_id=project_id).first()
        if not fase:
            return jsonify({'error': 'Fase no encontrada'}), 404
        
        data = request.get_json()
        avance = data.get('avance', 0)
        
        if avance < 0 or avance > 100:
            return jsonify({'error': 'El avance debe estar entre 0 y 100'}), 400
        
        fase.avance = avance
        if avance == 100:
            fase.completada = True
            fase.fecha_fin = datetime.utcnow().date()
        
        fase.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Fase actualizada exitosamente',
            'fase': fase.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Agregar ruta DELETE para proyectos
@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@token_required
@pm_required
def delete_project(current_user, project_id):
    try:
        proyecto = Proyecto.query.get(project_id)
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        db.session.delete(proyecto)
        db.session.commit()
        
        return jsonify({'message': 'Proyecto eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

