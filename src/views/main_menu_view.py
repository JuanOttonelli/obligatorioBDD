# src/views/main_menu_view.py

import tkinter as tk
from tkinter import messagebox
from src.views import session  # Importamos el módulo session
from src.views.login_view import LoginView

class MainMenuView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Menú Principal", font=("Helvetica", 16)).pack(pady=10)

        tipo_usuario = session.usuario_actual.get('tipo_persona')
        if tipo_usuario == 1:
            tk.Button(self.frame, text="Gestionar Actividades", command=self.gestionar_actividades, width=20).pack(pady=5)
            tk.Button(self.frame, text="Gestionar Alumnos", command=self.gestionar_alumnos, width=20).pack(pady=5)
            tk.Button(self.frame, text="Gestionar Instructores", command=self.gestionar_instructores, width=20).pack(pady=5)
            tk.Button(self.frame, text="Gestionar Clases", command=self.gestionar_clases, width=20).pack(pady=5)
            tk.Button(self.frame, text="Gestionar Turnos", command=self.gestionar_turnos, width=20).pack(pady=5)
            tk.Button(self.frame, text="Gestionar Equipos de Alquiler", command=self.gestionar_equipos_alquiler, width=20).pack(pady=5)  # Nueva opción
            tk.Button(self.frame, text="Ver Reportes", command=self.ver_reportes, width=20).pack(pady=5)
        elif tipo_usuario == 2:
            tk.Button(self.frame, text="Ver Agenda", command=self.ver_agenda, width=20).pack(pady=5)
        elif tipo_usuario == 3:
            tk.Button(self.frame, text="Ver Clases", command=self.ver_clases, width=20).pack(pady=5)
            tk.Button(self.frame, text="Inscribirse en Clase", command=self.inscribirse_clase, width=20).pack(pady=5)
        else:
            print(tipo_usuario)
            messagebox.showerror("Error", "Tipo de usuario no reconocido.")
            self.master.quit()
            return

        # Agregamos el botón de Cerrar Sesión
        tk.Button(self.frame, text="Cerrar Sesión", command=self.cerrar_sesion, width=20, bg="red", fg="white").pack(pady=10)

    # Implementa las funciones correspondientes a cada botón
    def gestionar_actividades(self):
        self.frame.destroy()
        from src.views.actividad_view import ActividadView
        ActividadView(self.master)

    def gestionar_alumnos(self):
        self.frame.destroy()
        from src.views.alumno_view import AlumnoView
        AlumnoView(self.master)

    def gestionar_instructores(self):
        self.frame.destroy()
        from src.views.instructor_view import InstructorView
        InstructorView(self.master)

    def gestionar_clases(self):
        self.frame.destroy()
        from src.views.clase_view import ClaseView
        ClaseView(self.master)

    def gestionar_turnos(self):
        self.frame.destroy()
        from src.views.turno_view import TurnoView
        TurnoView(self.master)

    def ver_agenda(self):
        self.frame.destroy()
        from src.views.ver_clases_instructor_view import VerClasesInstructorView
        VerClasesInstructorView(self.master)


    def ver_clases(self):
        self.frame.destroy()
        from src.views.ver_clases_view import VerClasesView
        VerClasesView(self.master)

    def inscribirse_clase(self):
        self.frame.destroy()
        from src.views.inscripcion_clase_view import InscripcionClaseView
        InscripcionClaseView(self.master)

    def gestionar_equipos_alquiler(self):
        self.frame.destroy()
        from src.views.equipo_alquiler_view import EquipoAlquilerView
        EquipoAlquilerView(self.master)

    def ver_reportes(self):
        self.frame.destroy()
        from src.views.reporte_view import ReporteView
        ReporteView(self.master)

    def cerrar_sesion(self):
        # Limpiamos usuario_actual a través del módulo session
        session.usuario_actual.clear()
        # Destruir el frame actual
        self.frame.destroy()
        # Volver a mostrar la pantalla de inicio de sesión
        LoginView(self.master)
