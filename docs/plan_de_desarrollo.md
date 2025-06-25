# Plan de Desarrollo para la Aplicación "Avanzando"

Este documento describe el plan de desarrollo para la aplicación "Avanzando", una plataforma integral de gestión de proyectos web y móvil. El plan se alinea con las especificaciones técnicas y el roadmap MVP definidos, priorizando un enfoque ágil y modular para la construcción de la aplicación.

## 1. Introducción

El desarrollo de "Avanzando" se llevará a cabo siguiendo las mejores prácticas de ingeniería de software, utilizando una arquitectura de microservicios y una pila tecnológica moderna. El objetivo es entregar una aplicación robusta, escalable y fácil de mantener, que cumpla con los requisitos funcionales y no funcionales establecidos. Se enfatizará la colaboración continua, la integración y entrega continua (CI/CD), y la calidad del código a través de pruebas exhaustivas.

## 2. Metodología de Desarrollo

Se adoptará una metodología de desarrollo ágil, preferiblemente Scrum, para gestionar el proyecto. Esto permitirá una entrega iterativa de funcionalidades, adaptabilidad a los cambios y una comunicación constante con el usuario. Cada fase del roadmap se tratará como un conjunto de sprints, con objetivos claros y entregables definidos.

## 3. Pila Tecnológica

La pila tecnológica seleccionada para "Avanzando" es la siguiente:

-   **Frontend Web:** React.js
-   **Frontend Móvil:** React Native
-   **Backend:** Node.js (NestJS)
-   **Base de Datos:** PostgreSQL
-   **Caché:** Redis
-   **Autenticación:** OAuth2.0 y JWT
-   **Contenerización:** Docker
-   **Orquestación:** Kubernetes (para despliegue en la nube)
-   **CI/CD:** GitHub Actions

Esta combinación de tecnologías proporciona un ecosistema potente para construir una aplicación de alto rendimiento y escalabilidad.




## 4. Fases de Desarrollo

El plan de desarrollo se alinea directamente con el roadmap MVP, dividiendo el proyecto en fases incrementales. Cada fase se centrará en la entrega de un conjunto de funcionalidades coherentes y probables.

### 4.1. Fase 1: Login/Registro, Gestión de Proyectos y Fases, Roles

Esta fase inicial sienta las bases de la aplicación, permitiendo a los usuarios registrarse, iniciar sesión y gestionar los aspectos fundamentales de los proyectos. Se desarrollarán los siguientes componentes:

-   **Módulo de Autenticación y Autorización:**
    -   **Registro de Usuarios:** Implementación de la funcionalidad de registro de nuevos usuarios, incluyendo validación de datos y confirmación (si aplica).
    -   **Login de Usuarios:** Desarrollo del sistema de inicio de sesión seguro utilizando OAuth2 y JWT, con manejo de sesiones y tokens.
    -   **Gestión de Roles:** Creación de los roles de usuario (Administrador, PM, Cliente, Recurso) y asignación de permisos básicos a cada rol.
    -   **Recuperación de Contraseña:** Funcionalidad para que los usuarios puedan restablecer sus contraseñas.

-   **Módulo de Gestión de Proyectos:**
    -   **Creación, Edición y Eliminación de Proyectos:** Implementación de las interfaces y la lógica de backend para que los usuarios con los roles adecuados puedan crear, modificar y eliminar proyectos.
    -   **Asignación de Proyectos a Clientes:** Funcionalidad para vincular proyectos a clientes existentes.
    -   **Gestión de Fases del Proyecto:** Definición y control de las fases del proyecto (Inicio, Planeación, Ejecución, Seguimiento y Control, Cierre), incluyendo la lógica para el avance entre fases y las validaciones necesarias.
    -   **Plantillas de Documentación:** Integración de plantillas preconfiguradas para la documentación asociada a cada fase del proyecto.

-   **Integración Frontend-Backend:**
    -   Desarrollo de las interfaces de usuario en React.js (web) y React Native (móvil) para las funcionalidades de registro, login y gestión de proyectos.
    -   Implementación de las APIs RESTful en NestJS para soportar las operaciones de frontend.

### 4.2. Fase 2: KPIs, Gestión de Riesgos, Recursos

Esta fase se centrará en la adición de funcionalidades de seguimiento y control, cruciales para la gestión efectiva de proyectos.

-   **Módulo de KPIs:**
    -   **Cálculo y Visualización de KPIs:** Desarrollo de la lógica para calcular KPIs de tiempo, alcance y costo, y su representación visual en dashboards interactivos.
    -   **Integración de Datos:** Conexión con los datos de proyectos y tareas para alimentar los cálculos de KPIs.

-   **Módulo de Gestión de Riesgos:**
    -   **Registro y Clasificación de Riesgos:** Funcionalidad para registrar nuevos riesgos, asignándoles una descripción, probabilidad e impacto.
    -   **Matriz de Riesgos:** Implementación de una matriz visual para la clasificación y priorización de riesgos.
    -   **Seguimiento y Cierre de Riesgos:** Herramientas para monitorear el estado de los riesgos y marcarlos como cerrados una vez mitigados.

