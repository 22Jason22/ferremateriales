# Documentación del Administrador de Django Personalizado

## 1. Introducción

El panel de administración de Django del proyecto Nexus ha sido modificado para ofrecer una experiencia de usuario más moderna e intuitiva. El cambio principal consiste en reemplazar la barra lateral de navegación (`sidebar`) por defecto con una barra de navegación superior (`navbar`) que organiza las aplicaciones y modelos en menús desplegables.

Este documento detalla los archivos clave involucrados en esta personalización, explicando el propósito de cada uno y cómo contribuyen al nuevo diseño.

## 2. Archivos Involucrados

La personalización se logra sobrescribiendo las plantillas por defecto del admin de Django y añadiendo archivos CSS y JavaScript personalizados. La información ha sido extraída de la documentación general del proyecto.

### 2.1. Archivos de Plantillas (Templates)

Estos archivos se encuentran en el directorio `templates/admin/` y sobrescriben las plantillas originales de Django para alterar la estructura y cargar recursos personalizados.

#### `templates/admin/base_site.html`
- **Propósito**: Es la plantilla base principal del sitio de administración. Se ha modificado para:
  - Cargar los archivos CSS y JavaScript personalizados (`admin_navbar.css` y `custom_admin.js`).
  - Reestructurar el HTML para incluir la nueva barra de navegación superior.
  - Eliminar o reemplazar los bloques de la cabecera y navegación originales.

#### `templates/admin/nav_sidebar.html`
- **Propósito**: En una configuración estándar de Django, esta plantilla renderiza la barra lateral de navegación.
- **Modificación**: Ha sido modificada para que no muestre ningún contenido, ocultando efectivamente la barra lateral. Toda la navegación se traslada a la barra superior.

#### `templates/admin/app_list.html`
- **Propósito**: Esta plantilla es responsable de renderizar la lista de aplicaciones y sus modelos.
- **Modificación**: Se ha personalizado para integrarse con la nueva barra de navegación. Su lógica se utiliza para poblar los menús desplegables de la `navbar`, agrupando los modelos bajo su respectiva aplicación.

#### `templates/admin/index.html`
- **Propósito**: Es la página principal (dashboard) del panel de administración.
- **Modificación**: Integra el nuevo diseño de navegación y personaliza la visualización de las aplicaciones y modelos, asegurando que el contenido se muestre correctamente bajo la nueva `navbar`.

### 2.2. Archivos Estáticos (CSS y JavaScript)

Estos archivos se encuentran en el directorio `static/admin/` y controlan la apariencia y el comportamiento de la nueva interfaz.

#### `static/admin/css/admin_navbar.css`
- **Propósito**: Define todos los estilos visuales para la barra de navegación personalizada.
- **Detalles**:
  - Estilos para la `navbar` (color, altura, posicionamiento).
  - Diseño de los menús desplegables y los elementos de la lista.
  - Estilos para los íconos y el menú de usuario.
  - Clases para estados `hover` y `active` de los menús.
  - Media queries para asegurar que la navegación sea responsiva en diferentes tamaños de pantalla.

#### `static/admin/js/custom_admin.js`
- **Propósito**: Controla toda la lógica interactiva y el comportamiento dinámico de la nueva barra de navegación.
- **Funcionalidades clave**:
  - **Manejo de menús desplegables**: Contiene el código JavaScript para mostrar y ocultar los menús de aplicaciones al hacer clic.
  - **Gestión de acordeones**: Si los menús tienen sub-listas, este script maneja su expansión y contracción.
  - **Acciones de usuario**: Controla la interactividad del menú de usuario (por ejemplo, el desplegable para "Ver perfil" o "Cerrar sesión").
  - **Estado activo**: Puede incluir lógica para resaltar el menú de la aplicación que se está viendo actualmente.

## 3. Resumen del Funcionamiento

1.  Al acceder al admin, Django carga `templates/admin/base_site.html`.
2.  Esta plantilla personalizada incluye la estructura de la `navbar` y enlaza a `admin_navbar.css` y `custom_admin.js`.
3.  La plantilla `nav_sidebar.html` se renderiza vacía, eliminando la barra lateral.
4.  La lógica de `app_list.html` se utiliza dentro de la `navbar` para generar los menús desplegables con las aplicaciones y modelos.
5.  El archivo `admin_navbar.css` aplica los estilos para que la `navbar` se vea correctamente.
6.  El archivo `custom_admin.js` se ejecuta en el navegador para hacer que los menús desplegables y otros componentes interactivos funcionen.
