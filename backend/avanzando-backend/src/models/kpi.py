from src.models.user import db
from datetime import datetime
import enum

class TipoKPI(enum.Enum):
    TIEMPO = "tiempo"
    ALCANCE = "alcance"
    COSTO = "costo"
    CALIDAD = "calidad"
    RECURSOS = "recursos"

class EstadoKPI(enum.Enum):
    VERDE = "verde"
    AMARILLO = "amarillo"
    ROJO = "rojo"

class KPI(db.Model):
    __tablename__ = 'kpis'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.Enum(TipoKPI), nullable=False)
    valor_objetivo = db.Column(db.Float, nullable=False)
    valor_actual = db.Column(db.Float, default=0)
    unidad_medida = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Enum(EstadoKPI), default=EstadoKPI.VERDE)
    umbral_amarillo = db.Column(db.Float, nullable=False)
    umbral_rojo = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    proyecto = db.relationship('Proyecto', backref='kpis')
    
    def calcular_estado(self):
        """Calcula el estado del KPI basado en los umbrales"""
        if self.valor_actual >= self.umbral_rojo:
            self.estado = EstadoKPI.ROJO
        elif self.valor_actual >= self.umbral_amarillo:
            self.estado = EstadoKPI.AMARILLO
        else:
            self.estado = EstadoKPI.VERDE
        
        self.fecha_actualizacion = datetime.utcnow()
    
    def porcentaje_cumplimiento(self):
        """Calcula el porcentaje de cumplimiento del KPI"""
        if self.valor_objetivo == 0:
            return 0
        return min(100, (self.valor_actual / self.valor_objetivo) * 100)
    
    def to_dict(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo.value,
            'valor_objetivo': self.valor_objetivo,
            'valor_actual': self.valor_actual,
            'unidad_medida': self.unidad_medida,
            'estado': self.estado.value,
            'umbral_amarillo': self.umbral_amarillo,
            'umbral_rojo': self.umbral_rojo,
            'porcentaje_cumplimiento': self.porcentaje_cumplimiento(),
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat(),
            'activo': self.activo
        }

