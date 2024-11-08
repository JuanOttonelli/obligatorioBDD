# main_menu_view.py
import tkinter as tk
from src.views.actividad_view import ActividadView
from src.views.alumno_view import AlumnoView
from src.views.instructor_view import InstructorView

class MainMenuView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Menú Principal", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.frame, text="Gestionar Actividades", command=self.gestionar_actividades, width=20).pack(pady=5)
        tk.Button(self.frame, text="Gestionar Alumnos", command=self.gestionar_alumnos, width=20).pack(pady=5)
        tk.Button(self.frame, text="Gestionar Instructores", command=self.gestionar_instructores, width=20).pack(pady=5)
        tk.Button(self.frame, text="Salir", command=self.master.quit, width=20, bg="red", fg="white").pack(pady=10)

    def gestionar_actividades(self):
        self.frame.destroy()
        from src.views.actividad_view import ActividadView
        ActividadView(self.master)

    def gestionar_alumnos(self):
        self.frame.destroy()
        AlumnoView(self.master)

    def gestionar_instructores(self):
        self.frame.destroy()
        from src.views.instructor_view import InstructorView
        InstructorView(self.master)
