# src/views/ver_clases_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers import clase_controller
from src.views import session

class VerClasesView:
    def __init__(self, master):
        self.master = master
        self.master.title('Mis Clases')
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Mis Clases", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Crear el Treeview para mostrar las clases
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Actividad", "Instructor", "Turno", "Hora Inicio", "Hora Fin"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Actividad", text="Actividad")
        self.tree.heading("Instructor", text="Instructor")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Hora Inicio", text="Hora Inicio")
        self.tree.heading("Hora Fin", text="Hora Fin")
        self.tree.grid(row=1, column=0, columnspan=2)

        # Cargar las clases inscritas
        self.cargar_clases_inscritas()

        # Botón Volver
        tk.Button(self.frame, text="Volver", command=self.volver).grid(row=2, column=0, columnspan=2, pady=10)

    def cargar_clases_inscritas(self):
        # Obtener el CI del alumno actual
        ci_alumno = session.usuario_actual.get('ci_persona')

        # Obtener las clases en las que el alumno está inscrito
        clases = clase_controller.obtener_clases_inscritas_por_alumno(ci_alumno)

        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar las clases en el Treeview
        for clase in clases:
            instructor = f"{clase.nombre_instructor} {clase.apellido_instructor}"
            self.tree.insert("", "end", values=(
                clase.id,
                clase.actividad_nombre,
                instructor,
                clase.turno_descripcion,
                str(clase.hora_inicio),
                str(clase.hora_fin)
            ))

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
