# 🧾 Inventario de Productos — Tkinter + SQLite

Este proyecto es una aplicación de escritorio desarrollada en **Python** utilizando **Tkinter** para la interfaz gráfica y **SQLite** para la persistencia de datos. Permite gestionar un inventario de productos con funcionalidades completas de CRUD tanto para productos como para sus categorías.

📍 Repositorio oficial: [https://github.com/sucuap/introduccionPython](https://github.com/sucuap/introduccionPython)

---

## 🚀 Funcionalidades

- Alta, modificación y baja de productos
- Gestión completa de categorías (crear, editar, eliminar)
- Filtro de productos por nombre
- Advertencia para productos con cantidad por debajo de un umbral definido por el usuario
- Interfaz clara y amigable
- Persistencia en disco con base de datos `inventario.db`

---

## 🗃️ Estructura de la base de datos

La base de datos `inventario.db` contiene dos tablas principales:

### 🛍️ Tabla `productos`

| Columna        | Tipo     | Descripción                                    |
|----------------|----------|------------------------------------------------|
| `id`           | INTEGER  | Clave primaria, autoincremental                |
| `nombre`       | TEXT     | Nombre del producto (no nulo)                  |
| `descripcion`  | TEXT     | Breve descripción del producto (opcional)      |
| `cantidad`     | INTEGER  | Stock disponible (no nulo)                     |
| `precio`       | REAL     | Precio del producto (no nulo)                  |
| `categoria_id` | INTEGER  | ID de categoría (clave foránea a `categorias`) |

### 🗂️ Tabla `categorias`

| Columna    | Tipo     | Descripción                                      |
|------------|----------|--------------------------------------------------|
| `id`       | INTEGER  | Clave primaria, autoincremental                  |
| `nombre`   | TEXT     | Nombre de la categoría (único, no nulo)          |

> 🔒 La categoría por defecto `"Sin categoría"` es permanente y no puede eliminarse.

---

## 💻 Requisitos

- Python 3.x
- Módulos estándar (`tkinter`, `sqlite3`)

No es necesario instalar paquetes adicionales.

---

## ▶️ Instrucciones de uso

1. Cloná el repositorio:
   ```bash
   git clone https://github.com/sucuap/introduccionPython
   cd introduccionPython
