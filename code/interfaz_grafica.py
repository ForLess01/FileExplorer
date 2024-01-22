import tkinter as tk
from tkinter import filedialog, ttk
from AlmacBDSQlite import crear_tabla_archivos, insertar_o_actualizar_archivos_en_bd, eliminar_base_de_datos
import Analisis_datos
import obtener_info
import sqlite3

class ExploradorArchivosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorador de Archivos")

        # Botón para seleccionar un directorio
        self.btn_seleccionar_directorio = tk.Button(root, text="Seleccionar Directorio", command=self.seleccionar_directorio)
        self.btn_seleccionar_directorio.pack(pady=10)

        # Etiqueta para mostrar el directorio seleccionado
        self.lbl_directorio_seleccionado = tk.Label(root, text="")
        self.lbl_directorio_seleccionado.pack()

        # Botón para actualizar la base de datos
        self.btn_actualizar_bd = tk.Button(root, text="Actualizar Base de Datos", command=self.actualizar_bd)
        self.btn_actualizar_bd.pack(pady=10)

        # Botón para realizar análisis de datos
        self.btn_analisis_datos = tk.Button(root, text="Realizar Análisis de Datos", command=self.analisis_datos)
        self.btn_analisis_datos.pack(pady=10)

        # Crear Treeview para mostrar archivos
        self.treeview = ttk.Treeview(root, columns=("Nombre", "Ruta", "Fecha Creación", "Fecha Modificación", "Tamaño"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Ruta", text="Ruta")
        self.treeview.heading("Fecha Creación", text="Fecha Creación")
        self.treeview.heading("Fecha Modificación", text="Fecha Modificación")
        self.treeview.heading("Tamaño", text="Tamaño")
        self.treeview.column("#0", width=50, anchor="w")
        self.treeview.column("Nombre", width=150)
        self.treeview.column("Ruta", width=250)
        self.treeview.column("Fecha Creación", width=150)
        self.treeview.column("Fecha Modificación", width=150)
        self.treeview.column("Tamaño", width=100)
        self.treeview.pack(expand=True, fill="both")

        # Crear Treeview para mostrar archivos modificados recientemente
        self.treeview_modificados_recientemente = ttk.Treeview(root, columns=("Nombre", "Ruta", "Fecha Modificación"))
        self.treeview_modificados_recientemente.heading("#0", text="ID")
        self.treeview_modificados_recientemente.heading("Nombre", text="Nombre")
        self.treeview_modificados_recientemente.heading("Ruta", text="Ruta")
        self.treeview_modificados_recientemente.heading("Fecha Modificación", text="Fecha Modificación")
        self.treeview_modificados_recientemente.column("#0", width=50, anchor="w")
        self.treeview_modificados_recientemente.column("Nombre", width=150)
        self.treeview_modificados_recientemente.column("Ruta", width=250)
        self.treeview_modificados_recientemente.column("Fecha Modificación", width=150)
        self.treeview_modificados_recientemente.pack(expand=True, fill="both")

        # Crear Treeview para mostrar archivos más grandes
        self.treeview_archivos_grandes = ttk.Treeview(root, columns=("Nombre", "Ruta", "Tamaño"))
        self.treeview_archivos_grandes.heading("#0", text="ID")
        self.treeview_archivos_grandes.heading("Nombre", text="Nombre")
        self.treeview_archivos_grandes.heading("Ruta", text="Ruta")
        self.treeview_archivos_grandes.heading("Tamaño", text="Tamaño")
        self.treeview_archivos_grandes.column("#0", width=50, anchor="w")
        self.treeview_archivos_grandes.column("Nombre", width=150)
        self.treeview_archivos_grandes.column("Ruta", width=250)
        self.treeview_archivos_grandes.column("Tamaño", width=100)
        self.treeview_archivos_grandes.pack(expand=True, fill="both")

    def seleccionar_directorio(self):
        if hasattr(self, 'directorio_a_explorar'):
            eliminar_base_de_datos()

        directorio = filedialog.askdirectory()
        self.lbl_directorio_seleccionado.config(text=f"Directorio Seleccionado: {directorio}")
        self.directorio_a_explorar = directorio
        crear_tabla_archivos()

    def actualizar_bd(self):
        if hasattr(self, 'directorio_a_explorar'):
            crear_tabla_archivos()
            archivos = obtener_info.obtener_info_archivos(self.directorio_a_explorar)
            insertar_o_actualizar_archivos_en_bd(archivos)
            print("Base de Datos Actualizada")
            self.mostrar_archivos_en_treeview()
        else:
            print("Error: Por favor, selecciona un directorio primero.")

    def analisis_datos(self):
        archivos_modificados_recientemente = Analisis_datos.obtener_archivos_modificados_recientemente()
        archivos_mas_grandes = Analisis_datos.obtener_archivos_mas_grandes()

        # Limpiar Treeviews antes de mostrar nuevos datos
        for item in self.treeview_modificados_recientemente.get_children():
            self.treeview_modificados_recientemente.delete(item)

        for item in self.treeview_archivos_grandes.get_children():
            self.treeview_archivos_grandes.delete(item)

        # Mostrar archivos modificados recientemente
        for archivo in archivos_modificados_recientemente:
            self.treeview_modificados_recientemente.insert("", "end",
                                                           values=(archivo[0], archivo[1], archivo[2], archivo[3]))

        # Mostrar archivos más grandes
        for archivo in archivos_mas_grandes:
            self.treeview_archivos_grandes.insert("", "end", values=(archivo[0], archivo[1], archivo[2]))

    def mostrar_archivos_en_treeview(self):
        # Limpiar Treeview antes de mostrar nuevos datos
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        conn = sqlite3.connect('../explorador_archivos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM archivos")
        archivos = cursor.fetchall()
        conn.close()

        for archivo in archivos:
            self.treeview.insert("", "end", text=archivo[0], values=(archivo[1], archivo[3], archivo[4], archivo[5], archivo[6]))

# Crear la ventana principal
root = tk.Tk()
app = ExploradorArchivosGUI(root)
root.mainloop()
