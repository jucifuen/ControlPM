# Plan de Pruebas Funcionales y End-to-End para "Avanzando"

Este documento detalla el plan de pruebas funcionales y end-to-end (E2E) para la aplicación "Avanzando", cubriendo los módulos funcionales identificados en las especificaciones técnicas. El objetivo es asegurar la calidad, fiabilidad y el correcto funcionamiento de la aplicación en todas sus interacciones.

## 1. Introducción

El plan de pruebas se estructura para validar cada módulo funcional de manera individual y, posteriormente, verificar la integración y el flujo completo de las funcionalidades críticas desde la perspectiva del usuario final. Se emplearán pruebas funcionales para asegurar que cada característica cumple con los requisitos definidos y pruebas E2E para confirmar que los flujos de negocio operan correctamente a través de los diferentes componentes del sistema (frontend, backend, base de datos).

## 2. Estrategia de Pruebas

La estrategia de pruebas se basará en un enfoque de pruebas de caja negra, donde se validará la funcionalidad de la aplicación sin conocimiento de su estructura interna. Se priorizarán las pruebas de regresión para asegurar que los cambios o nuevas funcionalidades no introduzcan defectos en áreas existentes. Se utilizarán herramientas de automatización para las pruebas E2E, lo que permitirá una ejecución eficiente y repetible.

## 3. Alcance de las Pruebas

El alcance de las pruebas cubre todos los módulos funcionales y los requisitos no funcionales críticos, incluyendo:

-   **Módulos Funcionales:** Gestión de Proyectos, Documentación, KPIs, Gestión de Riesgos, Recursos, Multi-proyecto/Multi-cliente, Roles y Permisos, UI/UX, Liquidación de Actividades y Costos.
-   **Requisitos No Funcionales:** Seguridad (autenticación, cifrado), Escalabilidad, Disponibilidad, Rendimiento, Multi-idioma, Backups.

## 4. Casos de Prueba por Módulo Funcional

### 4.1. Módulo de Gestión de Proyectos

**Objetivo:** Validar la creación, edición, eliminación y asignación de proyectos, así como el avance por fases y la aplicación de plantillas.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| GP-001 | Crear un nuevo proyecto con todos los campos obligatorios. | Usuario con rol 'Administrador' o 'PM' logueado. | 1. Navegar a la sección 'Crear Proyecto'.\n2. Rellenar todos los campos obligatorios (Nombre, Cliente, Fechas, etc.).\n3. Seleccionar una plantilla de documentación.\n4. Hacer clic en 'Guardar'. | El proyecto se crea exitosamente y aparece en el listado de proyectos. Se generan las fases y la documentación inicial según la plantilla. | Alta | Funcional |
| GP-002 | Editar la información de un proyecto existente. | Proyecto existente creado. Usuario con rol 'Administrador' o 'PM' logueado. | 1. Navegar al detalle de un proyecto.\n2. Hacer clic en 'Editar'.\n3. Modificar el nombre y la fecha de fin.\n4. Hacer clic en 'Guardar'. | La información del proyecto se actualiza correctamente. | Media | Funcional |
| GP-003 | Eliminar un proyecto. | Proyecto existente sin fases completadas. Usuario con rol 'Administrador' o 'PM' logueado. | 1. Navegar al listado de proyectos.\n2. Seleccionar un proyecto.\n3. Hacer clic en 'Eliminar'.\n4. Confirmar la eliminación. | El proyecto es eliminado del sistema y ya no aparece en el listado. | Media | Funcional |
| GP-004 | Asignar un proyecto a un cliente. | Cliente existente. Usuario con rol 'Administrador' o 'PM' logueado. | 1. Crear o editar un proyecto.\n2. Seleccionar un cliente de la lista desplegable.\n3. Guardar los cambios. | El proyecto se asocia correctamente al cliente seleccionado. | Alta | Funcional |
| GP-005 | Avanzar una fase de proyecto con validaciones. | Proyecto en fase 'Inicio'. Usuario con rol 'PM' logueado. | 1. Navegar al detalle del proyecto.\n2. Intentar avanzar la fase de 'Inicio' a 'Planeación'.\n3. Verificar validaciones (ej. documentación completa). | La fase avanza solo si se cumplen las validaciones. Se muestra un mensaje de error si no se cumplen. | Alta | Funcional |

