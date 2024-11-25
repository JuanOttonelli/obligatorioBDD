# src/views/ver_clases_instructor_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import clase_controller
from src.views import session

class VerClasesInstructorView:
    def __init__(self, master):
        self.master = master
        self.master.title('Mis Clases Asignadas')
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Mis Clases Asignadas", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Crear el Treeview para mostrar las clases
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Actividad", "Turno", "Hora Inicio", "Hora Fin"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Actividad", text="Actividad")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Hora Inicio", text="Hora Inicio")
        self.tree.heading("Hora Fin", text="Hora Fin")
        self.tree.grid(row=1, column=0, columnspan=2)

        # Cargar las clases asignadas
        self.cargar_clases_asignadas()

        # Botón Volver
        tk.Button(self.frame, text="Volver", command=self.volver).grid(row=2, column=0, columnspan=2, pady=10)

    def cargar_clases_asignadas(self):
        # Obtener el CI del instructor actual
        ci_instructor = session.usuario_actual.get('ci_persona')

        # Obtener las clases asignadas al instructor
        clases = clase_controller.obtener_clases_por_instructor(ci_instructor)

        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar las clases en el Treeview
        for clase in clases:
            self.tree.insert("", "end", values=(
                clase.id,
                clase.actividad_nombre,
                clase.turno_descripcion,
                str(clase.hora_inicio),
                str(clase.hora_fin)
            ))

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
