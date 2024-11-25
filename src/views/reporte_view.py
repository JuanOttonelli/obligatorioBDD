# src/views/reporte_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from src.views import session
from src.controllers import reporte_controller


class ReporteView:
    def __init__(self, master):
        self.master = master
        tipo_usuario = session.usuario_actual.get('tipo_persona')
        if tipo_usuario != 1:
            messagebox.showerror("Acceso Denegado", "No tiene permisos para acceder a esta funcionalidad.")
            master.destroy()
            return

        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Sistema de Reportes", font=("Helvetica", 16)).pack(pady=10)

        # Botones para seleccionar el reporte
        tk.Button(self.frame, text="Actividades que más ingresos generan", command=self.ver_reporte_ingresos).pack(
            pady=5)
        tk.Button(self.frame, text="Actividades con más alumnos", command=self.ver_reporte_alumnos).pack(pady=5)
        tk.Button(self.frame, text="Turnos con más clases dictadas", command=self.ver_reporte_turnos).pack(pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def ver_reporte_ingresos(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Actividades que más ingresos generan")
        self.mostrar_reporte_ingresos(ventana)

    def mostrar_reporte_ingresos(self, ventana):
        actividades_ingresos = reporte_controller.obtener_actividades_mas_ingresos()

        tree = ttk.Treeview(ventana, columns=("Actividad", "Ingreso Clases", "Ingreso Equipos", "Total Ingresos"),
                            show="headings")
        tree.heading("Actividad", text="Actividad")
        tree.heading("Ingreso Clases", text="Ingreso Clases")
        tree.heading("Ingreso Equipos", text="Ingreso Equipos")
        tree.heading("Total Ingresos", text="Total Ingresos")

        tree.pack()

        for actividad in actividades_ingresos:
            tree.insert("", "end", values=(
                actividad['actividad'],
                actividad['ingreso_clases'],
                actividad['ingreso_equipos'],
                actividad['total_ingresos']
            ))

    def ver_reporte_alumnos(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Actividades con más alumnos")
        self.mostrar_reporte_alumnos(ventana)

    def mostrar_reporte_alumnos(self, ventana):
        actividades_alumnos = reporte_controller.obtener_actividades_con_mas_alumnos()

        tree = ttk.Treeview(ventana, columns=("Actividad", "Total Alumnos"), show="headings")
        tree.heading("Actividad", text="Actividad")
        tree.heading("Total Alumnos", text="Total Alumnos")

        tree.pack()

        for actividad in actividades_alumnos:
            tree.insert("", "end", values=(
                actividad['actividad'],
                actividad['total_alumnos']
            ))

    def ver_reporte_turnos(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Turnos con más clases dictadas")
        self.mostrar_reporte_turnos(ventana)

    def mostrar_reporte_turnos(self, ventana):
        turnos_clases = reporte_controller.obtener_turnos_con_mas_clases()

        tree = ttk.Treeview(ventana, columns=("Turno", "Total Clases"), show="headings")
        tree.heading("Turno", text="Turno")
        tree.heading("Total Clases", text="Total Clases")

        tree.pack()

        for turno in turnos_clases:
            tree.insert("", "end", values=(
                turno['turno'],
                turno['total_clases']
            ))

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
