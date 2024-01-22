import obtener_info
import AlmacBDSQlite
import Analisis_datos
import tkinter as tk
from tkinter import filedialog
from interfaz_grafica import ExploradorArchivosGUI
from AlmacBDSQlite import crear_tabla_archivos, eliminar_base_de_datos

# Crear la interfaz gráfica
root = tk.Tk()
app = ExploradorArchivosGUI(root)

# Llamar a la función seleccionar_directorio en algún momento
app.seleccionar_directorio()

# Ejecutar el bucle principal de la interfaz gráfica
root.mainloop()

# Obtener información
directorio_a_explorar = 'C:/Users/juan7/OneDrive/Escritorio/DOCStry'
archivos = obtener_info.obtener_info_archivos(directorio_a_explorar)

# Crear la tabla si no existe
AlmacBDSQlite.crear_tabla_archivos()

# Insertar información en la base de datos
AlmacBDSQlite.insertar_o_actualizar_archivos_en_bd(archivos)

# Ejemplos de análisis de datos
ruta_archivo_accedido = "C:/Users/juan7/OneDrive/Escritorio/DOCStry/PRactica nr 01 Alfonte.pdf"
Analisis_datos.actualizar_frecuencia_acceso(ruta_archivo_accedido)

archivos_modificados_recientemente = Analisis_datos.obtener_archivos_modificados_recientemente()
print("Archivos modificados recientemente:")
for archivo in archivos_modificados_recientemente:
    print(archivo)

archivos_mas_grandes = Analisis_datos.obtener_archivos_mas_grandes()
print("Archivos más grandes:")
for archivo in archivos_mas_grandes:
    print(archivo)
