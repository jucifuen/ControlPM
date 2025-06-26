import pytest
from datetime import datetime, date
from src.models.user import User, UserRole, db
from src.models.project import Proyecto, EstadoProyecto, Fase, TipoFase

class TestProjectModel:
    """Pruebas unitarias para el modelo Proyecto"""
    
    def test_create_project(self, client):
        """Prueba la creación de un proyecto"""
        with client.application.app_context():
            # Crear usuario PM
            pm = User(
                nombre='Project Manager',
                email='pm@example.com',
                rol=UserRole.PM
            )
            pm.set_password('testpass')
            db.session.add(pm)
            db.session.commit()
            
            # Crear cliente
            cliente = User(
                nombre='Cliente Test',
                email='cliente@example.com',
                rol=UserRole.CLIENTE
            )
            cliente.set_password('testpass')
            db.session.add(cliente)
            db.session.commit()
            
            # Crear proyecto
            proyecto = Proyecto(
                nombre='Proyecto Test',
                descripcion='Descripción del proyecto',
                cliente_id=cliente.id,
                presupuesto_estimado=100000,
                fecha_inicio=date(2024, 1, 1),
                fecha_fin=date(2024, 12, 31)
            )
            
            db.session.add(proyecto)
            db.session.commit()
            
            assert proyecto.id is not None
            assert proyecto.nombre == 'Proyecto Test'
            assert proyecto.estado == EstadoProyecto.ACTIVO
            assert proyecto.cliente_id == cliente.id
            assert proyecto.presupuesto_estimado == 100000
    
    def test_project_states(self, client):
        """Prueba los estados del proyecto"""
        with client.application.app_context():
            # Crear usuario PM
            pm = User(
                nombre='PM',
                email='pm@example.com',
                rol=UserRole.PM
            )
            pm.set_password('testpass')
            db.session.add(pm)
            db.session.commit()
            
            estados = [
                EstadoProyecto.ACTIVO,
                EstadoProyecto.PAUSADO,
                EstadoProyecto.COMPLETADO,
                EstadoProyecto.CANCELADO
            ]
            
            for estado in estados:
                proyecto = Proyecto(
                    nombre=f'Proyecto {estado.value}',
                    descripcion='Test',
                    cliente_id=pm.id,
                    estado=estado,
                    fecha_inicio=date(2024, 1, 1)
                )
                
                db.session.add(proyecto)
                db.session.commit()
                
                assert proyecto.estado == estado
                assert proyecto.to_dict()['estado'] == estado.value
    
    def test_project_to_dict(self, client):
        """Prueba la serialización del proyecto"""
        with client.application.app_context():
            # Crear usuario PM
            pm = User(
                nombre='PM',
                email='pm2@example.com',
                rol=UserRole.PM
            )
            pm.set_password('testpass')
            db.session.add(pm)
            db.session.commit()
            
            proyecto = Proyecto(
                nombre='Proyecto Test',
                descripcion='Descripción test',
                cliente_id=pm.id,
                presupuesto_estimado=50000,
                presupuesto_real=25000,
                fecha_inicio=date(2024, 1, 1)
            )
            
            db.session.add(proyecto)
            db.session.commit()
            
            project_dict = proyecto.to_dict()
            
            assert project_dict['nombre'] == 'Proyecto Test'
            assert project_dict['descripcion'] == 'Descripción test'
            assert project_dict['estado'] == 'activo'
            assert project_dict['presupuesto_estimado'] == 50000
            assert project_dict['presupuesto_real'] == 25000
            assert 'id' in project_dict
    
    def test_project_phases(self, client):
        """Prueba la relación con fases"""
        with client.application.app_context():
            # Crear usuario PM
            pm = User(
                nombre='PM',
                email='pm3@example.com',
                rol=UserRole.PM
            )
            pm.set_password('testpass')
            db.session.add(pm)
            db.session.commit()
            
            # Crear proyecto
            proyecto = Proyecto(
                nombre='Proyecto con Fases',
                descripcion='Test',
                cliente_id=pm.id,
                fecha_inicio=date(2024, 1, 1)
            )
            db.session.add(proyecto)
            db.session.commit()
            
            # Crear fases
            fase1 = Fase(
                nombre='Fase 1',
                descripcion='Primera fase',
                proyecto_id=proyecto.id,
                tipo=TipoFase.INICIO,
                fecha_inicio=date(2024, 1, 1),
                fecha_fin=date(2024, 3, 31)
            )
            
            fase2 = Fase(
                nombre='Fase 2',
                descripcion='Segunda fase',
                proyecto_id=proyecto.id,
                tipo=TipoFase.PLANEACION,
                fecha_inicio=date(2024, 4, 1),
                fecha_fin=date(2024, 6, 30)
            )
            
            db.session.add_all([fase1, fase2])
            db.session.commit()
            
            # Verificar relación
            assert len(proyecto.fases) == 2
            assert fase1 in proyecto.fases
            assert fase2 in proyecto.fases
            assert fase1.proyecto == proyecto
            assert fase2.proyecto == proyecto
