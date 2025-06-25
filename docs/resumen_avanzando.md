# Resumen de Especificaciones Técnicas: Aplicación "Avanzando"

Este documento presenta un resumen estructurado de las especificaciones técnicas para el desarrollo de la aplicación "Avanzando", una plataforma web y móvil diseñada para la administración y gestión de proyectos de múltiples clientes bajo un modelo de negocio freemium. El análisis se basa en el documento `Especificaciones_tecnicas_Avanzando_ver2.md`.

## 1. Módulos Funcionales

La aplicación "Avanzando" se concibe con una serie de módulos funcionales clave que cubren el ciclo de vida completo de la gestión de proyectos, desde la creación hasta el cierre, incluyendo aspectos administrativos y de seguimiento. A continuación, se detallan los módulos principales:

### 1.1. Gestión de Proyectos
Permite la creación, edición y eliminación de proyectos, con la capacidad de asignarlos a clientes específicos. Cada proyecto se estructura en fases predefinidas (Inicio, Planeación, Ejecución, Seguimiento y Control, Cierre), con validaciones y aprobaciones para el avance entre ellas. Se incluyen plantillas preconfiguradas para la documentación de cada fase.

### 1.2. Documentación del Proyecto
Facilita la generación de documentos por fase, utilizando plantillas editables con historial de cambios. También soporta la carga de documentos externos, centralizando toda la información relevante del proyecto.

### 1.3. Indicadores Clave de Desempeño (KPIs)
Proporciona seguimiento de KPIs relacionados con el tiempo (avance vs. cronograma), alcance (tareas entregadas vs. planificadas) y costo (ejecución presupuestal vs. planeación). Se visualizan a través de un dashboard con gráficas comparativas para una rápida comprensión del estado del proyecto.

### 1.4. Gestión de Riesgos
Permite el registro y clasificación de riesgos, utilizando una matriz de probabilidad e impacto para su evaluación. Incluye funcionalidades para el seguimiento y cierre de los riesgos identificados, asegurando una gestión proactiva.

### 1.5. Recursos
Administra la asignación y seguimiento de recursos, tanto humanos como físicos. Facilita el control de la disponibilidad y la carga laboral de los recursos, optimizando su utilización en los proyectos.

### 1.6. Multi-proyecto y Multi-cliente
Diseñado para gestionar múltiples proyectos de forma paralela, con segmentación clara de la información por cliente. Ofrece un tablero maestro de portafolio para una visión consolidada de todos los proyectos.

### 1.7. Roles y Permisos
Implementa un control de acceso basado en roles (Administrador, PM, Cliente, Recurso), con permisos segmentados por rol y proyecto. Esto asegura que cada usuario tenga acceso únicamente a la información y funcionalidades pertinentes a su rol, manteniendo la trazabilidad de todas las acciones.

### 1.8. Interfaz y Experiencia de Usuario (UI/UX)
La aplicación contará con una UI moderna, que incluye modos claro y oscuro, y una navegación intuitiva a través de menús y tarjetas de proyecto. Será completamente responsive, accesible tanto desde la web como desde aplicaciones móviles nativas (iOS/Android).

### 1.9. Liquidación de Actividades y Costos
Permite el registro detallado de costos por actividad, fase y recurso. Genera reportes automáticos por proyecto o cliente, con visualización comparativa entre costos estimados y reales. Soporta la exportación de liquidaciones en PDF y Excel, y envía notificaciones automáticas para actividades no liquidadas.




## 2. Arquitectura Propuesta

La arquitectura de "Avanzando" se basa en un enfoque de microservicios para garantizar escalabilidad, disponibilidad y rendimiento. Se propone una pila tecnológica moderna y robusta:

