# src/controllers/clase_controller.py

from src.database import obtener_conexion
from src.models.clase import Clase

def obtener_clases():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.*, i.nombre AS nombre_instructor, i.apellido AS apellido_instructor, a.descripcion AS actividad, t.hora_inicio, t.hora_fin
    FROM clase c
    JOIN instructores i ON c.ci_instructor = i.ci
    JOIN actividades a ON c.id_actividad = a.id
    JOIN turnos t ON c.id_turno = t.id
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    clases = [Clase(**row) for row in resultados]
    cursor.close()
    conexion.close()
    return clases

def agregar_clase(clase):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO clase (ci_instructor, id_actividad, id_turno, dictada)
    VALUES (%s, %s, %s, %s)
    """
    valores = (clase.ci_instructor, clase.id_actividad, clase.id_turno, clase.dictada)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        clase.id = cursor.lastrowid  # Obtener el ID de la clase recién insertada
        exito = True
    except conexion.Error as err:
        print(f"Error al agregar clase: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def actualizar_clase(clase):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    UPDATE clase
    SET ci_instructor = %s, id_actividad = %s, id_turno = %s, dictada = %s
    WHERE id = %s
    """
    valores = (clase.ci_instructor, clase.id_actividad, clase.id_turno, clase.dictada, clase.id)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al actualizar clase: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def eliminar_clase(id_clase):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM clase WHERE id = %s"
    try:
        cursor.execute(query, (id_clase,))
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al eliminar clase: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def agregar_alumno_a_clase(id_clase, ci_alumno, id_equipamiento=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento)
    VALUES (%s, %s, %s)
    """
    valores = (id_clase, ci_alumno, id_equipamiento)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al agregar alumno a clase: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def quitar_alumno_de_clase(id_clase, ci_alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM alumno_clase WHERE id_clase = %s AND ci_alumno = %s"
    try:
        cursor.execute(query, (id_clase, ci_alumno))
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al quitar alumno de clase: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def obtener_alumnos_de_clase(id_clase):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT ac.*, e.nombre, e.apellido, eq.descripcion AS equipamiento
    FROM alumno_clase ac
    JOIN estudiantes e ON ac.ci_alumno = e.ci
    LEFT JOIN equiposDeAlquiler eq ON ac.id_equipamiento = eq.id
    WHERE ac.id_clase = %s
    """
    cursor.execute(query, (id_clase,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados
