# src/controllers/equipo_alquiler_controller.py

from src.database import obtener_conexion
from src.models.equipo_alquiler import EquipoDeAlquiler

def obtener_equipos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT e.*, a.descripcion AS nombre_actividad
    FROM equiposDeAlquiler e
    JOIN actividades a ON e.id_actividad = a.id
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    equipos = []
    for resultado in resultados:
        equipo = EquipoDeAlquiler(
            id=resultado['id'],
            descripcion=resultado['descripcion'],
            costo=resultado['costo'],
            id_actividad=resultado['id_actividad']
        )
        equipo.nombre_actividad = resultado['nombre_actividad']
        equipos.append(equipo)
    return equipos

def agregar_equipo(equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO equiposDeAlquiler (descripcion, costo, id_actividad)
    VALUES (%s, %s, %s)
    """
    valores = (equipo.descripcion, equipo.costo, equipo.id_actividad)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al agregar equipo de alquiler: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def modificar_equipo(equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    UPDATE equiposDeAlquiler SET descripcion = %s, costo = %s, id_actividad = %s
    WHERE id = %s
    """
    valores = (equipo.descripcion, equipo.costo, equipo.id_actividad, equipo.id)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al modificar equipo de alquiler: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def eliminar_equipo(id_equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM equiposDeAlquiler WHERE id = %s"
    try:
        cursor.execute(query, (id_equipo,))
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al eliminar equipo de alquiler: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def obtener_equipos_por_actividad(id_actividad):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT * FROM equiposDeAlquiler
    WHERE id_actividad = %s
    """
    cursor.execute(query, (id_actividad,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    equipos = []
    for resultado in resultados:
        equipo = EquipoDeAlquiler(
            id=resultado['id'],
            descripcion=resultado['descripcion'],
            costo=resultado['costo'],
            id_actividad=resultado['id_actividad']
        )
        equipos.append(equipo)
    return equipos

def obtener_equipos_por_ids(equipos_ids):
    if not equipos_ids:
        return []

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    format_strings = ','.join(['%s'] * len(equipos_ids))
    query = f"SELECT e.*, a.descripcion AS nombre_actividad FROM equiposDeAlquiler e JOIN actividades a ON e.id_actividad = a.id WHERE e.id IN ({format_strings})"
    try:
        cursor.execute(query, tuple(equipos_ids))
        resultados = cursor.fetchall()
        equipos = []
        for resultado in resultados:
            equipo = EquipoDeAlquiler(
                id=resultado['id'],
                descripcion=resultado['descripcion'],
                costo=resultado['costo'],
                id_actividad=resultado['id_actividad']
            )
            equipo.nombre_actividad = resultado['nombre_actividad']
            equipos.append(equipo)
        return equipos
    except Exception as err:
        print(f"Error al obtener equipos por IDs: {err}")
        return []
    finally:
        cursor.close()
        conexion.close()