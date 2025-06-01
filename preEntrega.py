import tkinter as tk
from tkinter import ttk, messagebox

CATEGORIA_GENERICA = "Sin categoría"

listaProductos = []  # Lista de productos: [id, nombre, precio, categoría]
listaCategorias = [CATEGORIA_GENERICA]
secuenciaIDProducto = 1

def altaProducto():
    global secuenciaIDProducto
    nombreProducto = inputNombre.get()
    precioProducto = inputPrecio.get()
    categoriaProducto = categoriaSeleccionada.get()

    if nombreProducto and precioProducto and categoriaProducto:
        try:
            precioProducto = int(precioProducto)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        listaProductos.append([secuenciaIDProducto, nombreProducto, precioProducto, categoriaProducto])
        arbolProductosMostrados.insert('', 'end', iid=secuenciaIDProducto, values=(nombreProducto, f"${precioProducto}", categoriaProducto))
        secuenciaIDProducto += 1
        deseleccionDeInputs()
        filtrarProductos()
    else:
        messagebox.showwarning("Dejaste algún campos vacío", "Por favor completá todos los campos.")

def deseleccionDeInputs():
    inputNombre.delete(0, tk.END)
    inputPrecio.delete(0, tk.END)
    categoriaSeleccionada.set(CATEGORIA_GENERICA)
    arbolProductosMostrados.selection_remove(arbolProductosMostrados.selection())

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
    categoriaProductoEditado = categoriaSeleccionada.get()

    if not nombreProductoEditado or not categoriaProductoEditado:
        messagebox.showwarning("Campos vacíos", "Por favor completá todos los campos.")
        return

    for producto in listaProductos:
        if producto[0] == idProductoSeleccionado:
            producto[1] = nombreProductoEditado
            producto[2] = precioIngresado
            producto[3] = categoriaProductoEditado
            break
    
    arbolProductosMostrados.item(idProductoSeleccionado, values=(nombreProductoEditado, f"${precioIngresado}", categoriaProductoEditado))
    deseleccionDeInputs()
    filtrarProductos()

def bajaProducto():
    productoSeleccionado = arbolProductosMostrados.selection()
    if not productoSeleccionado:
        messagebox.showwarning("Selección", "Seleccioná un producto a eliminar.")
        return

    idProductoSeleccionado = int(productoSeleccionado[0])
    for producto in listaProductos:
        if producto[0] == idProductoSeleccionado:
            listaProductos.remove(producto)
            break

    arbolProductosMostrados.delete(idProductoSeleccionado)
    deseleccionDeInputs()
    filtrarProductos()

def altaCategoria():
    nuevaCategoria = inputCategoria.get()
    if nuevaCategoria and nuevaCategoria not in listaCategorias:
        listaCategorias.append(nuevaCategoria)
        comboCategoriasMostradas = categoriasMostradas['menu']
        comboCategoriasMostradas.delete(0, 'end')
        for categoria in listaCategorias:
            comboCategoriasMostradas.add_command(label=categoria, command=tk._setit(categoriaSeleccionada, categoria))
        inputCategoria.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "La categoría ya existe o está vacía.")

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
            categoriaSeleccionada.set(categoriaProducto)
            break

def filtrarProductos(event=None):
    palabraclaveingresadaBusquedaProducto = inputBusqueda.get().lower()

    for productoMostrado in arbolProductosMostrados.get_children():
        arbolProductosMostrados.delete(productoMostrado)

    for producto in listaProductos:
        if palabraclaveingresadaBusquedaProducto in producto[1].lower():
            arbolProductosMostrados.insert('', 'end', iid=producto[0], values=(producto[1], f"${producto[2]}", producto[3]))

# GUI
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Pre entrega")

# Inputs
tk.Label(ventanaPrincipal, text="Nombre").grid(row=0, column=0)
inputNombre = tk.Entry(ventanaPrincipal)
inputNombre.grid(row=0, column=1)

tk.Label(ventanaPrincipal, text="Precio").grid(row=1, column=0)
inputPrecio = tk.Entry(ventanaPrincipal)
inputPrecio.grid(row=1, column=1)

tk.Label(ventanaPrincipal, text="Categoría").grid(row=2, column=0)
categoriaSeleccionada = tk.StringVar(ventanaPrincipal)
categoriaSeleccionada.set(listaCategorias[0])
categoriasMostradas = tk.OptionMenu(ventanaPrincipal, categoriaSeleccionada, *listaCategorias)
categoriasMostradas.grid(row=2, column=1)

# Botones
tk.Button(ventanaPrincipal, text="Agregar", command=altaProducto).grid(row=0, column=2)
tk.Button(ventanaPrincipal, text="Editar", command=modificacionProducto).grid(row=1, column=2)
tk.Button(ventanaPrincipal, text="Eliminar", command=bajaProducto).grid(row=2, column=2)

# Búsqueda
tk.Label(ventanaPrincipal, text="Buscar producto por nombre").grid(row=3, column=0)
inputBusqueda = tk.Entry(ventanaPrincipal)
inputBusqueda.grid(row=3, column=1, columnspan=2, sticky='we')
inputBusqueda.bind("<KeyRelease>", filtrarProductos)

# Tabla Principal
arbolProductosMostrados = ttk.Treeview(ventanaPrincipal, columns=('Nombre', 'Precio', 'Categoría'), show='headings')
arbolProductosMostrados.heading('Nombre', text='Nombre')
arbolProductosMostrados.heading('Precio', text='Precio')
arbolProductosMostrados.heading('Categoría', text='Categoría')
arbolProductosMostrados.grid(row=4, column=0, columnspan=3, padx=5, pady=10)
arbolProductosMostrados.bind('<<TreeviewSelect>>', cargarProductoSeleccionado)

# Categorías
tk.Label(ventanaPrincipal, text="Nueva categoría").grid(row=5, column=0)
inputCategoria = tk.Entry(ventanaPrincipal)
inputCategoria.grid(row=5, column=1)
tk.Button(ventanaPrincipal, text="Agregar categoría", command=altaCategoria).grid(row=5, column=2)

ventanaPrincipal.mainloop()
