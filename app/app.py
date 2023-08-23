import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog
import sqlite3
from tkinter import messagebox

def crear_proyecto():
    nombre_proyecto = tk.simpledialog.askstring("Crear Proyecto", "Ingrese el nombre del proyecto:")
    if nombre_proyecto:
        conexion = sqlite3.connect("materiales.db")
        cursor = conexion.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nombre_proyecto} \
                       (id INTEGER PRIMARY KEY, nombre TEXT, cantidad INTEGER, descripcion TEXT)")
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Proyecto Creado", f"Se ha creado el proyecto '{nombre_proyecto}'")

def limpiar_campos():
    nombre_var.set("")
    cantidad_var.set("")
    descripcion_var.set("")

def agregar_material():
    nombre = nombre_var.get()
    cantidad = cantidad_var.get()
    descripcion = descripcion_var.get()

    if nombre and cantidad and descripcion:
        nombre_proyecto = proyecto_var.get()

        conexion = sqlite3.connect("materiales.db")
        cursor = conexion.cursor()
        cursor.execute(f"INSERT INTO {nombre_proyecto} (nombre, cantidad, descripcion) VALUES (?, ?, ?)",
                       (nombre, cantidad, descripcion))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Material agregado correctamente")
        limpiar_campos()
        actualizar_tabla_materiales()

    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def actualizar_tabla_materiales():
    nombre_proyecto = proyecto_var.get()

    conexion = sqlite3.connect("materiales.db")
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM {nombre_proyecto}")
    materiales = cursor.fetchall()
    conexion.close()

    tabla_materiales.delete(*tabla_materiales.get_children())

    for material in materiales:
        tabla_materiales.insert("", "end", values=material[1:])

def obtener_nombres_proyectos():
    conexion = sqlite3.connect("materiales.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    nombres = [nombre[0] for nombre in cursor.fetchall()]
    conexion.close()
    return nombres

ventana_principal = tk.Tk()
ventana_principal.title("Registro de Materiales")

nombre_var = tk.StringVar()
cantidad_var = tk.StringVar()
descripcion_var = tk.StringVar()
proyecto_var = tk.StringVar()

frame_ingresar = tk.Frame(ventana_principal)
frame_ingresar.pack(side=tk.LEFT, padx=20, pady=20)

tk.Label(frame_ingresar, text="Nombre del Material:").grid(row=0, column=0)
tk.Entry(frame_ingresar, textvariable=nombre_var).grid(row=0, column=1)

tk.Label(frame_ingresar, text="Cantidad:").grid(row=1, column=0)
tk.Entry(frame_ingresar, textvariable=cantidad_var).grid(row=1, column=1)

tk.Label(frame_ingresar, text="Descripción:").grid(row=2, column=0)
tk.Entry(frame_ingresar, textvariable=descripcion_var).grid(row=2, column=1)

frame_proyecto = tk.Frame(ventana_principal)
frame_proyecto.pack(side=tk.TOP, padx=20, pady=10)

tk.Label(frame_proyecto, text="Proyecto:").grid(row=0, column=0)
proyecto_combobox = ttk.Combobox(frame_proyecto, textvariable=proyecto_var)
proyecto_combobox.grid(row=0, column=1)
proyecto_combobox['values'] = obtener_nombres_proyectos()


tk.Button(frame_proyecto, text="Crear Proyecto", command=crear_proyecto).grid(row=0, column=2)

frame_botones = tk.Frame(ventana_principal)
frame_botones.pack(side=tk.LEFT, padx=20)

tk.Button(frame_botones, text="Agregar Material", command=agregar_material).pack(pady=10)
tk.Button(frame_botones, text="Limpiar Campos", command=limpiar_campos).pack(pady=10)
tk.Button(frame_botones, text="Actualizar Tabla", command=actualizar_tabla_materiales).pack(pady=10)


tabla_materiales = ttk.Treeview(ventana_principal, columns=("Nombre", "Cantidad", "Descripción"), show="headings")
tabla_materiales.pack(side=tk.RIGHT, padx=20, pady=20)

tabla_materiales.heading("Nombre", text="Nombre")
tabla_materiales.heading("Cantidad", text="Cantidad")
tabla_materiales.heading("Descripción", text="Descripción")

ventana_principal.mainloop()
