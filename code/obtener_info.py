import os
import datetime

def obtener_info_archivos(directorio):
    lista_archivos = []

    for root, dirs, files in os.walk(directorio):
        for nombre_archivo in files:
            ruta_archivo = os.path.join(root, nombre_archivo)
            fecha_creacion = datetime.datetime.fromtimestamp(os.path.getctime(ruta_archivo)).strftime('%Y-%m-%d %H:%M:%S')
            fecha_modificacion = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_archivo)).strftime('%Y-%m-%d %H:%M:%S')
            tamano = os.path.getsize(ruta_archivo)

            info_archivo = {
                'nombre': nombre_archivo,
                'ruta': ruta_archivo,
                'fecha_creacion': fecha_creacion,
                'fecha_modificacion': fecha_modificacion,
                'tamano': tamano
            }

            lista_archivos.append(info_archivo)

    return lista_archivos

if __name__ == "__main__":
    directorio_a_explorar = 'C:/Users/juan7/OneDrive/Escritorio/DOCStry'
    archivos = obtener_info_archivos(directorio_a_explorar)
    print(archivos)
