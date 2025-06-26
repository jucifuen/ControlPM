from datetime import datetime
from src.models.user import db
import enum

class TipoGasto(enum.Enum):
    PERSONAL = 'personal'
    MATERIAL = 'material'
    SERVICIO = 'servicio'
    TRANSPORTE = 'transporte'
    OTRO = 'otro'

class EstadoLiquidacion(enum.Enum):
    BORRADOR = 'borrador'
    ENVIADA = 'enviada'
    APROBADA = 'aprobada'
    PAGADA = 'pagada'
    RECHAZADA = 'rechazada'

class Liquidacion(db.Model):
    __tablename__ = 'liquidaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    periodo_inicio = db.Column(db.Date, nullable=False)
    periodo_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum(EstadoLiquidacion), default=EstadoLiquidacion.BORRADOR)
    total_gastos = db.Column(db.Decimal(10, 2), default=0)
    total_horas = db.Column(db.Decimal(8, 2), default=0)
    observaciones = db.Column(db.Text)
    creado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    aprobado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_aprobacion = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    proyecto = db.relationship('Proyecto', backref='liquidaciones')
    creador = db.relationship('User', foreign_keys=[creado_por], backref='liquidaciones_creadas')
    aprobador = db.relationship('User', foreign_keys=[aprobado_por], backref='liquidaciones_aprobadas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'periodo_inicio': self.periodo_inicio.isoformat() if self.periodo_inicio else None,
            'periodo_fin': self.periodo_fin.isoformat() if self.periodo_fin else None,
            'estado': self.estado.value,
            'total_gastos': float(self.total_gastos) if self.total_gastos else 0,
            'total_horas': float(self.total_horas) if self.total_horas else 0,
            'observaciones': self.observaciones,
            'creado_por': self.creado_por,
            'aprobado_por': self.aprobado_por,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_aprobacion': self.fecha_aprobacion.isoformat() if self.fecha_aprobacion else None
        }

class DetalleGasto(db.Model):
    __tablename__ = 'detalle_gastos'
    
    id = db.Column(db.Integer, primary_key=True)
    liquidacion_id = db.Column(db.Integer, db.ForeignKey('liquidaciones.id'), nullable=False)
    tipo_gasto = db.Column(db.Enum(TipoGasto), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    cantidad = db.Column(db.Decimal(8, 2), nullable=False)
    precio_unitario = db.Column(db.Decimal(10, 2), nullable=False)
    total = db.Column(db.Decimal(10, 2), nullable=False)
    fecha_gasto = db.Column(db.Date, nullable=False)
    comprobante_url = db.Column(db.String(500))
    
    # Relaciones
    liquidacion = db.relationship('Liquidacion', backref='detalles_gastos')
    
    def to_dict(self):
        return {
            'id': self.id,
            'liquidacion_id': self.liquidacion_id,
            'tipo_gasto': self.tipo_gasto.value,
            'descripcion': self.descripcion,
            'cantidad': float(self.cantidad),
            'precio_unitario': float(self.precio_unitario),
            'total': float(self.total),
            'fecha_gasto': self.fecha_gasto.isoformat() if self.fecha_gasto else None,
            'comprobante_url': self.comprobante_url
        }

class RegistroHoras(db.Model):
    __tablename__ = 'registro_horas'
    
    id = db.Column(db.Integer, primary_key=True)
    liquidacion_id = db.Column(db.Integer, db.ForeignKey('liquidaciones.id'), nullable=False)
    recurso_id = db.Column(db.Integer, db.ForeignKey('recursos.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    horas_trabajadas = db.Column(db.Decimal(4, 2), nullable=False)
    tarifa_hora = db.Column(db.Decimal(8, 2), nullable=False)
    total = db.Column(db.Decimal(10, 2), nullable=False)
    descripcion_actividad = db.Column(db.Text)
    
    # Relaciones
    liquidacion = db.relationship('Liquidacion', backref='registro_horas')
    recurso = db.relationship('Recurso', backref='horas_registradas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'liquidacion_id': self.liquidacion_id,
            'recurso_id': self.recurso_id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'horas_trabajadas': float(self.horas_trabajadas),
            'tarifa_hora': float(self.tarifa_hora),
            'total': float(self.total),
            'descripcion_actividad': self.descripcion_actividad
        }

