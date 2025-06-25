
# Documento de Especificación Técnica para la Aplicación Web y Móvil "Avanzando"

---

## 1. Introducción
**Nombre del Proyecto:** Avanzando  
**Objetivo:** Desarrollar una aplicación web y móvil moderna, intuitiva y segura, con flujos de aprobación y un alta interacción de comunicaciones y reportes con el gestor del proyecto e interesados, para una activa gestión integral de proyectos de tecnología y software, con base en las buenas prácticas del PMI, PM2P, SCRUM y otros marcos de referencia ágiles e híbridos.

**Usuarios Objetivo:** Gestores de proyectos, equipos de desarrollo, clientes empresariales y consultores.

**Modelo de Negocio:** Freemium (con funcionalidades básicas gratuitas hasta un proyecto y sin lasa funciones de reportes y comunicaciones, opción estándar hasta 10 proyectos y las funciones de reportes y comunicaciones, con un costo mes de 20 USD y opción premium avanzadas ilimitado proyectos y las funciones de reportes y comunicaciones con un costo mes 50 USD por suscripción).

---

## 2. Requisitos Funcionales

### 2.1. Gestión de Proyectos
- Crear, editar y eliminar proyectos.
- Asignar proyectos a clientes.
- Cada proyecto con fases: Inicio, Planeación, Ejecución, Seguimiento y Control, Cierre.
- Plantillas preconfiguradas para documentación por fase.
- Avance por fases con validaciones y aprobaciones.

### 2.2. Documentación del Proyecto
- Generador de documentos por fase.
- Plantillas editables con historial de cambios.
- Posibilidad de carga de documentos externos.

### 2.3. Indicadores Clave de Desempeño (KPIs)
- Tiempo: Avance vs cronograma base.
- Alcance: Tareas entregadas vs planificadas.
- Costo: Ejecución presupuestal vs planeación.
- Dashboard visual con gráficas comparativas.

### 2.4. Gestión de Riesgos
- Registro y clasificación de riesgos.
- Matriz de probabilidad e impacto.
- Seguimiento y cierre de riesgos.

### 2.5. Recursos
- Asignación y seguimiento de recursos humanos y físicos.
- Control de disponibilidad y carga laboral.

### 2.6. Multi-proyecto y Multi-cliente
- Gestión paralela de múltiples proyectos.
- Segmentación de información por cliente.
- Tablero maestro de portafolio.

### 2.7. Roles y Permisos
- Control de usuarios con roles: Administrador, PM, Cliente, Recurso.
- Accesos segmentados por rol y proyecto.
- Trazabilidad de acciones por usuario.

### 2.8. Interfaz y Experiencia de Usuario
- UI moderna, con modo claro/oscuro.
- Navegación por menús intuitivos y tarjetas de proyecto.
- Responsive: acceso web y app móvil (iOS/Android).

### 2.9. Liquidación de Actividades y Costos
- Registro detallado de costos por actividad, fase y recurso.
- Generación de reportes automáticos por proyecto o cliente.
- Visualización comparativa entre costos estimados y reales.
- Exportación en PDF y Excel de liquidaciones por fase.
- Notificaciones automáticas para actividades no liquidadas.

---

## 3. Requisitos No Funcionales

- **Seguridad:** Autenticación OAuth2/JWT. Cifrado de datos en reposo y tránsito.
- **Escalabilidad:** Arquitectura basada en microservicios.
- **Disponibilidad:** SLA 99.9%, soporte para HA y balanceo de carga.
- **Rendimiento:** Respuesta menor a 2s en operaciones comunes.
- **Soporte Multi-idioma:** Inicialmente español e inglés.
- **Backups automáticos** diarios.

---

## 4. Arquitectura Propuesta

- **Frontend:** React.js (web) + React Native (móvil)
- **Backend:** Node.js + Express / NestJS
- **Base de Datos:** PostgreSQL (relacional) + Redis (caché)
- **Autenticación:** OAuth2.0 / JWT
- **APIs:** RESTful, escalables, documentadas con Swagger
- **Cloud & Hosting:** AWS / Azure / GCP (Docker + Kubernetes)
- **CI/CD:** GitHub Actions / GitLab CI + Docker

---

## 5. Estructura de Datos (Ejemplo Simplificado)

- **Usuario:** id, nombre, email, rol, cliente_id
- **Cliente:** id, nombre, sector, logo
- **Proyecto:** id, nombre, cliente_id, estado, fecha_inicio, fecha_fin
- **Fase:** id, proyecto_id, tipo, avance, fecha_inicio, fecha_fin
- **Documento:** id, fase_id, nombre, tipo, link, version
- **KPI:** id, proyecto_id, tipo, valor_planeado, valor_actual
- **Riesgo:** id, proyecto_id, descripción, impacto, probabilidad, estado
- **Recurso:** id, nombre, tipo (humano/físico), disponibilidad, proyecto_id
- **Costo:** id, fase_id, actividad, tipo_costo (recurso humano, insumo, indirecto), monto_estimado, monto_real, fecha_registro

---

## 6. Flujos de Navegación

### Inicio
- Login / Registro
- Dashboard resumen (proyectos activos, alertas, KPIs clave)

### Módulos principales
1. **Portafolio de Proyectos**
2. **Documentación por Fase**
3. **Gestor de Riesgos**
4. **KPIs del Proyecto**
5. **Recursos**
6. **Comunicaciones y reportes**
7. **Clientes y Usuarios**
8. **Liquidación de Actividades y Costos**

---

## 7. Integraciones
- Integración opcional con Microsoft 365, Google Drive, Slack, Whatsapp y Telegram.
- Exportación de reportes en PDF/Excel.

---

## 8. Roadmap de Desarrollo (MVP)

1. **Fase 1:** Registro/Login, Gestión de Proyectos, Documentación por Fase, Roles.
2. **Fase 2:** KPIs, Gestión de Riesgos, Recursos.
3. **Fase 3:** Dashboard portafolio, App móvil, Integraciones.
4. **Fase 4:** Módulo Premium, funcionalidades avanzadas, IA para predicción de riesgos y atrasos.

---

## 9. Consideraciones Finales
- Cumplir con GDPR y estándares ISO 27001.
- Accesibilidad conforme a WCAG 2.1.
- Arquitectura abierta para integración futura con ERP y CRMs.

---

**Fin del documento.**