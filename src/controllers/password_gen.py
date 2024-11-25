# src/controllers/password_gen.py

import random
import string

def generar_contraseña_aleatoria(longitud=8):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(random.choice(caracteres) for i in range(longitud))
    return contraseña
