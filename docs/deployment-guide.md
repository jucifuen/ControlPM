# Guía de Despliegue - Proyecto Avanzando

## Resumen Ejecutivo

Esta guía proporciona instrucciones completas para el despliegue de la aplicación "Avanzando" en diferentes entornos (desarrollo, staging, producción).

## Arquitectura de Despliegue

### Componentes Principales
- **Frontend:** React.js servido por Nginx
- **Backend:** Flask API con Gunicorn
- **Base de Datos:** PostgreSQL 15
- **Cache:** Redis
- **Proxy Reverso:** Nginx
- **Monitoreo:** Prometheus + Grafana

## Requisitos del Sistema

### Mínimos (Desarrollo)
- CPU: 2 cores
- RAM: 4GB
- Almacenamiento: 20GB
- Docker 20.10+
- Docker Compose 2.0+

### Recomendados (Producción)
- CPU: 4+ cores
- RAM: 8GB+
- Almacenamiento: 100GB+ SSD
- Kubernetes 1.25+
- Load Balancer
- SSL/TLS certificados

## Despliegue con Docker Compose

### 1. Preparación del Entorno

```bash
# Clonar repositorio
git clone https://github.com/jucifuen/ControlPM.git
cd ControlPM

# Crear archivo de variables de entorno
cp .env.example .env
```

### 2. Configuración de Variables

Editar `.env`:
```bash
# Base de datos
POSTGRES_PASSWORD=secure_password_change_me
POSTGRES_DB=avanzando_db

# Redis
REDIS_PASSWORD=redis_secure_password

# JWT
JWT_SECRET_KEY=super_secret_jwt_key_change_in_production

# URLs
REACT_APP_API_URL=https://api.avanzando.app
CORS_ORIGINS=https://avanzando.app,https://www.avanzando.app

# Monitoreo
GRAFANA_PASSWORD=admin_secure_password
```

### 3. Despliegue

```bash
# Construir y levantar servicios
docker-compose up -d

# Verificar estado
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 4. Inicialización de Base de Datos

```bash
# Ejecutar migraciones
docker-compose exec backend python -c "from src.models import db; db.create_all()"

# Crear usuario administrador
docker-compose exec backend python scripts/create_admin.py
```

## Despliegue en Kubernetes

### 1. Preparación del Cluster

```bash
# Crear namespace
kubectl apply -f k8s/namespace.yaml

# Configurar secrets
kubectl create secret generic avanzando-secrets \
  --from-literal=POSTGRES_PASSWORD=secure_password \
  --from-literal=REDIS_PASSWORD=redis_password \
  --from-literal=JWT_SECRET_KEY=jwt_secret_key \
  -n avanzando
```

### 2. Despliegue de Servicios

```bash
# Base de datos
kubectl apply -f k8s/postgres.yaml

# Redis
kubectl apply -f k8s/redis.yaml

# Backend
kubectl apply -f k8s/backend.yaml

# Frontend
kubectl apply -f k8s/frontend.yaml

# Ingress
kubectl apply -f k8s/ingress.yaml
```

### 3. Verificación

```bash
# Estado de pods
kubectl get pods -n avanzando

# Logs
kubectl logs -f deployment/avanzando-backend -n avanzando

# Servicios
kubectl get services -n avanzando
```

## Configuración de SSL/TLS

### Con Let's Encrypt (Certbot)

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d avanzando.app -d www.avanzando.app

# Renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Con Kubernetes (cert-manager)

```bash
# Instalar cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Configurar ClusterIssuer
kubectl apply -f k8s/cert-manager-issuer.yaml
```

## Monitoreo y Logging

### Prometheus + Grafana

```bash
# Acceder a Grafana
http://localhost:3001
# Usuario: admin
# Contraseña: definida en GRAFANA_PASSWORD

# Dashboards preconfigurados:
# - Sistema general
# - Métricas de aplicación
# - Base de datos
# - Performance
```

### Logs Centralizados

```bash
# Ver logs en tiempo real
docker-compose logs -f backend
docker-compose logs -f frontend

# Logs de Kubernetes
kubectl logs -f deployment/avanzando-backend -n avanzando
```

## Backup y Recuperación

### Base de Datos

```bash
# Backup automático diario
docker-compose exec postgres pg_dump -U avanzando_user avanzando_db > backup_$(date +%Y%m%d).sql

# Restauración
docker-compose exec -T postgres psql -U avanzando_user avanzando_db < backup_20231226.sql
```

### Archivos de Usuario

```bash
# Backup de uploads
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz backend/avanzando-backend/uploads/

# Sincronización con S3 (opcional)
aws s3 sync backend/avanzando-backend/uploads/ s3://avanzando-uploads/
```

## Escalabilidad

### Horizontal Scaling

```bash
# Docker Compose
docker-compose up -d --scale backend=3

# Kubernetes
kubectl scale deployment avanzando-backend --replicas=3 -n avanzando
```

### Load Balancing

```yaml
# nginx.conf
upstream backend {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
}
```

## Seguridad

### Checklist de Seguridad

- [ ] Cambiar todas las contraseñas por defecto
- [ ] Configurar SSL/TLS
- [ ] Firewall configurado (puertos 80, 443, 22)
- [ ] Actualizaciones de seguridad automáticas
- [ ] Backup automático configurado
- [ ] Monitoreo de logs de seguridad
- [ ] Rate limiting configurado
- [ ] CORS configurado correctamente

### Hardening

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Configurar firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Fail2ban para SSH
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

## Troubleshooting

### Problemas Comunes

1. **Error de conexión a base de datos**
   ```bash
   # Verificar estado de PostgreSQL
   docker-compose logs postgres
   
   # Verificar conectividad
   docker-compose exec backend pg_isready -h postgres -p 5432
   ```

2. **Frontend no carga**
   ```bash
   # Verificar build
   docker-compose logs frontend
   
   # Verificar nginx
   docker-compose exec nginx nginx -t
   ```

3. **Performance lenta**
   ```bash
   # Verificar recursos
   docker stats
   
   # Verificar logs de aplicación
   docker-compose logs backend | grep ERROR
   ```

### Comandos Útiles

```bash
# Reiniciar servicios
docker-compose restart backend

# Limpiar volúmenes
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache

# Acceso a contenedor
docker-compose exec backend bash
```

## Mantenimiento

### Actualizaciones

```bash
# Backup antes de actualizar
./scripts/backup.sh

# Pull de cambios
git pull origin main

# Reconstruir y desplegar
docker-compose build
docker-compose up -d

# Verificar funcionamiento
./scripts/health-check.sh
```

### Limpieza

```bash
# Limpiar imágenes no utilizadas
docker image prune -a

# Limpiar volúmenes huérfanos
docker volume prune

# Logs rotativos
sudo logrotate -f /etc/logrotate.conf
```

## Contacto y Soporte

- **Documentación:** [docs.avanzando.app](https://docs.avanzando.app)
- **Issues:** [GitHub Issues](https://github.com/jucifuen/ControlPM/issues)
- **Email:** soporte@avanzando.app

---

**Última actualización:** 26 de Junio de 2025  
**Versión:** 1.0

