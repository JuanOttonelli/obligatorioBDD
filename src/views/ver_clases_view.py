# src/views/ver_clases_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import clase_controller, equipo_alquiler_controller
from src.views import session

class VerClasesView:
    def __init__(self, master):
        self.master = master
        self.master.title('Ver Clases')
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Clases Disponibles", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Crear el Treeview para mostrar las clases
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Actividad", "Turno"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Actividad", text="Actividad")
        self.tree.heading("Turno", text="Turno")
        self.tree.grid(row=1, column=0, columnspan=2)

        # Cargar las clases disponibles
        self.cargar_clases()

        # Botón Volver
        tk.Button(self.frame, text="Volver", command=self.volver).grid(row=2, column=0, columnspan=2, pady=10)

    def cargar_clases(self):
        # Obtener las clases disponibles
        ci_alumno = session.usuario_actual.get('ci_persona')
        clases = clase_controller.obtener_clases_disponibles(ci_alumno)

        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar las clases en el Treeview
        for clase in clases:
            self.tree.insert("", "end", values=(clase.id, clase.actividad_nombre, clase.turno_descripcion))

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
