# alumno_controller.py
from src.database import obtener_conexion
from src.models.alumno import Alumno
from src.security import generar_hash_contraseña
from src.controllers.password_gen import generar_contraseña_aleatoria
import random
import string

def obtener_alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM estudiantes"
    cursor.execute(query)
    resultados = cursor.fetchall()
    alumnos = [Alumno(**row) for row in resultados]
    cursor.close()
    conexion.close()
    return alumnos


def agregar_alumno(alumno):
    # Generar una contraseña aleatoria
    contraseña = generar_contraseña_aleatoria()
    contraseña_hash = generar_hash_contraseña(contraseña)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Insertar el alumno en la tabla estudiantes
        query_estudiante = """
        INSERT INTO estudiantes (ci, nombre, apellido, fecha_nacimiento, telefono, correo_electronico)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores_estudiante = (
        alumno.ci, alumno.nombre, alumno.apellido, alumno.fecha_nacimiento, alumno.telefono, alumno.correo_electronico)
        cursor.execute(query_estudiante, valores_estudiante)

        # Insertar en la tabla login
        query_login = """
        INSERT INTO login (correo, contraseña_hash, tipo_persona, ci_persona)
        VALUES (%s, %s, %s, %s)
        """
        tipo_persona = 3
        valores_login = (alumno.correo_electronico, contraseña_hash, tipo_persona, alumno.ci)
        cursor.execute(query_login, valores_login)

        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al agregar alumno: {err}")
        conexion.rollback()
        exito = False
        contraseña = None  # No se pudo generar la contraseña
    finally:
        cursor.close()
        conexion.close()
    return exito, contraseña

def eliminar_alumno(ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM estudiantes WHERE ci = %s"
    cursor.execute(query, (ci,))
    conexion.commit()
    cursor.close()
    conexion.close()
