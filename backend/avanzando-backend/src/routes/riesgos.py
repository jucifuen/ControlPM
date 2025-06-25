from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.riesgo import Riesgo, TipoRiesgo, NivelProbabilidad, NivelImpacto, EstadoRiesgo
from src.models.project import Proyecto
from datetime import datetime

riesgos_bp = Blueprint('riesgos', __name__)

@riesgos_bp.route('/api/riesgos', methods=['GET'])
def get_riesgos():
    try:
        proyecto_id = request.args.get('proyecto_id')
        
        query = Riesgo.query.filter_by(activo=True)
        if proyecto_id:
            query = query.filter_by(proyecto_id=proyecto_id)
        
        riesgos = query.all()
        return jsonify([riesgo.to_dict() for riesgo in riesgos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@riesgos_bp.route('/api/riesgos', methods=['POST'])
def create_riesgo():
    try:
        data = request.get_json()
        
        # Validar que el proyecto existe
        proyecto = Proyecto.query.get(data['proyecto_id'])
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        # Generar código automático
        count = Riesgo.query.filter_by(proyecto_id=data['proyecto_id']).count()
        codigo = f"R-{data['proyecto_id']:03d}-{count + 1:03d}"
        
        riesgo = Riesgo(
            proyecto_id=data['proyecto_id'],
            codigo=codigo,
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            tipo=TipoRiesgo(data['tipo']),
            probabilidad=NivelProbabilidad(data['probabilidad']),
            impacto=NivelImpacto(data['impacto']),
            plan_mitigacion=data.get('plan_mitigacion', ''),
            plan_contingencia=data.get('plan_contingencia', ''),
            responsable_id=data.get('responsable_id'),
            costo_estimado=float(data.get('costo_estimado', 0))
        )
        
        db.session.add(riesgo)
        db.session.commit()
        
        return jsonify({
            'message': 'Riesgo creado exitosamente',
            'riesgo': riesgo.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@riesgos_bp.route('/api/riesgos/<int:riesgo_id>', methods=['GET'])
def get_riesgo(riesgo_id):
    try:
        riesgo = Riesgo.query.get_or_404(riesgo_id)
        return jsonify(riesgo.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@riesgos_bp.route('/api/riesgos/<int:riesgo_id>', methods=['PUT'])
def update_riesgo(riesgo_id):
    try:
        riesgo = Riesgo.query.get_or_404(riesgo_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            riesgo.nombre = data['nombre']
        if 'descripcion' in data:
            riesgo.descripcion = data['descripcion']
        if 'tipo' in data:
            riesgo.tipo = TipoRiesgo(data['tipo'])
        if 'probabilidad' in data:
            riesgo.probabilidad = NivelProbabilidad(data['probabilidad'])
        if 'impacto' in data:
            riesgo.impacto = NivelImpacto(data['impacto'])
        if 'estado' in data:
            riesgo.estado = EstadoRiesgo(data['estado'])
        if 'plan_mitigacion' in data:
            riesgo.plan_mitigacion = data['plan_mitigacion']
        if 'plan_contingencia' in data:
            riesgo.plan_contingencia = data['plan_contingencia']
        if 'responsable_id' in data:
            riesgo.responsable_id = data['responsable_id']
        if 'costo_estimado' in data:
            riesgo.costo_estimado = float(data['costo_estimado'])
        
        # Actualizar fechas según el estado
        if 'estado' in data:
            if data['estado'] == 'en_seguimiento' and not riesgo.fecha_revision:
                riesgo.fecha_revision = datetime.utcnow()
            elif data['estado'] in ['mitigado', 'cerrado'] and not riesgo.fecha_cierre:
                riesgo.fecha_cierre = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Riesgo actualizado exitosamente',
            'riesgo': riesgo.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@riesgos_bp.route('/api/riesgos/<int:riesgo_id>', methods=['DELETE'])
def delete_riesgo(riesgo_id):
    try:
        riesgo = Riesgo.query.get_or_404(riesgo_id)
        riesgo.activo = False
        
        db.session.commit()
        
        return jsonify({'message': 'Riesgo eliminado exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@riesgos_bp.route('/api/riesgos/matriz/<int:proyecto_id>', methods=['GET'])
def get_matriz_riesgos(proyecto_id):
    try:
        riesgos = Riesgo.query.filter_by(proyecto_id=proyecto_id, activo=True).all()
        
        # Crear matriz 5x5
        matriz = {}
        for prob in range(1, 6):
            matriz[prob] = {}
            for imp in range(1, 6):
                matriz[prob][imp] = []
        
        # Clasificar riesgos en la matriz
        for riesgo in riesgos:
            prob = riesgo.probabilidad.value
            imp = riesgo.impacto.value
            matriz[prob][imp].append(riesgo.to_dict())
        
        # Estadísticas
        total_riesgos = len(riesgos)
        riesgos_por_nivel = {}
        riesgos_por_estado = {}
        
        for riesgo in riesgos:
            nivel = riesgo.nivel_riesgo()
            estado = riesgo.estado.value
            
            riesgos_por_nivel[nivel] = riesgos_por_nivel.get(nivel, 0) + 1
            riesgos_por_estado[estado] = riesgos_por_estado.get(estado, 0) + 1
        
        return jsonify({
            'matriz': matriz,
            'estadisticas': {
                'total_riesgos': total_riesgos,
                'riesgos_por_nivel': riesgos_por_nivel,
                'riesgos_por_estado': riesgos_por_estado
            },
            'riesgos': [riesgo.to_dict() for riesgo in riesgos]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@riesgos_bp.route('/api/riesgos/dashboard/<int:proyecto_id>', methods=['GET'])
def get_riesgos_dashboard(proyecto_id):
    try:
        riesgos = Riesgo.query.filter_by(proyecto_id=proyecto_id, activo=True).all()
        
        # Riesgos críticos (exposición >= 20)
        riesgos_criticos = [r for r in riesgos if r.calcular_exposicion() >= 20]
        
        # Riesgos por tipo
        riesgos_por_tipo = {}
        for tipo in TipoRiesgo:
            count = len([r for r in riesgos if r.tipo == tipo])
            riesgos_por_tipo[tipo.value] = count
        
        # Costo total estimado de riesgos
        costo_total = sum([r.costo_estimado for r in riesgos])
        
        return jsonify({
            'resumen': {
                'total_riesgos': len(riesgos),
                'riesgos_criticos': len(riesgos_criticos),
                'costo_total_estimado': costo_total
            },
            'riesgos_por_tipo': riesgos_por_tipo,
            'riesgos_criticos': [r.to_dict() for r in riesgos_criticos[:5]]  # Top 5
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

