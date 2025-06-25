from src.models.user import db
from datetime import datetime
import enum

class TipoRiesgo(enum.Enum):
    TECNICO = "tecnico"
    OPERACIONAL = "operacional"
    FINANCIERO = "financiero"
    LEGAL = "legal"
    EXTERNO = "externo"

class NivelProbabilidad(enum.Enum):
    MUY_BAJA = 1
    BAJA = 2
    MEDIA = 3
    ALTA = 4
    MUY_ALTA = 5

class NivelImpacto(enum.Enum):
    MUY_BAJO = 1
    BAJO = 2
    MEDIO = 3
    ALTO = 4
    MUY_ALTO = 5

class EstadoRiesgo(enum.Enum):
    IDENTIFICADO = "identificado"
    EN_SEGUIMIENTO = "en_seguimiento"
    MITIGADO = "mitigado"
    MATERIALIZADO = "materializado"
    CERRADO = "cerrado"

class Riesgo(db.Model):
    __tablename__ = 'riesgos'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    codigo = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.Enum(TipoRiesgo), nullable=False)
    probabilidad = db.Column(db.Enum(NivelProbabilidad), nullable=False)
    impacto = db.Column(db.Enum(NivelImpacto), nullable=False)
    estado = db.Column(db.Enum(EstadoRiesgo), default=EstadoRiesgo.IDENTIFICADO)
    plan_mitigacion = db.Column(db.Text)
    plan_contingencia = db.Column(db.Text)
    responsable_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fecha_identificacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_revision = db.Column(db.DateTime)
    fecha_cierre = db.Column(db.DateTime)
    costo_estimado = db.Column(db.Float, default=0)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    proyecto = db.relationship('Proyecto', backref='riesgos')
    responsable = db.relationship('User', foreign_keys=[responsable_id])
    
    def calcular_exposicion(self):
        """Calcula la exposición al riesgo (probabilidad * impacto)"""
        return self.probabilidad.value * self.impacto.value
    
    def nivel_riesgo(self):
        """Determina el nivel de riesgo basado en la exposición"""
        exposicion = self.calcular_exposicion()
        if exposicion >= 20:
            return "CRITICO"
        elif exposicion >= 15:
            return "ALTO"
        elif exposicion >= 10:
            return "MEDIO"
        elif exposicion >= 5:
            return "BAJO"
        else:
            return "MUY_BAJO"
    
    def color_riesgo(self):
        """Retorna el color asociado al nivel de riesgo"""
        nivel = self.nivel_riesgo()
        colores = {
            "CRITICO": "#DC2626",  # Rojo
            "ALTO": "#EA580C",     # Naranja
            "MEDIO": "#D97706",    # Amarillo
            "BAJO": "#16A34A",     # Verde
            "MUY_BAJO": "#059669"  # Verde oscuro
        }
        return colores.get(nivel, "#6B7280")
    
    def to_dict(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo.value,
            'probabilidad': {
                'valor': self.probabilidad.value,
                'texto': self.probabilidad.name
            },
            'impacto': {
                'valor': self.impacto.value,
                'texto': self.impacto.name
            },
            'estado': self.estado.value,
            'plan_mitigacion': self.plan_mitigacion,
            'plan_contingencia': self.plan_contingencia,
            'responsable_id': self.responsable_id,
            'responsable_nombre': self.responsable.nombre if self.responsable else None,
            'exposicion': self.calcular_exposicion(),
            'nivel_riesgo': self.nivel_riesgo(),
            'color_riesgo': self.color_riesgo(),
            'fecha_identificacion': self.fecha_identificacion.isoformat(),
            'fecha_revision': self.fecha_revision.isoformat() if self.fecha_revision else None,
            'fecha_cierre': self.fecha_cierre.isoformat() if self.fecha_cierre else None,
            'costo_estimado': self.costo_estimado,
            'activo': self.activo
        }

