from src.models.user import db
from datetime import datetime
from decimal import Decimal
import enum

class EstadoProyecto(enum.Enum):
    ACTIVO = "activo"
    PAUSADO = "pausado"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"

class TipoFase(enum.Enum):
    INICIO = "inicio"
    PLANEACION = "planeacion"
    EJECUCION = "ejecucion"
    SEGUIMIENTO_CONTROL = "seguimiento_control"
    CIERRE = "cierre"

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    estado = db.Column(db.Enum(EstadoProyecto), nullable=False, default=EstadoProyecto.ACTIVO)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    presupuesto_estimado = db.Column(db.Float, nullable=True)
    presupuesto_real = db.Column(db.Float, nullable=True, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cliente = db.relationship('Cliente', backref='proyectos', lazy=True)
    fases = db.relationship('Fase', backref='proyecto', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre if self.cliente else None,
            'estado': self.estado.value,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'presupuesto_estimado': self.presupuesto_estimado,
            'presupuesto_real': self.presupuesto_real or 0,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }

class Fase(db.Model):
    __tablename__ = 'fases'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    tipo = db.Column(db.Enum(TipoFase), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    avance = db.Column(db.Integer, default=0)  # Porcentaje de avance (0-100)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    completada = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'tipo': self.tipo.value,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'avance': self.avance,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'completada': self.completada,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }

