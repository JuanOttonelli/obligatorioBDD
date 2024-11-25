# src/controllers/alquiler_controller.py

from src.database import obtener_conexion
from src.models.alquiler import Alquiler

def registrar_alquiler(alquiler):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO alquileres (alumno_ci, clase_id, equipo_id_alquiler)
    VALUES (%s, %s, %s)
    """
    valores = (alquiler.alumno_ci, alquiler.clase_id, alquiler.equipo_id_alquiler)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al registrar alquiler: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def obtener_alquileres_por_clase(clase_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT a.*, e.descripcion AS descripcion_equipo, e.costo
    FROM alquileres a
    JOIN equiposDeAlquiler e ON a.equipo_id_alquiler = e.id
    WHERE a.clase_id = %s
    """
    cursor.execute(query, (clase_id,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    alquileres = []
    for resultado in resultados:
        alquiler = Alquiler(
            id=resultado['id'],
            alumno_ci=resultado['alumno_ci'],
            clase_id=resultado['clase_id'],
            equipo_id_alquiler=resultado['equipo_id_alquiler']
        )
        alquiler.descripcion_equipo = resultado['descripcion_equipo']
        alquiler.costo_equipo = resultado['costo']
        alquileres.append(alquiler)
    return alquileres

def obtener_alquileres_por_alumno(alumno_ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT a.*, e.descripcion AS descripcion_equipo, e.costo
    FROM alquileres a
    JOIN equiposDeAlquiler e ON a.equipo_id_alquiler = e.id
    WHERE a.alumno_ci = %s
    """
    cursor.execute(query, (alumno_ci,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    alquileres = []
    for resultado in resultados:
        alquiler = Alquiler(
            id=resultado['id'],
            alumno_ci=resultado['alumno_ci'],
            clase_id=resultado['clase_id'],
            equipo_id_alquiler=resultado['equipo_id_alquiler']
        )
        alquiler.descripcion_equipo = resultado['descripcion_equipo']
        alquiler.costo_equipo = resultado['costo']
        alquileres.append(alquiler)
    return alquileres
