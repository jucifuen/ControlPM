from flask import Blueprint, request, jsonify, send_file
from src.middleware.auth import token_required
from src.models.documento import Documento, PlantillaDocumento, TipoDocumento, EstadoDocumento, db
from src.models.project import Proyecto
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

documentos_bp = Blueprint('documentos', __name__)

@documentos_bp.route('/documentos', methods=['GET'])
@token_required
def get_documentos(current_user):
    """Obtiene documentos con filtros"""
    try:
        proyecto_id = request.args.get('proyecto_id')
        tipo = request.args.get('tipo')
        
        query = Documento.query
        if proyecto_id:
            query = query.filter_by(proyecto_id=proyecto_id)
        if tipo:
            query = query.filter_by(tipo=TipoDocumento(tipo))
            
        documentos = query.all()
        return jsonify({'documentos': [d.to_dict() for d in documentos]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documentos_bp.route('/documentos', methods=['POST'])
@token_required
def crear_documento(current_user):
    """Crea un nuevo documento"""
    try:
        data = request.get_json()
        
        documento = Documento(
            nombre=data['nombre'],
            tipo=TipoDocumento(data['tipo']),
            proyecto_id=data['proyecto_id'],
            plantilla_id=data.get('plantilla_id'),
            contenido=data.get('contenido', ''),
            creado_por=current_user.id
        )
        
        db.session.add(documento)
        db.session.commit()
        
        return jsonify({
            'message': 'Documento creado exitosamente',
            'documento': documento.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documentos_bp.route('/documentos/upload', methods=['POST'])
@token_required
def upload_documento(current_user):
    """Sube archivo de documento"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró archivo'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
            
        # Crear directorio si no existe
        upload_dir = 'uploads/documentos'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generar nombre único
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        file.save(file_path)
        
        return jsonify({
            'message': 'Archivo subido exitosamente',
            'archivo_url': file_path
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documentos_bp.route('/plantillas', methods=['GET'])
@token_required
def get_plantillas(current_user):
    """Obtiene plantillas de documentos"""
    try:
        tipo = request.args.get('tipo')
        query = PlantillaDocumento.query.filter_by(activa=True)
        
        if tipo:
            query = query.filter_by(tipo=TipoDocumento(tipo))
            
        plantillas = query.all()
        return jsonify({'plantillas': [p.to_dict() for p in plantillas]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documentos_bp.route('/documentos/<int:doc_id>/generar', methods=['POST'])
@token_required
def generar_documento(current_user, doc_id):
    """Genera documento desde plantilla"""
    try:
        documento = Documento.query.get_or_404(doc_id)
        data = request.get_json()
        variables = data.get('variables', {})
        
        if documento.plantilla:
            # Reemplazar variables en la plantilla
            contenido = documento.plantilla.contenido_plantilla
            for var, valor in variables.items():
                contenido = contenido.replace(f"{{{{{var}}}}}", str(valor))
            
            documento.contenido = contenido
            documento.fecha_actualizacion = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': 'Documento generado exitosamente',
                'documento': documento.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Documento no tiene plantilla asociada'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

