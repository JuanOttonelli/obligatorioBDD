# src/controllers/instructor_controller.py

from src.database import obtener_conexion
from src.models.instructor import Instructor

def obtener_instructores():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM instructores"
    cursor.execute(query)
    resultados = cursor.fetchall()
    instructores = [Instructor(**row) for row in resultados]
    cursor.close()
    conexion.close()
    return instructores

def agregar_instructor(instructor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO instructores (ci, nombre, apellido)
    VALUES (%s, %s, %s)
    """
    valores = (instructor.ci, instructor.nombre, instructor.apellido)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al agregar instructor: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def actualizar_instructor(instructor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    UPDATE instructores
    SET nombre = %s, apellido = %s
    WHERE ci = %s
    """
    valores = (instructor.nombre, instructor.apellido, instructor.ci)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al actualizar instructor: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def eliminar_instructor(ci_instructor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM instructores WHERE ci = %s"
    try:
        cursor.execute(query, (ci_instructor,))
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al eliminar instructor: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def obtener_agenda_instructor(ci_instructor):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.id, t.hora_inicio, t.hora_fin, a.descripcion AS actividad
    FROM clase c
    JOIN turnos t ON c.id_turno = t.id
    JOIN actividades a ON c.id_actividad = a.id
    WHERE c.ci_instructor = %s
    """
    cursor.execute(query, (ci_instructor,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados
