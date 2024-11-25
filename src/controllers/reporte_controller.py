# src/controllers/reporte_controller.py

from src.database import obtener_conexion


def obtener_actividades_mas_ingresos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Obtener ingresos por clases para cada actividad
    query_ingreso_clases = """
    SELECT
        a.id AS id_actividad,
        a.descripcion AS actividad,
        SUM(a.costo) AS ingreso_clases
    FROM
        actividades a
    JOIN
        clase c ON c.id_actividad = a.id
    JOIN
        alumno_clase ac ON ac.id_clase = c.id
    GROUP BY
        a.id
    """
    cursor.execute(query_ingreso_clases)
    ingresos_clases = cursor.fetchall()

    # Obtener ingresos por equipamiento para cada actividad
    query_ingreso_equipos = """
    SELECT
        a.id AS id_actividad,
        a.descripcion AS actividad,
        SUM(e.costo) AS ingreso_equipos
    FROM
        actividades a
    JOIN
        equiposDeAlquiler e ON e.id_actividad = a.id
    JOIN
        alquileres alq ON alq.equipo_id_alquiler = e.id
    GROUP BY
        a.id
    """
    cursor.execute(query_ingreso_equipos)
    ingresos_equipos = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Combinar ingresos por clases y equipos
    ingresos_dict = {}
    for ingreso in ingresos_clases:
        id_actividad = ingreso['id_actividad']
        ingresos_dict[id_actividad] = {
            'actividad': ingreso['actividad'],
            'ingreso_clases': ingreso['ingreso_clases'],
            'ingreso_equipos': 0
        }

    for ingreso in ingresos_equipos:
        id_actividad = ingreso['id_actividad']
        if id_actividad in ingresos_dict:
            ingresos_dict[id_actividad]['ingreso_equipos'] = ingreso['ingreso_equipos']
        else:
            ingresos_dict[id_actividad] = {
                'actividad': ingreso['actividad'],
                'ingreso_clases': 0,
                'ingreso_equipos': ingreso['ingreso_equipos']
            }

    # Calcular total de ingresos
    for ingreso in ingresos_dict.values():
        ingreso['total_ingresos'] = ingreso['ingreso_clases'] + ingreso['ingreso_equipos']

    # Convertir a lista y ordenar por total de ingresos descendente
    actividades_ingresos = list(ingresos_dict.values())
    actividades_ingresos.sort(key=lambda x: x['total_ingresos'], reverse=True)

    return actividades_ingresos

def obtener_actividades_con_mas_alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT
        a.descripcion AS actividad,
        COUNT(DISTINCT ac.ci_alumno) AS total_alumnos
    FROM
        actividades a
    JOIN
        clase c ON c.id_actividad = a.id
    JOIN
        alumno_clase ac ON ac.id_clase = c.id
    GROUP BY
        a.id
    ORDER BY
        total_alumnos DESC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados


def obtener_turnos_con_mas_clases():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT
        t.descripcion AS turno,
        COUNT(c.id) AS total_clases
    FROM
        turnos t
    JOIN
        clase c ON c.id_turno = t.id
    GROUP BY
        t.id
    ORDER BY
        total_clases DESC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados
