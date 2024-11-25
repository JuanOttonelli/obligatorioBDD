# src/views/reporte_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from src.views import session
from src.controllers import reporte_controller
from src.views.main_menu_view import MainMenuView


class ReporteView:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Reportes")
        tipo_usuario = session.usuario_actual.get('tipo_persona')
        if tipo_usuario != 1:
            messagebox.showerror("Acceso Denegado", "No tiene permisos para acceder a esta funcionalidad.")
            master.destroy()
            return

        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Sistema de Reportes", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Lista de reportes disponibles
        self.reportes = [
            ("Actividades que más ingresos generan", self.mostrar_reporte_ingresos),
            ("Actividades con más alumnos", self.mostrar_reporte_alumnos),
            ("Turnos con más clases dictadas", self.mostrar_reporte_turnos),
        ]

        # Combobox para seleccionar el reporte
        tk.Label(self.frame, text="Seleccione un reporte:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.combo_reportes = ttk.Combobox(self.frame, values=[r[0] for r in self.reportes], state="readonly", width=40)
        self.combo_reportes.grid(row=1, column=1, padx=5, pady=5)
        self.combo_reportes.bind("<<ComboboxSelected>>", self.cargar_reporte)

        # Botón Volver
        tk.Button(self.frame, text="Volver", command=self.volver, width=15).grid(row=1, column=2, padx=5, pady=5)

        # Frame para mostrar el reporte
        self.reporte_frame = tk.Frame(self.frame)
        self.reporte_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def cargar_reporte(self, event):
        seleccion = self.combo_reportes.get()
        # Limpiar el frame del reporte
        for widget in self.reporte_frame.winfo_children():
            widget.destroy()

        if seleccion == self.reportes[0][0]:
            self.mostrar_reporte_ingresos()
        elif seleccion == self.reportes[1][0]:
            self.mostrar_reporte_alumnos()
        elif seleccion == self.reportes[2][0]:
            self.mostrar_reporte_turnos()

    def mostrar_reporte_ingresos(self):
        actividades_ingresos = reporte_controller.obtener_actividades_mas_ingresos()

        tree = ttk.Treeview(self.reporte_frame, columns=("Actividad", "Ingreso Clases", "Ingreso Equipos", "Total Ingresos"),
                            show="headings")
        tree.heading("Actividad", text="Actividad")
        tree.heading("Ingreso Clases", text="Ingreso Clases")
        tree.heading("Ingreso Equipos", text="Ingreso Equipos")
        tree.heading("Total Ingresos", text="Total Ingresos")

        tree.column("Actividad", width=200)
        tree.column("Ingreso Clases", width=120, anchor='center')
        tree.column("Ingreso Equipos", width=120, anchor='center')
        tree.column("Total Ingresos", width=120, anchor='center')

        tree.pack(fill='both', expand=True)

        for actividad in actividades_ingresos:
            tree.insert("", "end", values=(
                actividad['actividad'],
                f"${actividad['ingreso_clases']:.2f}",
                f"${actividad['ingreso_equipos']:.2f}",
                f"${actividad['total_ingresos']:.2f}"
            ))

    def mostrar_reporte_alumnos(self):
        actividades_alumnos = reporte_controller.obtener_actividades_con_mas_alumnos()

        tree = ttk.Treeview(self.reporte_frame, columns=("Actividad", "Total Alumnos"), show="headings")
        tree.heading("Actividad", text="Actividad")
        tree.heading("Total Alumnos", text="Total Alumnos")

        tree.column("Actividad", width=300)
        tree.column("Total Alumnos", width=150, anchor='center')

        tree.pack(fill='both', expand=True)

        for actividad in actividades_alumnos:
            tree.insert("", "end", values=(
                actividad['actividad'],
                actividad['total_alumnos']
            ))

    def mostrar_reporte_turnos(self):
        turnos_clases = reporte_controller.obtener_turnos_con_mas_clases()

        tree = ttk.Treeview(self.reporte_frame, columns=("Turno", "Total Clases"), show="headings")
        tree.heading("Turno", text="Turno")
        tree.heading("Total Clases", text="Total Clases")

        tree.column("Turno", width=300)
        tree.column("Total Clases", width=150, anchor='center')

        tree.pack(fill='both', expand=True)

        for turno in turnos_clases:
            tree.insert("", "end", values=(
                turno['turno'],
                turno['total_clases']
            ))

    def volver(self):
        self.frame.destroy()
        MainMenuView(self.master)
