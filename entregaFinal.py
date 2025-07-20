import sqlite3 as sql
import tkinter as tk
from tkinter import ttk, messagebox

CATEGORIA_GENERICA = "Sin categoría"
NOMBRE_BD = "inventario.db"

listaProductos = []  # Lista de productos: [id, nombre, descripcion, cantidad, precio, id_categoría]

listaCategorias = [] # Lista de categorías: [id, nombre]

categoriaInicial = {
    "id": 1,
    "nombre": [CATEGORIA_GENERICA]
}

listaCategorias.append(categoriaInicial)

conexionBD = sql.connect(NOMBRE_BD)
cursor = conexionBD.cursor()

def configuracionBD():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    ''')
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    ''')

    cursor.execute(f"INSERT OR IGNORE INTO categorias (id, nombre) VALUES (1, '{CATEGORIA_GENERICA}')")

    conexionBD.commit()

def obtenerNombreCategoria(idCategoriaProducto):
    return " ".join(arbolCategoriasMostradas.item(idCategoriaProducto)['values'])

def cargarProductosDesdeBD():
    cursor.execute("SELECT p.id, p.nombre, p.descripcion, p.cantidad, p.precio, c.id, c.nombre FROM productos AS p, categorias as C WHERE p.categoria_id = c.id")
    for idProducto, nombreProducto, descripcionProducto, cantidadProducto, precioProducto, idCategoria, nombreCategoria in cursor.fetchall():
        producto = [idProducto, nombreProducto, descripcionProducto, cantidadProducto, precioProducto, idCategoria]
        if producto not in listaProductos:
            listaProductos.append(producto)

        arbolProductosMostrados.insert('', 'end', iid=idProducto, values=(nombreProducto, descripcionProducto, cantidadProducto, f"${precioProducto}", nombreCategoria))

def cargarCategoriasDesdeBD():
    cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    for idCategoria, nombreCategoria in cursor.fetchall():
        itemCategoria = {
            "id": idCategoria,
            "nombre": nombreCategoria
        }
        if itemCategoria not in listaCategorias:
            listaCategorias.append(itemCategoria)

        arbolCategoriasMostradas.insert('', 'end', iid=idCategoria, values=(nombreCategoria))

def altaProducto():
    nombreProducto = inputNombre.get()
    descripcionProducto = inputDescripcion.get()
    cantidadProducto = inputCantidad.get()
    precioProducto = inputPrecio.get()
    categoriaProductoCargado = arbolCategoriasMostradas.selection()

    if nombreProducto and descripcionProducto and cantidadProducto and precioProducto and categoriaProductoCargado:
        try:
            cantidadProducto = int(cantidadProducto)
            precioProducto = float(precioProducto)
        except ValueError:
            messagebox.showerror("Error", "La cantidad y eel precio deben ser números.")
            return

        idCategoriaSeleccionada = int(categoriaProductoCargado[0])
        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria_id) VALUES (?, ?, ?, ?, ?)",
               (nombreProducto, descripcionProducto, cantidadProducto, precioProducto, idCategoriaSeleccionada))
        conexionBD.commit()

        listaProductos.append([cursor.lastrowid, nombreProducto, descripcionProducto, cantidadProducto, precioProducto, idCategoriaSeleccionada])
        arbolProductosMostrados.insert('', 'end', iid=cursor.lastrowid, values=(nombreProducto, descripcionProducto, cantidadProducto, f"${precioProducto}", obtenerNombreCategoria(idCategoriaSeleccionada)))
        deseleccionDeInputs()
    else:
        messagebox.showwarning("Dejaste algún campos vacío", "Por favor completá todos los campos.")

def altaCategoria():
    nombreNuevaCategoria = inputCategoria.get().strip()
    if not nombreNuevaCategoria:
        messagebox.showwarning("Advertencia", "Ingresá un nombre de categoría.")
        return
    try:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombreNuevaCategoria, ))
        conexionBD.commit()

        listaCategorias.append({"id": cursor.lastrowid, "nombre": nombreNuevaCategoria})
        arbolCategoriasMostradas.insert('', 'end', iid=cursor.lastrowid, values=(nombreNuevaCategoria))
        inputCategoria.delete(0, tk.END)
    except sql.IntegrityError:
        messagebox.showerror("Error", "La categoría ya existe.")

