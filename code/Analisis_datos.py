import sqlite3
import datetime

def actualizar_frecuencia_acceso(ruta_archivo):
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE archivos
        SET frecuencia_acceso = frecuencia_acceso + 1
        WHERE ruta = ?
    ''', (ruta_archivo,))

    conn.commit()
    conn.close()

# Supongamos que el archivo "/ruta/ejemplo.txt" fue accedido
ruta_archivo_accedido = "C:/Users/juan7/OneDrive/Escritorio/DOCStry/PRactica nr 01 Alfonte.pdf"
actualizar_frecuencia_acceso(ruta_archivo_accedido)

def obtener_archivos_modificados_recientemente():
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        SELECT * FROM archivos
        WHERE fecha_modificacion > ?
    ''', (fecha_limite,))

    archivos_modificados = cursor.fetchall()

    conn.close()

    return archivos_modificados

archivos_modificados_recientemente = obtener_archivos_modificados_recientemente()
print("Archivos modificados recientemente:")
for archivo in archivos_modificados_recientemente:
    print(archivo)


def obtener_archivos_mas_grandes(num_archivos=5):
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM archivos
        ORDER BY tamano DESC
        LIMIT ?
    ''', (num_archivos,))

    archivos_mas_grandes = cursor.fetchall()

    conn.close()

    return archivos_mas_grandes

archivos_mas_grandes = obtener_archivos_mas_grandes()
print("Archivos más grandes:")
for archivo in archivos_mas_grandes:
    print(archivo)

def obtener_archivos_antiguos(dias=30):
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=dias)).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        SELECT * FROM archivos
        WHERE fecha_creacion < ?
    ''', (fecha_limite,))

    archivos_antiguos = cursor.fetchall()

    conn.close()

    return archivos_antiguos

archivos_antiguos = obtener_archivos_antiguos()
print("Archivos antiguos:")
for archivo in archivos_antiguos:
    print(archivo)


def obtener_posibles_duplicados():
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT nombre, COUNT(*) as cantidad
        FROM archivos
        GROUP BY nombre
        HAVING COUNT(*) > 1
    ''')

    posibles_duplicados = cursor.fetchall()

    conn.close()

    return posibles_duplicados

posibles_duplicados = obtener_posibles_duplicados()
print("Posibles duplicados:")
for duplicado in posibles_duplicados:
    print(f"Nombre: {duplicado[0]}, Cantidad: {duplicado[1]}")


def recomendar_eliminacion_antiguedad_tamano(dias=60, tamano_limite=1024 * 1024 * 100):  # Ejemplo de tamaño límite: 100 MB
    conn = sqlite3.connect('../explorador_archivos.db')
    cursor = conn.cursor()

    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=dias)).strftime('%Y-%m-%d %H:%M:%S')

    # Archivos antiguos
    cursor.execute('''
        SELECT * FROM archivos
        WHERE fecha_creacion < ? AND eliminado = 0
    ''', (fecha_limite,))
    archivos_antiguos = cursor.fetchall()

    # Archivos grandes
    cursor.execute('''
        SELECT * FROM archivos
        WHERE tamano > ? AND eliminado = 0
    ''', (tamano_limite,))
    archivos_grandes = cursor.fetchall()

    conn.close()

    return archivos_antiguos, archivos_grandes

archivos_antiguos, archivos_grandes = recomendar_eliminacion_antiguedad_tamano()
print("Recomendación de eliminación por antigüedad:")
for archivo in archivos_antiguos:
    print(archivo)
print("\nRecomendación de eliminación por tamaño:")
for archivo in archivos_grandes:
    print(archivo)
