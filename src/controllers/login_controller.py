# src/controllers/login_controller.py

from src.database import obtener_conexion

def verificar_credenciales(correo, contraseña):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT contraseña, tipo_persona, ci_persona FROM login WHERE correo = %s"
    cursor.execute(query, (correo,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado and resultado['contraseña'] == contraseña:
        return {
            'autenticado': True,
            'tipo_persona': resultado['tipo_persona'],
            'ci_persona': resultado['ci_persona']
        }
    else:
        return {'autenticado': False}

def registrar_usuario(correo, contraseña, tipo_persona, ci_persona):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO login (correo, contraseña, tipo_persona, ci_persona)
    VALUES (%s, %s, %s, %s)
    """
    valores = (correo, contraseña, tipo_persona, ci_persona)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except conexion.Error as err:
        print(f"Error al registrar usuario: {err}")
        conexion.rollback()
        exito = False
    finally:
        cursor.close()
        conexion.close()
    return exito

def obtener_tipo_persona_descripcion(id_tipo_persona):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "SELECT descripcion FROM tiposPersonas WHERE id = %s"
    cursor.execute(query, (id_tipo_persona,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado:
        return resultado[0]
    else:
        return None
