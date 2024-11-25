# src/controllers/clase_controller.py

from src.database import obtener_conexion
from src.models.clase import Clase

def obtener_clases():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.*, i.nombre AS nombre_instructor, i.apellido AS apellido_instructor, a.descripcion AS actividad, t.hora_inicio, t.hora_fin, t.descripcion AS turno_descripcion
    FROM clase c
    JOIN instructores i ON c.ci_instructor = i.ci
    JOIN actividades a ON c.id_actividad = a.id
    JOIN turnos t ON c.id_turno = t.id
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    clases = []
    for resultado in resultados:
        clase = Clase(
            id=resultado['id'],
            ci_instructor=resultado['ci_instructor'],
            id_actividad=resultado['id_actividad'],
            id_turno=resultado['id_turno'],
            dictada=resultado['dictada']
        )
        # Asignar atributos adicionales
        clase.nombre_instructor = resultado['nombre_instructor']
        clase.apellido_instructor = resultado['apellido_instructor']
        clase.actividad = resultado['actividad']
        clase.hora_inicio = resultado['hora_inicio']
        clase.hora_fin = resultado['hora_fin']
        clase.turno_descripcion = resultado['turno_descripcion']
        clases.append(clase)
    return clases

def obtener_clase_por_id(id_clase):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.*, i.nombre AS nombre_instructor, i.apellido AS apellido_instructor, a.descripcion AS actividad, t.hora_inicio, t.hora_fin, t.descripcion AS turno_descripcion
    FROM clase c
    JOIN instructores i ON c.ci_instructor = i.ci
    JOIN actividades a ON c.id_actividad = a.id
    JOIN turnos t ON c.id_turno = t.id
    WHERE c.id = %s
    """
    cursor.execute(query, (id_clase,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado:
        clase = Clase(
            id=resultado['id'],
            ci_instructor=resultado['ci_instructor'],
            id_actividad=resultado['id_actividad'],
            id_turno=resultado['id_turno'],
            dictada=resultado['dictada']
        )
        # Asignar atributos adicionales
        clase.nombre_instructor = resultado['nombre_instructor']
        clase.apellido_instructor = resultado['apellido_instructor']
        clase.actividad = resultado['actividad']
        clase.hora_inicio = resultado['hora_inicio']
        clase.hora_fin = resultado['hora_fin']
        clase.turno_descripcion = resultado['turno_descripcion']
        return clase
    else:
        return None

def obtener_clases_disponibles(ci_alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.*, a.descripcion AS actividad_nombre, t.descripcion AS turno_descripcion
    FROM clase c
    JOIN actividades a ON c.id_actividad = a.id
    JOIN turnos t ON c.id_turno = t.id
    WHERE c.id NOT IN (
        SELECT ac.id_clase
        FROM alumno_clase ac
        WHERE ac.ci_alumno = %s
    ) AND t.id NOT IN (
        SELECT t2.id
        FROM clase c2
        JOIN alumno_clase ac2 ON c2.id = ac2.id_clase
        JOIN turnos t2 ON c2.id_turno = t2.id
        WHERE ac2.ci_alumno = %s
    )
    """
    cursor.execute(query, (ci_alumno, ci_alumno))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    clases = []
    for resultado in resultados:
        clase = Clase(
            id=resultado['id'],
            ci_instructor=resultado['ci_instructor'],
            id_actividad=resultado['id_actividad'],
            id_turno=resultado['id_turno'],
            dictada=resultado['dictada']
        )
        # Asignar atributos adicionales
        clase.actividad_nombre = resultado['actividad_nombre']
        clase.turno_descripcion = resultado['turno_descripcion']
        clases.append(clase)
    return clases

