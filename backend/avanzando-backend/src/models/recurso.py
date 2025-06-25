from src.models.user import db
from datetime import datetime
import enum

class TipoRecurso(enum.Enum):
    HUMANO = "humano"
    MATERIAL = "material"
    TECNOLOGICO = "tecnologico"
    FINANCIERO = "financiero"

class EstadoRecurso(enum.Enum):
    DISPONIBLE = "disponible"
    ASIGNADO = "asignado"
    OCUPADO = "ocupado"
    NO_DISPONIBLE = "no_disponible"

class Recurso(db.Model):
    __tablename__ = 'recursos'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.Enum(TipoRecurso), nullable=False)
    estado = db.Column(db.Enum(EstadoRecurso), default=EstadoRecurso.DISPONIBLE)
    cantidad_requerida = db.Column(db.Float, nullable=False)
    cantidad_asignada = db.Column(db.Float, default=0)
    unidad_medida = db.Column(db.String(50), nullable=False)
    costo_unitario = db.Column(db.Float, default=0)
    costo_total = db.Column(db.Float, default=0)
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    usuario_asignado_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    proyecto = db.relationship('Proyecto', backref='recursos')
    usuario_asignado = db.relationship('User', foreign_keys=[usuario_asignado_id])
    
    def calcular_costo_total(self):
        """Calcula el costo total del recurso"""
        self.costo_total = self.cantidad_asignada * self.costo_unitario
        return self.costo_total
    
    def porcentaje_asignacion(self):
        """Calcula el porcentaje de asignación del recurso"""
        if self.cantidad_requerida == 0:
            return 0
        return min(100, (self.cantidad_asignada / self.cantidad_requerida) * 100)
    
    def dias_utilizacion(self):
        """Calcula los días de utilización del recurso"""
        if not self.fecha_inicio or not self.fecha_fin:
            return 0
        return (self.fecha_fin - self.fecha_inicio).days + 1
    
    def actualizar_estado(self):
        """Actualiza el estado del recurso basado en la asignación"""
        porcentaje = self.porcentaje_asignacion()
        
        if porcentaje == 0:
            self.estado = EstadoRecurso.DISPONIBLE
        elif porcentaje < 100:
            self.estado = EstadoRecurso.ASIGNADO
        else:
            self.estado = EstadoRecurso.OCUPADO
        
        self.fecha_actualizacion = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo.value,
            'estado': self.estado.value,
            'cantidad_requerida': self.cantidad_requerida,
            'cantidad_asignada': self.cantidad_asignada,
            'unidad_medida': self.unidad_medida,
            'costo_unitario': self.costo_unitario,
            'costo_total': self.costo_total,
            'porcentaje_asignacion': self.porcentaje_asignacion(),
            'dias_utilizacion': self.dias_utilizacion(),
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'usuario_asignado_id': self.usuario_asignado_id,
            'usuario_asignado_nombre': self.usuario_asignado.nombre if self.usuario_asignado else None,
            'observaciones': self.observaciones,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat(),
            'activo': self.activo
        }

