from functools import wraps
from flask import request, jsonify, current_app
import jwt
from src.models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener token del header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token de acceso requerido'}), 401
        
        try:
            # Decodificar token
            SECRET_KEY = current_app.config.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user or not current_user.activo:
                return jsonify({'error': 'Token inválido'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'error': 'Error de autenticación'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def get_current_user():
    """Helper para obtener el usuario actual desde el token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    
    try:
        from flask import current_app
        SECRET_KEY = current_app.config.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return User.query.get(data['user_id'])
    except:
        return None

