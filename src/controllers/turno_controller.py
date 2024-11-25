# src/controllers/turno_controller.py

from src.database import obtener_conexion
from src.models.turno import Turno

def obtener_turnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM turnos"
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    turnos = []
    for resultado in resultados:
        turno = Turno(
            id=resultado['id'],
            descripcion=resultado['descripcion'],
            hora_inicio=resultado['hora_inicio'],
            hora_fin=resultado['hora_fin']
        )
        turnos.append(turno)
    return turnos

def agregar_turno(turno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO turnos (descripcion, hora_inicio, hora_fin)
    VALUES (%s, %s, %s)
    """
    valores = (turno.descripcion, turno.hora_inicio, turno.hora_fin)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al agregar turno: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def modificar_turno(turno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    UPDATE turnos SET descripcion = %s, hora_inicio = %s, hora_fin = %s
    WHERE id = %s
    """
    valores = (turno.descripcion, turno.hora_inicio, turno.hora_fin, turno.id)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al modificar turno: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def eliminar_turno(id_turno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "DELETE FROM turnos WHERE id = %s"
    try:
        cursor.execute(query, (id_turno,))
        conexion.commit()
        exito = True
    except Exception as err:
        print(f"Error al eliminar turno: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito
