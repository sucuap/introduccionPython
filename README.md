# 🧾 Inventario de Productos

Este proyecto es una aplicación de escritorio desarrollada en **Python** usando **Tkinter** para la interfaz gráfica y **SQLite** para la persistencia de datos. Permite gestionar un inventario de productos con funcionalidades completas de CRUD tanto para productos como para categorías.

---

## 🚀 Características

- Alta, modificación y baja de productos
- Gestión de categorías con opción a crear, editar y eliminar (excepto la genérica "Sin categoría")
- Filtro de productos por nombre
- Aviso visual para productos con baja cantidad
- Interfaz amigable y simple
- Persistencia con base de datos `inventario.db`

---

## 🗃️ Estructura de la base de datos

La base de datos `inventario.db` contiene las siguientes tablas:

### 🛍️ productos

| Columna    | Tipo     | Descripción                           |
|------------|----------|---------------------------------------|
| `id`       | INTEGER  | Clave primaria, autoincremental       |
| `nombre`   | TEXT     | Nombre del producto (no nulo)         |
| `descripcion` | TEXT | Descripción opcional                  |
| `cantidad` | INTEGER  | Cantidad disponible (no nulo)         |
| `precio`   | REAL     | Precio del producto (no nulo)         |
| `categoria_id` | INTEGER | Clave foránea a la tabla `categorias` |

### 🗂️ categorias

| Columna    | Tipo     | Descripción                         |
|------------|----------|-------------------------------------|
| `id`       | INTEGER  | Clave primaria, autoincremental     |
| `nombre`   | TEXT     | Nombre de la categoría (único, no nulo) |

> 🔒 La categoría `"Sin categoría"` se crea por defecto y no puede eliminarse.

---

## 💻 Requisitos

- Python 3.x
- Paquetes estándar (`tkinter`, `sqlite3`)

No se requiere instalación de librerías externas.

---

## 🧰 Cómo usar

1. Cloná este repositorio:
   ```bash
   git clone https://github.com/tuusuario/inventario-productos.git
   cd inventario-productos
