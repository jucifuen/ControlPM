from flask import Blueprint, request, jsonify
from src.models.user import db, User, UserRole
import jwt
from datetime import datetime, timedelta
import os

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data:
            return jsonify({'error': 'Datos requeridos'}), 400
            
        if not data.get('nombre'):
            return jsonify({'error': 'Nombre es requerido'}), 400
            
        if not data.get('email'):
            return jsonify({'error': 'Email es requerido'}), 400
            
        if not data.get('password'):
            return jsonify({'error': 'Contraseña es requerida'}), 400
        
        # Validar rol
        rol_str = data.get('rol', 'recurso')
        try:
            rol = UserRole(rol_str)
        except ValueError:
            return jsonify({'error': 'Rol inválido'}), 400
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        # Crear nuevo usuario
        new_user = User(
            nombre=data['nombre'],
            email=data['email'],
            rol=rol,
            cliente_id=data.get('cliente_id')
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        # Buscar usuario
        user = User.query.filter_by(email=data['email'], activo=True).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Generar token JWT
        token_payload = {
            'user_id': user.id,
            'email': user.email,
            'rol': user.rol.value,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'message': 'Login exitoso',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    try:
        # Obtener token del header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        
        # Buscar usuario
        user = User.query.get(user_id)
        if not user or not user.activo:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token inválido'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