### 4.2. Módulo de Documentación del Proyecto

**Objetivo:** Validar la generación, edición y carga de documentos, así como el historial de cambios.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| DP-001 | Generar un documento a partir de una plantilla. | Proyecto y fase existentes. Usuario con rol 'PM' logueado. | 1. Navegar a la sección de documentación de una fase.\n2. Seleccionar una plantilla disponible.\n3. Hacer clic en 'Generar Documento'. | Se crea un nuevo documento basado en la plantilla y se asocia a la fase. | Alta | Funcional |
| DP-002 | Editar un documento generado y verificar el historial de cambios. | Documento generado existente. Usuario con rol 'PM' logueado. | 1. Abrir un documento para edición.\n2. Realizar cambios en el contenido.\n3. Guardar el documento.\n4. Acceder al historial de cambios del documento. | Los cambios se guardan correctamente y una nueva versión se registra en el historial. | Media | Funcional |
| DP-003 | Cargar un documento externo. | Proyecto y fase existentes. Usuario con rol 'PM' logueado. | 1. Navegar a la sección de documentación de una fase.\n2. Hacer clic en 'Cargar Documento'.\n3. Seleccionar un archivo (ej. PDF, DOCX) desde el sistema local.\n4. Asignar un nombre y tipo al documento.\n5. Hacer clic en 'Cargar'. | El documento externo se carga exitosamente y se visualiza en la lista de documentos de la fase. | Alta | Funcional |

### 4.3. Módulo de Indicadores Clave de Desempeño (KPIs)

**Objetivo:** Validar la visualización y actualización de los KPIs de tiempo, alcance y costo.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| KPI-001 | Visualizar el dashboard de KPIs para un proyecto. | Proyecto con datos de avance, tareas y costos registrados. Usuario con rol 'PM' o 'Cliente' logueado. | 1. Navegar al detalle de un proyecto.\n2. Acceder a la sección 'KPIs'. | El dashboard muestra gráficas comparativas para tiempo, alcance y costo con datos actualizados. | Alta | Funcional |
| KPI-002 | Verificar la actualización de KPIs tras un cambio en el cronograma. | Proyecto con cronograma definido. Usuario con rol 'PM' logueado. | 1. Modificar la fecha de fin de una tarea en el cronograma.\n2. Navegar al dashboard de KPIs. | El KPI de tiempo (avance vs cronograma) se actualiza reflejando el cambio. | Media | Funcional |

### 4.4. Módulo de Gestión de Riesgos

**Objetivo:** Validar el registro, clasificación, seguimiento y cierre de riesgos.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| GR-001 | Registrar un nuevo riesgo con clasificación de probabilidad e impacto. | Proyecto existente. Usuario con rol 'PM' logueado. | 1. Navegar a la sección 'Gestión de Riesgos'.\n2. Hacer clic en 'Nuevo Riesgo'.\n3. Rellenar descripción, seleccionar probabilidad e impacto.\n4. Guardar. | El riesgo se registra y aparece en la matriz de probabilidad e impacto. | Alta | Funcional |
| GR-002 | Actualizar el estado de un riesgo (ej. de 'Abierto' a 'Cerrado'). | Riesgo existente. Usuario con rol 'PM' logueado. | 1. Abrir el detalle de un riesgo.\n2. Cambiar el estado a 'Cerrado'.\n3. Guardar. | El estado del riesgo se actualiza correctamente y se refleja en el seguimiento. | Media | Funcional |

### 4.5. Módulo de Recursos

