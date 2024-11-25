# src/controllers/login_controller.py

from src.database import obtener_conexion
from src.security import verificar_contraseña  # Lo utilizaremos más adelante
from src.security import generar_hash_contraseña

def verificar_credenciales(correo, contraseña):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT contraseña_hash, tipo_persona, ci_persona FROM login WHERE correo = %s"
    cursor.execute(query, (correo,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()

    if resultado:
        # Verificar la contraseña utilizando la función verificar_contraseña
        if verificar_contraseña(contraseña, resultado['contraseña_hash']):
            return {
                'autenticado': True,
                'tipo_persona': resultado['tipo_persona'],
                'ci_persona': resultado['ci_persona']
            }
    # En caso de que el correo no exista o la contraseña sea incorrecta
    return {'autenticado': False}

def registrar_usuario(correo, contraseña, tipo_persona, ci_persona):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Genera el hash de la contraseña
    contraseña_hash = generar_hash_contraseña(contraseña)
    query = """
    INSERT INTO login (correo, contraseña_hash, tipo_persona, ci_persona)
    VALUES (%s, %s, %s, %s)
    """
    valores = (correo, contraseña_hash, tipo_persona, ci_persona)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Exception as err:
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
