# ControlPM

**ControlPM** es una aplicación web y móvil diseñada para la administración y gestión integral de proyectos de tecnología y software, bajo un modelo de negocio freemium. La plataforma busca optimizar la gestión de proyectos para gestores, equipos de desarrollo, clientes empresariales y consultores, basándose en las buenas prácticas de marcos de referencia ágiles e híbridos como PMI, PM2P y SCRUM.

## Características Principales

-   **Gestión de Proyectos:** Creación, edición y eliminación de proyectos, con asignación a clientes y estructuración por fases (Inicio, Planeación, Ejecución, Seguimiento y Control, Cierre).
-   **Documentación:** Generación de documentos por fase, plantillas editables y carga de documentos externos.
-   **KPIs:** Seguimiento de indicadores clave de desempeño para tiempo, alcance y costo, con dashboards visuales.
-   **Gestión de Riesgos:** Registro, clasificación, seguimiento y cierre de riesgos.
-   **Recursos:** Asignación y seguimiento de recursos humanos y físicos, control de disponibilidad y carga laboral.
-   **Multi-proyecto y Multi-cliente:** Gestión paralela de múltiples proyectos y segmentación de información por cliente.
-   **Roles y Permisos:** Control de acceso granular basado en roles (Administrador, PM, Cliente, Recurso).
-   **Liquidación de Actividades y Costos:** Registro detallado de costos, generación de reportes automáticos y notificaciones.
-   **Interfaz de Usuario:** UI moderna, responsive, con modo claro/oscuro y acceso web/móvil.

## Arquitectura y Tecnología

La aplicación se construye sobre una arquitectura de microservicios, utilizando las siguientes tecnologías:

-   **Frontend Web:** React.js
-   **Frontend Móvil:** React Native
-   **Backend:** Node.js (NestJS)
-   **Base de Datos:** PostgreSQL (relacional) y Redis (caché)
-   **Autenticación:** OAuth2.0 / JWT
-   **APIs:** RESTful, documentadas con Swagger
-   **Cloud & Hosting:** AWS / Azure / GCP (Docker + Kubernetes)
-   **CI/CD:** GitHub Actions

## Roadmap (MVP)

El desarrollo se realizará en fases incrementales:

1.  **Fase 1:** Login/Registro, Gestión de Proyectos y Fases, Roles.
2.  **Fase 2:** KPIs, Gestión de Riesgos, Recursos.
3.  **Fase 3:** Dashboard Portafolio, App Móvil, Integraciones.
4.  **Fase 4:** Módulo Freemium, funcionalidades avanzadas con IA.

## Documentación

La documentación detallada del proyecto, incluyendo especificaciones técnicas, resumen y plan de desarrollo, se encuentra en la carpeta `docs/`.


