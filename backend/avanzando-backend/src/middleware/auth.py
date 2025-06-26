from functools import wraps
from flask import request, jsonify, current_app
import jwt
from src.models.user import User

def token_required(f):
    """Decorador para requerir autenticación JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener token del header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token malformado'}), 401
        
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        try:
            # Decodificar token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
            
            if not current_user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.rol.value != 'administrador':
            return jsonify({'error': 'Acceso denegado. Se requiere rol de administrador'}), 403
        return f(current_user, *args, **kwargs)
    
    return decorated

def pm_required(f):
    """Decorador para requerir rol de PM o superior"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        allowed_roles = ['administrador', 'pm']
        if current_user.rol.value not in allowed_roles:
            return jsonify({'error': 'Acceso denegado. Se requiere rol de PM o superior'}), 403
        return f(current_user, *args, **kwargs)
    
    return decorated

