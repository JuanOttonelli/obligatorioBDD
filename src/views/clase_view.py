# src/views/clase_view.py

import tkinter as tk
from tkinter import messagebox
from src.controllers.clase_controller import obtener_clases, agregar_clase, actualizar_clase, eliminar_clase, agregar_alumno_a_clase, quitar_alumno_de_clase, obtener_alumnos_de_clase
from src.models.clase import Clase

class ClaseView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)
        # Aquí implementas la interfaz para gestionar clases
        # Puedes listar clases, agregar nuevas, modificar y eliminar