def deseleccionDeInputs():
    inputNombre.delete(0, tk.END)
    inputDescripcion.delete(0, tk.END)
    inputCantidad.delete(0, tk.END)
    inputPrecio.delete(0, tk.END)
    inputCategoria.delete(0, tk.END)
    arbolProductosMostrados.selection_remove(arbolProductosMostrados.selection())
    arbolCategoriasMostradas.selection_remove(arbolCategoriasMostradas.selection())
    filtrarProductos()

def modificacionProducto():
    productoSeleccionado = arbolProductosMostrados.selection()
    if not productoSeleccionado:
        messagebox.showwarning("Selección", "Seleccioná un producto a editar.")
        return

    try:
        cantidadIngresada = int(inputCantidad.get())
        precioIngresado = float(inputPrecio.get())
    except ValueError:
        messagebox.showerror("Error", "La cantidad y el precio debe ser números.")
        return

    idProductoSeleccionado = int(productoSeleccionado[0])
    nombreProductoEditado = inputNombre.get()
    descripcionProductoEditado = inputDescripcion.get()
    categoriaProductoEditado = arbolCategoriasMostradas.selection()

    if not nombreProductoEditado or not categoriaProductoEditado:
        messagebox.showwarning("Campos vacíos", "Por favor completá todos los campos.")
        return

    for productoIterado in listaProductos:
        if productoIterado[0] == idProductoSeleccionado:
            productoIterado[1] = nombreProductoEditado
            productoIterado[2] = descripcionProductoEditado
            productoIterado[3] = cantidadIngresada
            productoIterado[4] = precioIngresado
            idCategoriaSeleccionada = int(categoriaProductoEditado[0])
            productoIterado[5] = idCategoriaSeleccionada
            arbolProductosMostrados.item(idProductoSeleccionado, values=(nombreProductoEditado, descripcionProductoEditado, cantidadIngresada, f"${precioIngresado}", obtenerNombreCategoria(idCategoriaSeleccionada)))

            cursor.execute('UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria_id=? WHERE id=?',
               (nombreProductoEditado, descripcionProductoEditado, cantidadIngresada, precioIngresado, idCategoriaSeleccionada, idProductoSeleccionado))
            conexionBD.commit()

            deseleccionDeInputs()
            break

def modificacionCategoria():
    categoriaSeleccionada = arbolCategoriasMostradas.selection()
    if not categoriaSeleccionada:
        messagebox.showwarning("Advertencia", "Seleccioná una categoría a editar.")
        return
    idCategoriaSeleccionada = int(categoriaSeleccionada[0])
    if idCategoriaSeleccionada == 1:
        messagebox.showwarning("Advertencia", "No se puede editar la categoría genérica")
        return
    nombreCategoriaModificado = inputCategoria.get().strip()
    if not nombreCategoriaModificado:
        messagebox.showwarning("Advertencia", "Ingresá un nombre.")
        return

    for categoriaIterada in listaCategorias:
        if categoriaIterada['id'] == idCategoriaSeleccionada:
            categoriaIterada['nombre'] = nombreCategoriaModificado
            break

    arbolCategoriasMostradas.item(idCategoriaSeleccionada, values=(nombreCategoriaModificado))

    try:
        cursor.execute("UPDATE categorias SET nombre = ? WHERE id = ?", (nombreCategoriaModificado, idCategoriaSeleccionada))
        conexionBD.commit()

        inputCategoria.delete(0, tk.END)
    except sql.IntegrityError:
        messagebox.showerror("Error", "Ya existe una categoría con ese nombre.")

    limpiezaArbolProductosMostrados() 
    cargarProductosDesdeBD()

def bajaProducto():
    productoSeleccionado = arbolProductosMostrados.selection()
    if not productoSeleccionado:
        messagebox.showwarning("Selección", "Seleccioná un producto a eliminar.")
        return

    idProductoSeleccionado = int(productoSeleccionado[0])
    for productoIterado in listaProductos:
        if productoIterado[0] == idProductoSeleccionado:
            listaProductos.remove(productoIterado)

            cursor.execute('DELETE FROM productos WHERE id=?', (idProductoSeleccionado,))
            conexionBD.commit()

            break

    arbolProductosMostrados.delete(idProductoSeleccionado)
    deseleccionDeInputs()