**Objetivo:** Validar la asignación y seguimiento de recursos, y el control de disponibilidad.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| REC-001 | Asignar un recurso humano a un proyecto. | Recurso humano disponible. Proyecto existente. Usuario con rol 'PM' logueado. | 1. Navegar a la sección 'Recursos'.\n2. Seleccionar un recurso.\n3. Asignar al proyecto. | El recurso se asigna al proyecto y su disponibilidad se actualiza. | Alta | Funcional |
| REC-002 | Verificar la carga laboral de un recurso. | Recurso asignado a múltiples proyectos. Usuario con rol 'PM' logueado. | 1. Navegar a la sección 'Recursos'.\n2. Seleccionar un recurso.\n3. Visualizar su carga laboral. | Se muestra la carga laboral consolidada del recurso a través de los proyectos asignados. | Media | Funcional |

### 4.6. Módulo Multi-proyecto y Multi-cliente

**Objetivo:** Validar la gestión paralela de proyectos y la segmentación por cliente.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| MPC-001 | Visualizar el tablero maestro de portafolio. | Múltiples proyectos de diferentes clientes existentes. Usuario con rol 'Administrador' logueado. | 1. Navegar al 'Dashboard Resumen' o 'Portafolio de Proyectos'. | El tablero muestra un resumen consolidado de todos los proyectos, agrupados o filtrables por cliente. | Alta | Funcional |
| MPC-002 | Filtrar proyectos por cliente. | Múltiples proyectos de diferentes clientes existentes. Usuario con rol 'PM' o 'Cliente' logueado. | 1. Navegar al listado de proyectos.\n2. Aplicar filtro por un cliente específico. | Solo se muestran los proyectos asociados al cliente seleccionado. | Alta | Funcional |

### 4.7. Módulo de Roles y Permisos

**Objetivo:** Validar que los accesos y funcionalidades se segmentan correctamente por rol y proyecto.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| RP-001 | Intentar crear un proyecto con rol 'Recurso'. | Usuario con rol 'Recurso' logueado. | 1. Intentar navegar a la sección 'Crear Proyecto'. | El usuario no tiene acceso a la funcionalidad de creación de proyectos. Se muestra un mensaje de error o la opción está deshabilitada. | Alta | Funcional |
| RP-002 | Acceder a un proyecto no asignado como 'Cliente'. | Usuario con rol 'Cliente' logueado. Proyecto no asignado a este cliente. | 1. Intentar acceder al detalle de un proyecto no asociado a su cliente. | El usuario no puede acceder al detalle del proyecto. Se muestra un mensaje de acceso denegado. | Alta | Funcional |

### 4.8. Módulo de Liquidación de Actividades y Costos

**Objetivo:** Validar el registro de costos, generación de reportes y notificaciones.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| LC-001 | Registrar un costo detallado por actividad y recurso. | Proyecto y fase existentes. Usuario con rol 'PM' logueado. | 1. Navegar a la sección 'Liquidación de Costos'.\n2. Hacer clic en 'Registrar Costo'.\n3. Rellenar campos (actividad, tipo de costo, monto, recurso, etc.).\n4. Guardar. | El costo se registra correctamente y se asocia a la actividad, fase y recurso. | Alta | Funcional |
| LC-002 | Generar un reporte de liquidación en PDF para un proyecto. | Costos registrados para un proyecto. Usuario con rol 'PM' o 'Administrador' logueado. | 1. Navegar a la sección 'Reportes de Costos'.\n2. Seleccionar un proyecto.\n3. Hacer clic en 'Generar PDF'. | Se descarga un archivo PDF con el reporte de liquidación detallado del proyecto. | Alta | Funcional |
| LC-003 | Verificar notificación por actividad no liquidada. | Actividad completada sin costo registrado. | 1. Simular la finalización de una actividad sin registrar su costo.\n2. Verificar las notificaciones del sistema. | Se recibe una notificación automática alertando sobre la actividad no liquidada. | Media | Funcional |

## 5. Casos de Prueba End-to-End (E2E)

