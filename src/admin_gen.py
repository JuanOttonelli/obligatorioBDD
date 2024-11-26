import security
from src.security import generar_hash_contraseña
#script utilizado
adminPass = generar_hash_contraseña("adminadmin")
print(adminPass)
