# src/controllers/actividad_controller.py

from src.database import obtener_conexion
from src.models.actividad import Actividad

def obtener_actividades():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM actividades"
    cursor.execute(query)
    resultados = cursor.fetchall()
    actividades = [Actividad(**row) for row in resultados]
    cursor.close()
    conexion.close()
    return actividades

def agregar_actividad(actividad):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO actividades (descripcion, costo, restriccion_edad)
    VALUES (%s, %s, %s)
    """
    valores = (actividad.descripcion, actividad.costo, actividad.restriccion_edad)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        actividad.id = cursor.lastrowid  # Obtener el ID de la actividad recién insertada
        exito = True
    except Exception as err:
        print(f"Error al agregar actividad: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def actualizar_actividad(actividad):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    UPDATE actividades
    SET descripcion = %s, costo = %s, restriccion_edad = %s
    WHERE id = %s
    """
    valores = (actividad.descripcion, actividad.costo, actividad.restriccion_edad, actividad.id)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al actualizar actividad: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def eliminar_actividad(id_actividad):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM actividades WHERE id = %s"
    try:
        cursor.execute(query, (id_actividad,))
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al eliminar actividad: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito
