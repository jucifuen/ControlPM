import pytest
from datetime import datetime, date
from src.models.user import User, UserRole, db
from src.models.project import Proyecto, EstadoProyecto, Fase, TipoFase

class TestPhaseModel:
    """Pruebas unitarias para el modelo Fase"""
    
    def test_create_phase(self, client):
        """Prueba la creación de una fase"""
        with client.application.app_context():
            # Crear usuario PM
            pm = User(
                nombre='PM',
                email='pm4@example.com',
                rol=UserRole.PM
            )
            pm.set_password('testpass')
            db.session.add(pm)
            db.session.commit()
            
            # Crear proyecto
            proyecto = Proyecto(
                nombre='Proyecto',
                descripcion='Test',
                cliente_id=pm.id,
                fecha_inicio=date(2024, 1, 1)
            )
            db.session.add(proyecto)
            db.session.commit()
            
            # Crear fase
            fase = Fase(
                nombre='Fase Test',
                descripcion='Descripción de la fase',
                proyecto_id=proyecto.id,
                tipo=TipoFase.INICIO,
                fecha_inicio=date(2024, 1, 1),
                fecha_fin=date(2024, 3, 31)
            )
            
            db.session.add(fase)
            db.session.commit()
            
            assert fase.id is not None
            assert fase.nombre == 'Fase Test'
            assert fase.completada == False
            assert fase.proyecto_id == proyecto.id
    
    def test_phase_states(self, client):
        """Prueba los estados de las fases"""
        with client.application.app_context():
            # Crear usuario PM
            pm = User(
                nombre='PM',
                email='pm5@example.com',
                rol=UserRole.PM
            )
            pm.set_password('testpass')
            db.session.add(pm)
            db.session.commit()
            
            # Crear proyecto
            proyecto = Proyecto(
                nombre='Proyecto',
                descripcion='Test',
                cliente_id=pm.id,
                fecha_inicio=date(2024, 1, 1)
            )
            db.session.add(proyecto)
            db.session.commit()
            
            tipos = [
                TipoFase.INICIO,
                TipoFase.PLANEACION,
                TipoFase.EJECUCION,
                TipoFase.SEGUIMIENTO_CONTROL,
                TipoFase.CIERRE
            ]
            
            for tipo in tipos:
                fase = Fase(
                    nombre=f'Fase {tipo.value}',
                    descripcion='Test',
                    proyecto_id=proyecto.id,
                    tipo=tipo
                )
                
                db.session.add(fase)
                db.session.commit()
                
                assert fase.tipo == tipo
                assert fase.to_dict()['tipo'] == tipo.value

