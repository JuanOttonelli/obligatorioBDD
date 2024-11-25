# src/controllers/instructor_controller.py

from src.database import obtener_conexion
from src.models.instructor import Instructor
from src.security import generar_hash_contraseña
from src.controllers.password_gen import generar_contraseña_aleatoria
import random
import string

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
    # Generar una contraseña aleatoria
    contraseña = generar_contraseña_aleatoria()
    contraseña_hash = generar_hash_contraseña(contraseña)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Insertar el instructor en la tabla instructores
        query_instructor = """
        INSERT INTO instructores (ci, nombre, apellido, correo_electronico)
        VALUES (%s, %s, %s, %s)
        """
        valores_instructor = (instructor.ci, instructor.nombre, instructor.apellido, instructor.correo_electronico)
        cursor.execute(query_instructor, valores_instructor)

        # Insertar en la tabla login
        query_login = """
        INSERT INTO login (correo, contraseña_hash, tipo_persona, ci_persona)
        VALUES (%s, %s, %s, %s)
        """
        tipo_persona = '2'
        valores_login = (instructor.correo_electronico, contraseña_hash, tipo_persona, instructor.ci)
        cursor.execute(query_login, valores_login)

        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al agregar instructor: {err}")
        conexion.rollback()
        exito = False
        contraseña = None  # No se pudo generar la contraseña
    finally:
        cursor.close()
        conexion.close()
    return exito, contraseña

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