-   **Frontend:** Se desarrollará una aplicación web utilizando **React.js** y una aplicación móvil nativa para iOS y Android con **React Native**. Esto asegura una experiencia de usuario consistente y optimizada en diferentes plataformas.
-   **Backend:** Se construirá con **Node.js**, con preferencia por el framework **NestJS** para aprovechar su arquitectura modular y escalable. Esto permitirá una gestión eficiente de las APIs y la lógica de negocio.
-   **Base de Datos:** Se utilizará **PostgreSQL** como base de datos relacional principal, ideal para la gestión estructurada de proyectos, usuarios y datos financieros. **Redis** se implementará para el almacenamiento en caché, mejorando el rendimiento y la velocidad de respuesta de la aplicación.
-   **Autenticación:** La seguridad se garantizará mediante **OAuth2.0** para la autorización y **JWT (JSON Web Tokens)** para la autenticación, proporcionando un sistema seguro y eficiente para el acceso de usuarios.
-   **APIs:** Se diseñarán **APIs RESTful** que serán escalables y estarán documentadas con **Swagger**, facilitando la integración y el consumo por parte de los clientes frontend y posibles integraciones externas.
-   **Cloud & Hosting:** El despliegue se realizará en plataformas de nube como **AWS, Azure o GCP**, utilizando **Docker** para la contenerización de los microservicios y **Kubernetes** para la orquestación y gestión de los contenedores, asegurando alta disponibilidad y escalabilidad horizontal.
-   **CI/CD:** Se implementarán pipelines de Integración Continua y Despliegue Continuo utilizando **GitHub Actions** o **GitLab CI**, junto con Docker, para automatizar el proceso de construcción, prueba y despliegue del código, garantizando entregas rápidas y fiables.




## 3. Requisitos No Funcionales

Además de las funcionalidades, la aplicación "Avanzando" debe cumplir con una serie de requisitos no funcionales críticos para su éxito y operación:

-   **Seguridad:** Implementación de autenticación **OAuth2/JWT** y cifrado de datos tanto en reposo como en tránsito para proteger la información sensible de los usuarios y proyectos.
-   **Escalabilidad:** La arquitectura basada en microservicios permitirá que la aplicación escale horizontalmente para manejar un creciente número de usuarios y proyectos sin comprometer el rendimiento.
-   **Disponibilidad:** Se busca un **SLA del 99.9%**, con soporte para Alta Disponibilidad (HA) y balanceo de carga, asegurando que la aplicación esté siempre accesible para los usuarios.
-   **Rendimiento:** Las operaciones comunes de la aplicación deben tener un tiempo de respuesta inferior a 2 segundos, garantizando una experiencia de usuario fluida y eficiente.
-   **Soporte Multi-idioma:** Inicialmente, la aplicación soportará español e inglés, con la posibilidad de añadir más idiomas en el futuro para atender a una base de usuarios global.
-   **Backups automáticos:** Se realizarán copias de seguridad automáticas diarias de la base de datos para prevenir la pérdida de información y facilitar la recuperación ante desastres.
-   **Cumplimiento Normativo:** La aplicación deberá cumplir con normativas de privacidad como **GDPR** y estándares de seguridad como **ISO 27001**.
-   **Accesibilidad:** Se garantizará la accesibilidad conforme a las directrices **WCAG 2.1**, haciendo la aplicación usable para personas con diversas capacidades.
-   **Arquitectura Abierta:** El diseño de la arquitectura permitirá futuras integraciones con sistemas externos como ERP y CRM, aumentando la versatilidad y el valor de la plataforma.




## 4. Roadmap de Desarrollo (MVP)

El desarrollo de la aplicación "Avanzando" se ha planificado en fases, priorizando las funcionalidades clave para un Producto Mínimo Viable (MVP) y escalando progresivamente. El roadmap propuesto es el siguiente:

-   **Fase 1:** Se enfoca en las funcionalidades básicas para la gestión de proyectos y usuarios. Incluye el sistema de Registro/Login, la Gestión de Proyectos (creación, edición, eliminación, asignación a clientes, fases), la Documentación por Fase (generación y carga de documentos) y la implementación de Roles y Permisos.
-   **Fase 2:** Amplía las capacidades de seguimiento y gestión de riesgos. Incorpora los Indicadores Clave de Desempeño (KPIs) con sus respectivos dashboards, la Gestión de Riesgos (registro, clasificación, seguimiento y cierre) y la administración de Recursos (asignación, seguimiento, disponibilidad y carga laboral).
-   **Fase 3:** Mejora la visibilidad y la conectividad de la plataforma. Se desarrollará el Dashboard de Portafolio para una visión consolidada de todos los proyectos, la App móvil (React Native) para iOS y Android, y las Integraciones con servicios externos como Microsoft 365, Google Drive, Slack, WhatsApp y Telegram.
-   **Fase 4:** Introduce el modelo de negocio freemium y funcionalidades avanzadas. Se implementará el Módulo Premium con sus características exclusivas, funcionalidades avanzadas (posiblemente personalización, reportes avanzados) y la integración de Inteligencia Artificial para la predicción de riesgos y atrasos en los proyectos.