def obtener_clases_inscritas_por_alumno(ci_alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.*, a.descripcion AS actividad_nombre, t.descripcion AS turno_descripcion, i.nombre AS nombre_instructor, i.apellido AS apellido_instructor, t.hora_inicio, t.hora_fin
    FROM clase c
    JOIN alumno_clase ac ON c.id = ac.id_clase
    JOIN actividades a ON c.id_actividad = a.id
    JOIN turnos t ON c.id_turno = t.id
    JOIN instructores i ON c.ci_instructor = i.ci
    WHERE ac.ci_alumno = %s
    """
    cursor.execute(query, (ci_alumno,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    clases = []
    for resultado in resultados:
        clase = Clase(
            id=resultado['id'],
            ci_instructor=resultado['ci_instructor'],
            id_actividad=resultado['id_actividad'],
            id_turno=resultado['id_turno'],
            dictada=resultado['dictada']
        )
        # Asignar atributos adicionales
        clase.actividad_nombre = resultado['actividad_nombre']
        clase.turno_descripcion = resultado['turno_descripcion']
        clase.nombre_instructor = resultado['nombre_instructor']
        clase.apellido_instructor = resultado['apellido_instructor']
        clase.hora_inicio = resultado['hora_inicio']
        clase.hora_fin = resultado['hora_fin']
        clases.append(clase)
    return clases

def obtener_clases_por_instructor(ci_instructor):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.*, a.descripcion AS actividad_nombre, t.descripcion AS turno_descripcion, t.hora_inicio, t.hora_fin
    FROM clase c
    JOIN actividades a ON c.id_actividad = a.id
    JOIN turnos t ON c.id_turno = t.id
    WHERE c.ci_instructor = %s
    """
    cursor.execute(query, (ci_instructor,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    clases = []
    for resultado in resultados:
        clase = Clase(
            id=resultado['id'],
            ci_instructor=resultado['ci_instructor'],
            id_actividad=resultado['id_actividad'],
            id_turno=resultado['id_turno'],
            dictada=resultado['dictada']
        )
        # Asignar atributos adicionales
        clase.actividad_nombre = resultado['actividad_nombre']
        clase.turno_descripcion = resultado['turno_descripcion']
        clase.hora_inicio = resultado['hora_inicio']
        clase.hora_fin = resultado['hora_fin']
        clases.append(clase)
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
    except Exception as err:
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
    except Exception as err:
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
    except Exception as err:
        print(f"Error al eliminar clase: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def agregar_alumno_a_clase(id_clase, ci_alumno):
    # Validar que el alumno no esté inscrito en otra clase en el mismo turno
    if alumno_en_turno(ci_alumno, id_clase):
        print("El alumno ya está inscrito en otra clase en el mismo turno.")
        return False
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO alumno_clase (id_clase, ci_alumno)
    VALUES (%s, %s)
    """
    valores = (id_clase, ci_alumno)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
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
    except Exception as err:
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
    SELECT ac.*, e.nombre, e.apellido
    FROM alumno_clase ac
    JOIN estudiantes e ON ac.ci_alumno = e.ci
    WHERE ac.id_clase = %s
    """
    cursor.execute(query, (id_clase,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados

def alumno_en_turno(ci_alumno, id_clase):
    # Verificar si el alumno ya está inscrito en otra clase en el mismo turno
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    SELECT COUNT(*)
    FROM alumno_clase ac
    JOIN clase c ON ac.id_clase = c.id
    WHERE ac.ci_alumno = %s AND c.id_turno = (
        SELECT id_turno FROM clase WHERE id = %s
    )
    """
    cursor.execute(query, (ci_alumno, id_clase))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado[0] > 0

def obtener_costo_clase(id_clase):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    SELECT a.costo
    FROM clase c
    JOIN actividades a ON c.id_actividad = a.id
    WHERE c.id = %s
    """
    cursor.execute(query, (id_clase,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado:
        return resultado[0]
    else:
        return 0.0

def inscribir_alumno_en_clase(id_clase, ci_alumno):
    # Validar que el alumno no esté inscrito en otra clase en el mismo turno
    if alumno_en_turno(ci_alumno, id_clase):
        print("El alumno ya está inscrito en otra clase en el mismo turno.")
        return False
    # Inscribir al alumno en la clase
    exito = agregar_alumno_a_clase(id_clase, ci_alumno)
    return exito