-   **Módulo de Recursos:**
    -   **Asignación y Seguimiento de Recursos:** Funcionalidad para asignar recursos humanos y físicos a proyectos y tareas.
    -   **Control de Disponibilidad y Carga Laboral:** Herramientas para visualizar la disponibilidad de los recursos y su carga de trabajo, evitando la sobreasignación.

### 4.3. Fase 3: Dashboard Portafolio, App Móvil, Integraciones

Esta fase se enfocará en mejorar la visibilidad a nivel de portafolio y expandir la accesibilidad de la aplicación.

-   **Dashboard de Portafolio:**
    -   **Vista Consolidada de Proyectos:** Desarrollo de un dashboard que proporcione una visión general de todos los proyectos, permitiendo filtrar por cliente y estado.
    -   **Alertas y Resúmenes:** Inclusión de alertas clave y resúmenes ejecutivos del estado del portafolio.

-   **Aplicación Móvil (React Native):**
    -   **Desarrollo de la App Móvil:** Implementación de las funcionalidades principales de la aplicación en React Native, priorizando la experiencia de usuario móvil.
    -   **Sincronización de Datos:** Asegurar la sincronización eficiente de datos entre la aplicación web y móvil.

-   **Módulo de Integraciones:**
    -   **Integración con Herramientas de Colaboración:** Desarrollo de conectores para Microsoft 365, Google Drive, Slack, WhatsApp y Telegram, permitiendo la comunicación y el intercambio de documentos.
    -   **Exportación de Reportes:** Funcionalidad para exportar reportes en formatos PDF y Excel.

### 4.4. Fase 4: Módulo Freemium y Funcionalidades Premium con IA

La fase final del MVP se centrará en la monetización y la incorporación de capacidades avanzadas.

-   **Módulo Freemium:**
    -   **Gestión de Suscripciones:** Implementación de la lógica para gestionar los diferentes niveles de suscripción (Freemium, Estándar, Premium) y sus respectivas limitaciones de funcionalidad.
    -   **Control de Acceso a Funcionalidades Premium:** Restricción de acceso a ciertas características basadas en el plan de suscripción del usuario.

-   **Funcionalidades Premium con IA:**
    -   **Predicción de Riesgos y Atrasos:** Integración de modelos de inteligencia artificial para analizar datos del proyecto y predecir posibles riesgos o desviaciones en el cronograma.
    -   **Análisis Predictivo:** Herramientas de análisis avanzado para ofrecer insights y recomendaciones a los gestores de proyectos.




## 5. Gestión de Repositorio y CI/CD

La gestión del código fuente y el proceso de despliegue serán críticos para el éxito del proyecto. Se utilizará GitHub como plataforma de repositorio y GitHub Actions para la automatización de CI/CD.

### 5.1. Repositorio GitHub

-   **URL del Repositorio:** `https://github.com/jucifuen/ControlPM.git`
-   **Token de Acceso:** `` (Este token se utilizará para las operaciones automatizadas de CI/CD y no debe ser expuesto públicamente).

### 5.2. Estructura de Ramas

Se adoptará una estrategia de ramificación basada en Git Flow o similar, con las siguientes ramas principales:

-   `main`: Rama protegida que contendrá el código listo para producción.
-   `develop`: Rama principal para la integración de nuevas funcionalidades y correcciones de errores.
-   `feature/nombre-funcionalidad`: Ramas para el desarrollo de nuevas funcionalidades, por ejemplo, `feature/usuarios`, `feature/kpis`.
-   `bugfix/descripcion-bug`: Ramas para la corrección de errores específicos.
-   `release/version`: Ramas para preparar nuevas versiones de la aplicación.

### 5.3. Workflows de GitHub Actions para CI/CD

Se configurarán workflows automatizados en GitHub Actions para asegurar la calidad del código y facilitar el despliegue continuo. Los workflows incluirán:

-   **Integración Continua (CI):**
    -   **Disparadores:** Ejecución automática en cada `push` a las ramas `develop` y `feature/*`, y en cada `pull request`.
    -   **Pasos:**
        -   Checkout del código.
        -   Instalación de dependencias (Node.js, Python, etc.).
        -   Ejecución de pruebas unitarias y de integración (Jest, Supertest).
        -   Análisis de código estático (ESLint, Prettier).
        -   Construcción de los artefactos (frontend web, frontend móvil, backend).
        -   Generación de imágenes Docker para los microservicios.
-   **Despliegue Continuo (CD):**
    -   **Disparadores:** Ejecución automática en cada `push` a la rama `main` (para despliegue a producción) y a la rama `develop` (para despliegue a entorno de staging/QA).
    -   **Pasos:**
        -   Autenticación en el proveedor de nube (AWS/Azure/GCP).
        -   Despliegue de las imágenes Docker a Kubernetes.
        -   Actualización de la base de datos (migraciones).
        -   Notificaciones de despliegue (Slack, Email).

Se asegurará que los secretos (como el token de acceso de GitHub y las credenciales de la nube) se gestionen de forma segura utilizando las funcionalidades de secretos de GitHub Actions.


