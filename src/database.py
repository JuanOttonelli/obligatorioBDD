# database.py
import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='rootpassword',
        database='escuela_deportes_nieve'
    )
    return conexion
