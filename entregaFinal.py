import sqlite3 as sql
import tkinter as tk
from tkinter import ttk, messagebox

CATEGORIA_GENERICA = "Sin categoría"
NOMBRE_BD = "entregaFinal.db"

listaProductos = []  # Lista de productos: [id, nombre, precio, categoría]

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
        precio INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    ''')

    cursor.execute(f"INSERT OR IGNORE INTO categorias (id, nombre) VALUES (1, '{CATEGORIA_GENERICA}')")

    conexionBD.commit()

def cargarProductosDesdeBD():
    cursor.execute("SELECT p.id, p.nombre, p.precio, c.nombre FROM productos AS p, categorias as C WHERE p.categoria_id = c.id")
    for idProducto, nombreProducto, precioProducto, nombreCategoria in cursor.fetchall():
        producto = [idProducto, nombreProducto, precioProducto, nombreCategoria]
        if producto not in listaProductos:
            listaProductos.append(producto)

        arbolProductosMostrados.insert('', 'end', iid=idProducto, values=(f"{nombreProducto}", f"${precioProducto}", f"{nombreCategoria}"))

def cargarCategoriasDesdeBD():
    cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    for idCategoria, nombreCategoria in cursor.fetchall():
        itemCategoria = {
            "id": idCategoria,
            "nombre": nombreCategoria
        }
        if itemCategoria not in listaCategorias:
            listaCategorias.append(itemCategoria)

        arbolCategoriasMostradas.insert('', 'end', iid=idCategoria, values=(f"{nombreCategoria}"))

def altaProducto():
    nombreProducto = inputNombre.get()
    precioProducto = inputPrecio.get()
    categoriaProductoCargado = arbolCategoriasMostradas.selection()

    if nombreProducto and precioProducto and categoriaProductoCargado:
        try:
            precioProducto = int(precioProducto)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        idCategoriaSeleccionada = int(categoriaProductoCargado[0])
        cursor.execute("INSERT INTO productos (nombre, precio, categoria_id) VALUES (?, ?, ?)",
               (nombreProducto, precioProducto, idCategoriaSeleccionada))
        conexionBD.commit()


        nombreCategoriaProductoAgregado = " ".join(arbolCategoriasMostradas.item(idCategoriaSeleccionada)['values'])
        listaProductos.append([cursor.lastrowid, nombreProducto, precioProducto, nombreCategoriaProductoAgregado])
        arbolProductosMostrados.insert('', 'end', iid=cursor.lastrowid, values=(f"{nombreProducto}", f"${precioProducto}", f"{nombreCategoriaProductoAgregado}"))
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
        arbolCategoriasMostradas.insert('', 'end', iid=cursor.lastrowid, values=(f"{nombreNuevaCategoria}"))
        inputCategoria.delete(0, tk.END)
    except sql.IntegrityError:
        messagebox.showerror("Error", "La categoría ya existe.")

def deseleccionDeInputs():
    inputNombre.delete(0, tk.END)
    inputPrecio.delete(0, tk.END)
    arbolProductosMostrados.selection_remove(arbolProductosMostrados.selection())
    arbolCategoriasMostradas.selection_remove(arbolCategoriasMostradas.selection())
    filtrarProductos()

def modificacionProducto():
    productoSeleccionado = arbolProductosMostrados.selection()
    if not productoSeleccionado:
        messagebox.showwarning("Selección", "Seleccioná un producto a editar.")
        return

    try:
        precioIngresado = int(inputPrecio.get())
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número.")
        return

    idProductoSeleccionado = int(productoSeleccionado[0])
    nombreProductoEditado = inputNombre.get()
    categoriaProductoEditado = arbolCategoriasMostradas.selection()

    if not nombreProductoEditado or not categoriaProductoEditado:
        messagebox.showwarning("Campos vacíos", "Por favor completá todos los campos.")
        return

    for productoIterado in listaProductos:
        if productoIterado[0] == idProductoSeleccionado:
            productoIterado[1] = nombreProductoEditado
            productoIterado[2] = precioIngresado
            idCategoriaSeleccionada = int(categoriaProductoEditado[0])
            nombreCategoriaProductoEditado = " ".join(arbolCategoriasMostradas.item(idCategoriaSeleccionada)['values'])
            productoIterado[3] = nombreCategoriaProductoEditado
            arbolProductosMostrados.item(idProductoSeleccionado, values=(f"{nombreProductoEditado}", f"${precioIngresado}", nombreCategoriaProductoEditado))

            cursor.execute('UPDATE productos SET nombre=?, precio=?, categoria_id=? WHERE id=?',
               (nombreProductoEditado, precioIngresado, idCategoriaSeleccionada, idProductoSeleccionado))
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

    arbolCategoriasMostradas.item(idCategoriaSeleccionada, values=(f"{nombreCategoriaModificado}"))

    try:
        cursor.execute("UPDATE categorias SET nombre = ? WHERE id = ?", (nombreCategoriaModificado, idCategoriaSeleccionada))
        conexionBD.commit()

        inputCategoria.delete(0, tk.END)
    except sql.IntegrityError:
        messagebox.showerror("Error", "Ya existe una categoría con ese nombre.")

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
    for [idProducto, nombreProducto, precioProducto, categoriaProducto] in listaProductos:
        if idProducto == idProductoSeleccionado:
            inputNombre.delete(0, tk.END)
            inputPrecio.delete(0, tk.END)
            inputNombre.insert(0, nombreProducto)
            inputPrecio.insert(0, str(precioProducto))
            if arbolCategoriasMostradas.exists(categoriaProducto):
                arbolCategoriasMostradas.selection_set(categoriaProducto)
                arbolCategoriasMostradas.see(categoriaProducto)  # Hace scroll si está fuera de vista
            break

def cargarCategoriaSeleccionada(event):
    categoriaSeleccionada = arbolCategoriasMostradas.selection()
    if not categoriaSeleccionada:
        return
    idCategoriaSeleccionada = int(categoriaSeleccionada[0])
    nombreCategoria = " ".join(arbolCategoriasMostradas.item(idCategoriaSeleccionada)['values'])
    inputCategoria.delete(0, tk.END)
    inputCategoria.insert(0, nombreCategoria)

def filtrarProductos(event=None):
    palabraclaveingresadaBusquedaProducto = inputBusqueda.get().lower()

    for productoMostrado in arbolProductosMostrados.get_children():
        arbolProductosMostrados.delete(productoMostrado)

    for producto in listaProductos:
        if palabraclaveingresadaBusquedaProducto in producto[1].lower():
            arbolProductosMostrados.insert('', 'end', iid=producto[0], values=(f"{producto[1]}", f"${producto[2]}", f"{producto[3]}"))

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

tk.Label(ventanaPrincipal, text="Precio").grid(row=1, column=0)
inputPrecio = tk.Entry(ventanaPrincipal)
inputPrecio.grid(row=1, column=1)

# Botones
tk.Button(ventanaPrincipal, text="Agregar producto", command=altaProducto).grid(row=0, column=2)
tk.Button(ventanaPrincipal, text="Editar producto", command=modificacionProducto).grid(row=1, column=2)
tk.Button(ventanaPrincipal, text="Eliminar producto", command=bajaProducto).grid(row=2, column=2)

# Búsqueda
tk.Label(ventanaPrincipal, text="Buscar producto por nombre").grid(row=3, column=0)
inputBusqueda = tk.Entry(ventanaPrincipal)
inputBusqueda.grid(row=3, column=1, columnspan=2, sticky='we')
inputBusqueda.bind("<KeyRelease>", filtrarProductos)

# Tabla Principal
arbolProductosMostrados = ttk.Treeview(ventanaPrincipal, columns=("Nombre", "Precio", "Categoría"), show='headings', height=5)
arbolProductosMostrados.heading("Nombre", text="Nombre")
arbolProductosMostrados.heading("Precio", text="Precio")
arbolProductosMostrados.heading("Categoría", text="Categoría")
arbolProductosMostrados.grid(row=4, column=0, columnspan=3, padx=5, pady=10)
arbolProductosMostrados.bind('<<TreeviewSelect>>', cargarProductoSeleccionado)

tk.Label(ventanaPrincipal, text="Categorías").grid(row=5, column=0, pady=(20, 0))

# Tabla de Categorías
arbolCategoriasMostradas = ttk.Treeview(ventanaPrincipal, columns=("Nombre"), show='headings', height=5)
arbolCategoriasMostradas.heading("Nombre", text="Nombre")
arbolCategoriasMostradas.grid(row=6, column=0, columnspan=3, pady=5)
arbolCategoriasMostradas.bind("<<TreeviewSelect>>", cargarCategoriaSeleccionada)

tk.Label(ventanaPrincipal, text="Nombre categoría").grid(row=7, column=0)
inputCategoria = tk.Entry(ventanaPrincipal)
inputCategoria.grid(row=7, column=1)

tk.Button(ventanaPrincipal, text="Agregar categoría", command=altaCategoria).grid(row=7, column=2)
tk.Button(ventanaPrincipal, text="Editar categoría", command=modificacionCategoria).grid(row=8, column=1)
tk.Button(ventanaPrincipal, text="Eliminar categoría", command=bajaCategoria).grid(row=8, column=2)

cargarProductosDesdeBD()
cargarCategoriasDesdeBD()

ventanaPrincipal.protocol("WM_DELETE_WINDOW", cerrarBD)
ventanaPrincipal.mainloop()
