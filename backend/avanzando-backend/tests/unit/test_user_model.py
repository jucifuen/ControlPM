import pytest
from src.models.user import User, UserRole
from src.models.user import db

class TestUserModel:
    """Pruebas unitarias para el modelo User"""
    
    def test_create_user(self, client):
        """Prueba la creación de un usuario"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test@example.com',
                rol=UserRole.ADMINISTRADOR
            )
            user.set_password('testpass123')
            
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.nombre == 'Test User'
            assert user.email == 'test@example.com'
            assert user.rol == UserRole.ADMINISTRADOR
            assert user.check_password('testpass123')
            assert not user.check_password('wrongpass')
    
    def test_user_password_hashing(self, client):
        """Prueba el hash de contraseñas"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test@example.com',
                rol=UserRole.PM
            )
            user.set_password('mypassword')
            
            # La contraseña no debe almacenarse en texto plano
            assert user.password_hash != 'mypassword'
            assert user.check_password('mypassword')
            assert not user.check_password('wrongpassword')
    
    def test_user_to_dict(self, client):
        """Prueba la serialización del usuario"""
        with client.application.app_context():
            user = User(
                nombre='Test User',
                email='test@example.com',
                rol=UserRole.CLIENTE
            )
            user.set_password('testpass')
            
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            assert user_dict['nombre'] == 'Test User'
            assert user_dict['email'] == 'test@example.com'
            assert user_dict['rol'] == 'cliente'
            assert 'password_hash' not in user_dict
            assert 'id' in user_dict
    
    def test_user_roles(self, client):
        """Prueba los diferentes roles de usuario"""
        with client.application.app_context():
            roles = [
                UserRole.ADMINISTRADOR,
                UserRole.PM,
                UserRole.CLIENTE,
                UserRole.RECURSO
            ]
            
            for rol in roles:
                user = User(
                    nombre=f'User {rol.value}',
                    email=f'{rol.value}@example.com',
                    rol=rol
                )
                user.set_password('testpass')
                
                db.session.add(user)
                db.session.commit()
                
                assert user.rol == rol
                assert user.to_dict()['rol'] == rol.value
    
    def test_user_unique_email(self, client):
        """Prueba que el email sea único"""
        with client.application.app_context():
            user1 = User(
                nombre='User 1',
                email='same@example.com',
                rol=UserRole.PM
            )
            user1.set_password('pass1')
            
            user2 = User(
                nombre='User 2',
                email='same@example.com',
                rol=UserRole.CLIENTE
            )
            user2.set_password('pass2')
            
            db.session.add(user1)
            db.session.commit()
            
            db.session.add(user2)
            
            # Debe fallar por email duplicado
            with pytest.raises(Exception):
                db.session.commit()

