#!/bin/bash

# Script de Despliegue Automatizado - Proyecto Avanzando
# Versión: 1.0
# Fecha: 26 de Junio de 2025

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuración
ENVIRONMENT=${1:-development}
PROJECT_DIR=$(pwd)
BACKUP_DIR="$PROJECT_DIR/backups"
LOG_FILE="$PROJECT_DIR/logs/deploy_$(date +%Y%m%d_%H%M%S).log"

# Crear directorios necesarios
mkdir -p "$BACKUP_DIR" "$PROJECT_DIR/logs"

# Función de backup
backup_database() {
    log_info "Creando backup de base de datos..."
    
    if [ "$ENVIRONMENT" = "production" ]; then
        BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
        docker-compose exec -T postgres pg_dump -U avanzando_user avanzando_db > "$BACKUP_FILE"
        
        if [ $? -eq 0 ]; then
            log_success "Backup creado: $BACKUP_FILE"
        else
            log_error "Error creando backup"
            exit 1
        fi
    else
        log_info "Saltando backup en entorno $ENVIRONMENT"
    fi
}

# Función de verificación de requisitos
check_requirements() {
    log_info "Verificando requisitos del sistema..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker no está instalado"
        exit 1
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose no está instalado"
        exit 1
    fi
    
    # Verificar archivo .env
    if [ ! -f ".env" ]; then
        log_warning "Archivo .env no encontrado, copiando desde .env.example"
        cp .env.example .env
        log_warning "Por favor, edita el archivo .env con tus configuraciones"
    fi
    
    log_success "Requisitos verificados"
}

# Función de construcción
build_images() {
    log_info "Construyendo imágenes Docker..."
    
    docker-compose build --no-cache
    
    if [ $? -eq 0 ]; then
        log_success "Imágenes construidas exitosamente"
    else
        log_error "Error construyendo imágenes"
        exit 1
    fi
}

# Función de despliegue
deploy_services() {
    log_info "Desplegando servicios..."
    
    # Detener servicios existentes
    docker-compose down
    
    # Levantar servicios
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        log_success "Servicios desplegados exitosamente"
    else
        log_error "Error desplegando servicios"
        exit 1
    fi
}

# Función de verificación de salud
health_check() {
    log_info "Verificando salud de los servicios..."
    
    # Esperar a que los servicios estén listos
    sleep 30
    
    # Verificar backend
    if curl -f http://localhost:5000/health &> /dev/null; then
        log_success "Backend está funcionando"
    else
        log_error "Backend no responde"
        return 1
    fi
    
    # Verificar frontend
    if curl -f http://localhost:3000 &> /dev/null; then
        log_success "Frontend está funcionando"
    else
        log_error "Frontend no responde"
        return 1
    fi
    
    # Verificar base de datos
    if docker-compose exec -T postgres pg_isready -U avanzando_user &> /dev/null; then
        log_success "Base de datos está funcionando"
    else
        log_error "Base de datos no responde"
        return 1
    fi
    
    log_success "Todos los servicios están funcionando correctamente"
}

# Función de inicialización de base de datos
init_database() {
    log_info "Inicializando base de datos..."
    
    # Esperar a que la base de datos esté lista
    sleep 10
    
    # Crear tablas
    docker-compose exec backend python -c "
from src.models.user import db
from src.models.project import Proyecto
from src.models.kpi import KPI
from src.models.riesgo import Riesgo
from src.models.recurso import Recurso
from src.models.subscription import Subscription
from src.models.ai_prediction import AIPrediction
from src.models.documento import Documento, PlantillaDocumento
from src.models.liquidacion import Liquidacion, DetalleGasto, RegistroHoras
db.create_all()
print('Tablas creadas exitosamente')
"
    
    if [ $? -eq 0 ]; then
        log_success "Base de datos inicializada"
    else
        log_error "Error inicializando base de datos"
        exit 1
    fi
}

# Función de limpieza
cleanup() {
    log_info "Limpiando recursos no utilizados..."
    
    # Limpiar imágenes no utilizadas
    docker image prune -f
    
    # Limpiar volúmenes huérfanos
    docker volume prune -f
    
    log_success "Limpieza completada"
}

# Función principal
main() {
    log_info "Iniciando despliegue en entorno: $ENVIRONMENT"
    log_info "Directorio del proyecto: $PROJECT_DIR"
    log_info "Log file: $LOG_FILE"
    
    # Ejecutar pasos del despliegue
    check_requirements
    
    if [ "$ENVIRONMENT" = "production" ]; then
        backup_database
    fi
    
    build_images
    deploy_services
    init_database
    health_check
    
    if [ $? -eq 0 ]; then
        log_success "Despliegue completado exitosamente"
        
        echo ""
        echo "🚀 Aplicación desplegada:"
        echo "   Frontend: http://localhost:3000"
        echo "   Backend API: http://localhost:5000"
        echo "   Grafana: http://localhost:3001"
        echo ""
        echo "📊 Para ver el estado de los servicios:"
        echo "   docker-compose ps"
        echo ""
        echo "📝 Para ver los logs:"
        echo "   docker-compose logs -f"
        
    else
        log_error "Despliegue falló"
        exit 1
    fi
    
    cleanup
}

# Función de ayuda
show_help() {
    echo "Uso: $0 [ENVIRONMENT]"
    echo ""
    echo "ENVIRONMENT:"
    echo "  development  - Entorno de desarrollo (por defecto)"
    echo "  staging      - Entorno de staging"
    echo "  production   - Entorno de producción"
    echo ""
    echo "Ejemplos:"
    echo "  $0                    # Despliegue en desarrollo"
    echo "  $0 production         # Despliegue en producción"
    echo ""
}

# Verificar argumentos
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

# Ejecutar función principal
main 2>&1 | tee "$LOG_FILE"