def bajaCategoria():
    categoriaSeleccionada = arbolCategoriasMostradas.selection()
    if not categoriaSeleccionada:
        messagebox.showwarning("Advertencia", "Seleccioná una categoría.")
        return

    idCategoriaSeleccionada = int(categoriaSeleccionada[0])
    if idCategoriaSeleccionada == 1:
        messagebox.showwarning("Advertencia", "No se puede eliminar la categoría genérica")
        return
    # Verificar si está en uso
    cursor.execute("SELECT COUNT(*) FROM productos WHERE categoria_id = ?", (idCategoriaSeleccionada,))
    if cursor.fetchone()[0] > 0:
        messagebox.showerror("Error", "No se puede eliminar una categoría en uso.")
        return

    for categoriaIterada in listaCategorias:
        if categoriaIterada['id'] == idCategoriaSeleccionada:
            listaCategorias.remove(categoriaIterada)

            cursor.execute("DELETE FROM categorias WHERE id = ?", (idCategoriaSeleccionada,))
            conexionBD.commit()

            break

    arbolCategoriasMostradas.delete(idCategoriaSeleccionada)
    inputCategoria.delete(0, tk.END)

def cargarProductoSeleccionado(event):
    productoSeleccionado = arbolProductosMostrados.selection()
    if not productoSeleccionado:
        return
    idProductoSeleccionado = int(productoSeleccionado[0])
    for [idProducto, nombreProducto, descripcionProducto, cantidadProducto, precioProducto, idCategoriaProducto] in listaProductos:
        if idProducto == idProductoSeleccionado:
            inputNombre.delete(0, tk.END)
            inputDescripcion.delete(0, tk.END)
            inputCantidad.delete(0, tk.END)
            inputPrecio.delete(0, tk.END)
            inputNombre.insert(0, nombreProducto)
            inputDescripcion.insert(0, descripcionProducto)
            inputCantidad.insert(0, str(cantidadProducto))
            inputPrecio.insert(0, str(precioProducto))
            if arbolCategoriasMostradas.exists(idCategoriaProducto):
                arbolCategoriasMostradas.selection_set(idCategoriaProducto)
                arbolCategoriasMostradas.see(idCategoriaProducto)  # Hace scroll si está fuera de vista
            break

def cargarCategoriaSeleccionada(event):
    categoriaSeleccionada = arbolCategoriasMostradas.selection()
    if not categoriaSeleccionada:
        return
    inputCategoria.delete(0, tk.END)
    inputCategoria.insert(0, obtenerNombreCategoria(int(categoriaSeleccionada[0])))

def limpiezaArbolProductosMostrados():
    for productoMostrado in arbolProductosMostrados.get_children():
        arbolProductosMostrados.delete(productoMostrado)

def filtrarProductos(event=None):
    palabraclaveingresadaBusquedaProducto = inputBusqueda.get().lower()
    limpiezaArbolProductosMostrados() 

    for [idProducto, nombreProducto, descripcionProducto, cantidadProducto, precioProducto, idCategoriaProducto] in listaProductos:
        if palabraclaveingresadaBusquedaProducto in nombreProducto.lower():
            arbolProductosMostrados.insert('', 'end', iid=idProducto, values=(nombreProducto, descripcionProducto, cantidadProducto, f"${precioProducto}", obtenerNombreCategoria(idCategoriaProducto)))

def verificarStockBajo():
    try:
        limite = int(inputLimiteReporte.get())
    except ValueError:
        messagebox.showerror("Error", "El límite debe ser un número entero.")
        return

    cursor.execute('''
        SELECT nombre, cantidad FROM productos WHERE cantidad <= ?
    ''', (limite,))
    productos = cursor.fetchall()

    if not productos:
        messagebox.showinfo("Stock suficiente", "No hay productos con stock bajo.")
    else:
        mensaje = "Productos con bajo stock:\n"
        mensaje += "\n".join(f"- {nombre}: {cant} unidades" for nombre, cant in productos)
        messagebox.showwarning("Atención", mensaje)

def cerrarBD():
    conexionBD.close()
    ventanaPrincipal.destroy()

# BD
configuracionBD()

# GUI
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Entrega final")

# Inputs
tk.Label(ventanaPrincipal, text="Nombre").grid(row=0, column=0)
inputNombre = tk.Entry(ventanaPrincipal)
inputNombre.grid(row=0, column=1)

tk.Label(ventanaPrincipal, text="Descripción").grid(row=1, column=0)
inputDescripcion = tk.Entry(ventanaPrincipal)
inputDescripcion.grid(row=1, column=1)

tk.Label(ventanaPrincipal, text="Cantidad").grid(row=2, column=0)
inputCantidad = tk.Entry(ventanaPrincipal)
inputCantidad.grid(row=2, column=1)

