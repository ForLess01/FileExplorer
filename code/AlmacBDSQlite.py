import obtener_info
import sqlite3
import os

def crear_tabla_archivos():
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archivos (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            nombre_anterior TEXT, 
            ruta TEXT,
            fecha_creacion TEXT,
            fecha_modificacion TEXT,
            tamano INTEGER,
            eliminado INTEGER DEFAULT 0,
            frecuencia_acceso INTEGER DEFAULT 0
        )
    ''')

    cursor.execute("PRAGMA table_info(archivos)")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM archivos")
    print(cursor.fetchall())

    conn.commit()
    conn.close()

def insertar_o_actualizar_archivos_en_bd(lista_archivos):
    if lista_archivos is None:
        print("Error: La lista de archivos es None.")
        return

    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    for archivo in lista_archivos:
        # Buscar archivo existente por ruta
        cursor.execute('SELECT * FROM archivos WHERE ruta = ?', (archivo['ruta'],))
        existing_file = cursor.fetchone()

        if existing_file:
            # Actualizar detalles del archivo existente
            cursor.execute('''
                UPDATE archivos
                SET nombre_anterior = ?, nombre = ?, fecha_creacion = ?, fecha_modificacion = ?, tamano = ?, eliminado = 0
                WHERE ruta = ?
            ''', (existing_file[1], archivo['nombre'], archivo['fecha_creacion'], archivo['fecha_modificacion'],
                    archivo['tamano'], archivo['ruta']))
            print(f"Información de archivo actualizada/encontrada en la base de datos: {archivo['nombre']}")
        else:
            # Insertar nuevo archivo
            cursor.execute('''
                INSERT INTO archivos (nombre, nombre_anterior, ruta, fecha_creacion, fecha_modificacion, tamano)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
            archivo['nombre'], "", archivo['ruta'], archivo['fecha_creacion'], archivo['fecha_modificacion'],
            archivo['tamano']))
            print(f"Archivo almacenado en la base de datos: {archivo['nombre']}")

    # Buscar archivos obsoletos (existen en la base de datos pero no en la lista actual)
    cursor.execute('SELECT ruta FROM archivos')
    existing_files = [file[0] for file in cursor.fetchall()]

    for existing_file in existing_files:
        if existing_file not in [archivo['ruta'] for archivo in lista_archivos]:
            # Marcar como eliminado o eliminar según tu lógica
            cursor.execute('UPDATE archivos SET eliminado = 1 WHERE ruta = ?', (existing_file,))
            print(f"Archivo marcado como eliminado en la base de datos: {existing_file}")

    conn.commit()
    conn.close()

def verificar_renombrado(ruta_archivo):
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nombre, nombre_anterior FROM archivos WHERE ruta = ?', (ruta_archivo,))
    archivo_info = cursor.fetchone()

    if archivo_info:
        nombre_actual = archivo_info[0]
        nombre_anterior = archivo_info[1]

        if nombre_actual != nombre_anterior:
            print(f"El archivo ha sido renombrado de '{nombre_anterior}' a '{nombre_actual}'.")
        else:
            print("El archivo no ha sido renombrado.")

    conn.close()

def eliminar_base_de_datos():
    ruta_base_de_datos = '../explorador_archivos.db'
    if os.path.exists(ruta_base_de_datos):
        os.remove(ruta_base_de_datos)
        print("Base de Datos Eliminada")

# Crear la tabla si no existe
crear_tabla_archivos()

# Insertar la información de los archivos en la base de datos
insertar_o_actualizar_archivos_en_bd(obtener_info.obtener_info_archivos('C:/Users/juan7/OneDrive/Escritorio/DOCStry'))
