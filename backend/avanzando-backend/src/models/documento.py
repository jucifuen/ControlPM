from datetime import datetime
from src.models.user import db
import enum

class TipoDocumento(enum.Enum):
    CONTRATO = 'contrato'
    PROPUESTA = 'propuesta'
    INFORME = 'informe'
    ACTA = 'acta'
    FACTURA = 'factura'
    OTRO = 'otro'

class EstadoDocumento(enum.Enum):
    BORRADOR = 'borrador'
    REVISION = 'revision'
    APROBADO = 'aprobado'
    FIRMADO = 'firmado'

class Documento(db.Model):
    __tablename__ = 'documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum(TipoDocumento), nullable=False)
    estado = db.Column(db.Enum(EstadoDocumento), default=EstadoDocumento.BORRADOR)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    plantilla_id = db.Column(db.Integer, db.ForeignKey('plantillas_documento.id'), nullable=True)
    contenido = db.Column(db.Text)
    archivo_url = db.Column(db.String(500))
    version = db.Column(db.Integer, default=1)
    creado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    proyecto = db.relationship('Proyecto', backref='documentos')
    plantilla = db.relationship('PlantillaDocumento', backref='documentos')
    creador = db.relationship('User', backref='documentos_creados')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo.value,
            'estado': self.estado.value,
            'proyecto_id': self.proyecto_id,
            'plantilla_id': self.plantilla_id,
            'contenido': self.contenido,
            'archivo_url': self.archivo_url,
            'version': self.version,
            'creado_por': self.creado_por,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

class PlantillaDocumento(db.Model):
    __tablename__ = 'plantillas_documento'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum(TipoDocumento), nullable=False)
    contenido_plantilla = db.Column(db.Text, nullable=False)
    variables = db.Column(db.JSON)  # Variables disponibles en la plantilla
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo.value,
            'contenido_plantilla': self.contenido_plantilla,
            'variables': self.variables,
            'activa': self.activa,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

