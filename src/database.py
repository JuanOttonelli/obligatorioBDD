# database.py
import mysql.connector

#conexión a base de datos
def obtener_conexion():
    conexion = mysql.connector.connect(
        host='127.0.0.1',
        user='', #Ingresar usuario propio
        password='', #Ingresar contraseña propia
        database='escuela_deportes_nieve'
    )
    return conexion
