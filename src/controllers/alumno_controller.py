# src/controllers/alumno_controller.py
from src.controllers.password_gen import generar_contraseña_aleatoria
from src.database import obtener_conexion
from src.models.alumno import Alumno
import random
import string
import hashlib

from src.security import generar_hash_contraseña


def obtener_alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM estudiantes"
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    alumnos = []
    for resultado in resultados:
        alumno = Alumno(
            ci=resultado['ci'],
            nombre=resultado['nombre'],
            apellido=resultado['apellido'],
            fecha_nacimiento=resultado['fecha_nacimiento'],
            telefono=resultado['telefono'],
            correo_electronico=resultado['correo_electronico']
        )
        alumnos.append(alumno)
    return alumnos

def agregar_alumno(alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Generar una contraseña aleatoria
    contraseña = generar_contraseña_aleatoria()
    contraseña_hash = generar_hash_contraseña(contraseña)
    try:
        # Insertar en la tabla 'estudiantes'
        query_estudiante = """
        INSERT INTO estudiantes (ci, nombre, apellido, fecha_nacimiento, telefono, correo_electronico)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores_estudiante = (alumno.ci, alumno.nombre, alumno.apellido, alumno.fecha_nacimiento, alumno.telefono, alumno.correo_electronico)
        cursor.execute(query_estudiante, valores_estudiante)
        # Insertar en la tabla 'login'
        query_login = """
        INSERT INTO login (correo, contraseña_hash, tipo_persona, ci_persona)
        VALUES (%s, %s, %s, %s)
        """
        valores_login = (alumno.correo_electronico, contraseña_hash, 1, alumno.ci)
        cursor.execute(query_login, valores_login)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al agregar alumno: {err}")
        conexion.rollback()
        exito = False
        contraseña = None
    finally:
        cursor.close()
        conexion.close()
    return exito, contraseña

def actualizar_alumno(alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
        UPDATE estudiantes
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s, telefono = %s, correo_electronico = %s
        WHERE ci = %s
        """
        valores = (alumno.nombre, alumno.apellido, alumno.fecha_nacimiento, alumno.telefono, alumno.correo_electronico, alumno.ci)
        cursor.execute(query, valores)
        # Actualizar correo en la tabla 'login'
        query_login = "UPDATE login SET correo = %s WHERE ci_persona = %s AND tipo_persona = 1"
        cursor.execute(query_login, (alumno.correo_electronico, alumno.ci))
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al actualizar alumno: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def eliminar_alumno(ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Eliminar de la tabla 'login'
        query_login = "DELETE FROM login WHERE ci_persona = %s AND tipo_persona = 1"
        cursor.execute(query_login, (ci,))
        # Eliminar de la tabla 'estudiantes'
        query_estudiante = "DELETE FROM estudiantes WHERE ci = %s"
        cursor.execute(query_estudiante, (ci,))
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al eliminar alumno: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def obtener_alumno_por_ci(ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM estudiantes WHERE ci = %s"
    cursor.execute(query, (ci,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado:
        alumno = Alumno(
            ci=resultado['ci'],
            nombre=resultado['nombre'],
            apellido=resultado['apellido'],
            fecha_nacimiento=resultado['fecha_nacimiento'],
            telefono=resultado['telefono'],
            correo_electronico=resultado['correo_electronico']
        )
        return alumno
    else:
        return None
