# src/controllers/instructor_controller.py

from src.database import obtener_conexion
from src.models.instructor import Instructor
import random
import string
import hashlib

def obtener_instructores():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM instructores"
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    instructores = []
    for resultado in resultados:
        instructor = Instructor(
            ci=resultado['ci'],
            nombre=resultado['nombre'],
            apellido=resultado['apellido'],
            correo_electronico=resultado['correo_electronico']
        )
        instructores.append(instructor)
    return instructores

def agregar_instructor(instructor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Generar una contraseña aleatoria
    contraseña = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    # Hashear la contraseña
    contraseña_hash = hashlib.sha256(contraseña.encode('utf-8')).hexdigest()
    try:
        # Insertar en la tabla 'instructores'
        query_instructor = """
        INSERT INTO instructores (ci, nombre, apellido, correo_electronico)
        VALUES (%s, %s, %s, %s)
        """
        valores_instructor = (instructor.ci, instructor.nombre, instructor.apellido, instructor.correo_electronico)
        cursor.execute(query_instructor, valores_instructor)
        # Insertar en la tabla 'login'
        query_login = """
        INSERT INTO login (correo, contraseña_hash, tipo_persona, ci_persona)
        VALUES (%s, %s, %s, %s)
        """
        valores_login = (instructor.correo_electronico, contraseña_hash, 2, instructor.ci)
        cursor.execute(query_login, valores_login)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al agregar instructor: {err}")
        conexion.rollback()
        exito = False
        contraseña = None
    finally:
        cursor.close()
        conexion.close()
    return exito, contraseña

def actualizar_instructor(instructor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
        UPDATE instructores
        SET nombre = %s, apellido = %s, correo_electronico = %s
        WHERE ci = %s
        """
        valores = (instructor.nombre, instructor.apellido, instructor.correo_electronico, instructor.ci)
        cursor.execute(query, valores)
        # Actualizar correo en la tabla 'login'
        query_login = "UPDATE login SET correo = %s WHERE ci_persona = %s AND tipo_persona = 2"
        cursor.execute(query_login, (instructor.correo_electronico, instructor.ci))
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al actualizar instructor: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def eliminar_instructor(ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Verificar si el instructor tiene clases asignadas
        query_clases = "SELECT COUNT(*) FROM clase WHERE ci_instructor = %s"
        cursor.execute(query_clases, (ci,))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            # No se puede eliminar porque tiene clases asignadas
            exito = False
        else:
            # Eliminar de la tabla 'login'
            query_login = "DELETE FROM login WHERE ci_persona = %s AND tipo_persona = 2"
            cursor.execute(query_login, (ci,))
            # Eliminar de la tabla 'instructores'
            query_instructor = "DELETE FROM instructores WHERE ci = %s"
            cursor.execute(query_instructor, (ci,))
            conexion.commit()
            exito = True
    except Exception as err:
        print(f"Error al eliminar instructor: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def obtener_instructor_por_ci(ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM instructores WHERE ci = %s"
    cursor.execute(query, (ci,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado:
        instructor = Instructor(
            ci=resultado['ci'],
            nombre=resultado['nombre'],
            apellido=resultado['apellido'],
            correo_electronico=resultado['correo_electronico']
        )
        return instructor
    else:
        return None

def obtener_agenda_instructor(ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.id, a.descripcion AS actividad, t.descripcion AS turno, t.hora_inicio, t.hora_fin
    FROM clase c
    JOIN actividades a ON c.id_actividad = a.id
    JOIN turnos t ON c.id_turno = t.id
    WHERE c.ci_instructor = %s
    """
    cursor.execute(query, (ci,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados
