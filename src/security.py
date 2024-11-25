# src/security.py

import bcrypt

def generar_hash_contraseña(contraseña):
    # Convierte la contraseña a bytes
    contraseña_bytes = contraseña.encode('utf-8')
    # Genera una sal y hashea la contraseña
    contraseña_hash = bcrypt.hashpw(contraseña_bytes, bcrypt.gensalt())
    # Retorna el hash como string
    return contraseña_hash.decode('utf-8')

def verificar_contraseña(contraseña_ingresada, contraseña_hash_almacenada):
    # Convierte la contraseña ingresada y el hash almacenado a bytes
    contraseña_ingresada_bytes = contraseña_ingresada.encode('utf-8')
    contraseña_hash_almacenada_bytes = contraseña_hash_almacenada.encode('utf-8')
    # Verifica si la contraseña coincide con el hash
    return bcrypt.checkpw(contraseña_ingresada_bytes, contraseña_hash_almacenada_bytes)