**Objetivo:** Validar los flujos de negocio críticos que involucran múltiples módulos y roles.

| ID Caso de Prueba | Descripción del Caso de Prueba | Precondiciones | Pasos de Prueba | Resultado Esperado | Prioridad | Tipo de Prueba |
|---|---|---|---|---|---|---|
| E2E-001 | Flujo completo de creación y seguimiento de un proyecto. | Usuario 'Administrador' o 'PM' logueado. | 1. Crear un nuevo proyecto.\n2. Asignar un cliente y recursos.\n3. Generar documentación para la fase de 'Inicio'.\n4. Registrar un riesgo.\n5. Registrar costos para una actividad.\n6. Avanzar la fase a 'Planeación'.\n7. Verificar el dashboard de KPIs. | El proyecto se crea y se gestiona correctamente a través de todas las etapas. Los datos se reflejan en los módulos correspondientes (documentación, riesgos, costos, KPIs). | Crítica | E2E |
| E2E-002 | Flujo de acceso y visualización de un cliente. | Usuario 'Cliente' logueado. Proyecto asignado a este cliente. | 1. Iniciar sesión como cliente.\n2. Visualizar el listado de proyectos asignados.\n3. Acceder al detalle de un proyecto.\n4. Revisar la documentación y el dashboard de KPIs del proyecto. | El cliente puede acceder únicamente a sus proyectos asignados y visualizar la información relevante según su rol. | Alta | E2E |
| E2E-003 | Flujo de registro de usuario y primer login. | Ninguna. | 1. Acceder a la página de registro.\n2. Rellenar todos los campos obligatorios.\n3. Confirmar el registro (si aplica, vía email).\n4. Intentar iniciar sesión con las credenciales recién creadas. | El usuario se registra exitosamente y puede iniciar sesión. Se le asigna el rol por defecto (ej. 'Recurso' o 'Cliente') y se le redirige al dashboard inicial. | Crítica | E2E |

## 6. Herramientas de Pruebas

-   **Pruebas Funcionales:** Manuales y/o automatizadas con frameworks como Jest (para React/React Native) y Supertest (para Node.js/NestJS).
-   **Pruebas E2E:** Cypress o Playwright para la interfaz de usuario web y Appium para la interfaz de usuario móvil.
-   **Gestión de Casos de Prueba:** Jira, TestLink o un sistema similar para la gestión y seguimiento de los casos de prueba.

## 7. Criterios de Éxito

-   El 100% de los casos de prueba de prioridad 'Crítica' y 'Alta' deben pasar.
-   El 90% de los casos de prueba de prioridad 'Media' deben pasar.
-   No se deben encontrar defectos de bloqueo (blockers) o críticos (critical) en las pruebas E2E.
-   La aplicación debe cumplir con los requisitos de rendimiento y seguridad establecidos.

## 8. Roles y Responsabilidades

-   **Desarrolladores:** Implementación de pruebas unitarias e integración, corrección de defectos.
-   **QA Engineer (Manus AI):** Diseño de casos de prueba, ejecución de pruebas funcionales y E2E, reporte de defectos, seguimiento de la calidad.
-   **Product Owner:** Revisión y aprobación de las funcionalidades, validación de los criterios de aceptación.

## 9. Entorno de Pruebas

Se utilizará un entorno de pruebas dedicado que replique lo más fielmente posible el entorno de producción, incluyendo la configuración de la base de datos, el backend y el frontend. Se asegurará que los datos de prueba sean representativos y no contengan información sensible real.

## 10. Reporte de Defectos

Los defectos encontrados durante las pruebas serán registrados en un sistema de seguimiento de errores (ej. Jira), incluyendo la siguiente información:

-   ID del Defecto
-   Descripción detallada
-   Pasos para reproducir
-   Resultado esperado vs. Resultado actual
-   Severidad (Bloqueador, Crítico, Mayor, Menor, Trivial)
-   Prioridad (Alta, Media, Baja)
-   Capturas de pantalla o videos (si aplica)