tk.Label(ventanaPrincipal, text="Precio").grid(row=3, column=0)
inputPrecio = tk.Entry(ventanaPrincipal)
inputPrecio.grid(row=3, column=1)

# Botones
tk.Button(ventanaPrincipal, text="Agregar producto", command=altaProducto).grid(row=0, column=2)
tk.Button(ventanaPrincipal, text="Editar producto", command=modificacionProducto).grid(row=1, column=2)
tk.Button(ventanaPrincipal, text="Eliminar producto", command=bajaProducto).grid(row=2, column=2)

# Sección categoría
tk.Label(ventanaPrincipal, text="Categoría").grid(row=5, column=0)
inputCategoria = tk.Entry(ventanaPrincipal)
inputCategoria.grid(row=5, column=1)

tk.Button(ventanaPrincipal, text="Agregar categoría", command=altaCategoria).grid(row=4, column=2)
tk.Button(ventanaPrincipal, text="Editar categoría", command=modificacionCategoria).grid(row=5, column=2)
tk.Button(ventanaPrincipal, text="Eliminar categoría", command=bajaCategoria).grid(row=6, column=2)

# Búsqueda
tk.Label(ventanaPrincipal, text="Buscar producto por nombre").grid(row=7, column=0)
inputBusqueda = tk.Entry(ventanaPrincipal)
inputBusqueda.grid(row=7, column=1, columnspan=2, sticky='we')
inputBusqueda.bind("<KeyRelease>", filtrarProductos)

frameProductos = tk.Frame(ventanaPrincipal)
frameProductos.grid(row=8, column=0, columnspan=3, padx=5, pady=10, sticky='nsew')

scrollbarProductos = ttk.Scrollbar(frameProductos, orient="vertical")
scrollbarProductos.grid(row=0, column=1, sticky='ns')

# Tabla Principal
arbolProductosMostrados = ttk.Treeview(frameProductos, columns=("Nombre", "Descripción", "Cantidad", "Precio", "Categoría"), show='headings', yscrollcommand=scrollbarProductos.set)
arbolProductosMostrados.heading("Nombre", text="Nombre")
arbolProductosMostrados.heading("Descripción", text="Descripción")
arbolProductosMostrados.heading("Cantidad", text="Cantidad")
arbolProductosMostrados.heading("Precio", text="Precio")
arbolProductosMostrados.heading("Categoría", text="Categoría")
arbolProductosMostrados.bind('<<TreeviewSelect>>', cargarProductoSeleccionado)
arbolProductosMostrados.grid(row=0, column=0, sticky='nsew')
scrollbarProductos.config(command=arbolProductosMostrados.yview)
frameProductos.grid_rowconfigure(0, weight=1)
frameProductos.grid_columnconfigure(0, weight=1)

tk.Label(ventanaPrincipal, text="Categorías").grid(row=9, column=0, pady=(20, 0))

frameCategorias = tk.Frame(ventanaPrincipal)
frameCategorias.grid(row=10, column=0, columnspan=3, padx=5, pady=10, sticky='nsew')

scrollbarCategorias = ttk.Scrollbar(frameCategorias, orient="vertical")
scrollbarCategorias.grid(row=0, column=1, sticky='ns')

# Tabla de Categorías
arbolCategoriasMostradas = ttk.Treeview(frameCategorias, columns=("Nombre"), show='headings', yscrollcommand=scrollbarCategorias.set)
arbolCategoriasMostradas.heading("Nombre", text="Nombre")
arbolCategoriasMostradas.grid(row=0, column=0, sticky='nsew')
arbolCategoriasMostradas.bind("<<TreeviewSelect>>", cargarCategoriaSeleccionada)
scrollbarCategorias.config(command=arbolCategoriasMostradas.yview)

# Generador de reportes
tk.Label(ventanaPrincipal, text="Generar reporte de ").grid(row=11, column=0)
inputLimiteReporte = tk.Entry(ventanaPrincipal)
inputLimiteReporte.grid(row=10, column=1)
tk.Button(ventanaPrincipal, text="Ver productos con bajo stock", command=verificarStockBajo).grid(row=10, column=2)

cargarProductosDesdeBD()
cargarCategoriasDesdeBD()

ventanaPrincipal.protocol("WM_DELETE_WINDOW", cerrarBD)
ventanaPrincipal.mainloop()
