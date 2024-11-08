# alumno_controller.py
from src.database import obtener_conexion
from src.models.alumno import Alumno

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
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO estudiantes (ci, nombre, apellido, fecha_nacimiento, telefono, correo_electronico)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (alumno.ci, alumno.nombre, alumno.apellido, alumno.fecha_nacimiento, alumno.telefono, alumno.correo_electronico)
    cursor.execute(query, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_alumno(ci):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM estudiantes WHERE ci = %s"
    cursor.execute(query, (ci,))
    conexion.commit()
    cursor.close()
    conexion.close()
