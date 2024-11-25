# src/views/inscripcion_clase_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers import clase_controller, equipo_alquiler_controller, alquiler_controller
from src.models.alquiler import Alquiler
from src.views import session
from src.views.main_menu_view import MainMenuView

class InscripcionClaseView:
    def __init__(self, master):
        self.master = master
        #self.ventana = tk.Toplevel(self.master)
        #self.ventana.title("Inscribirse en Clase")
        self.master.title('Inscripcion Clase')
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        ci_alumno = session.usuario_actual.get('ci_persona')
        clases = clase_controller.obtener_clases_disponibles(ci_alumno)

        tk.Label(self.frame, text="Seleccione una clase:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_clases = ttk.Combobox(self.frame, values=[f"{c.id} - {c.actividad_nombre} - {c.turno_descripcion}" for c in clases])
        self.combo_clases.grid(row=0, column=1, padx=5, pady=5)
        self.combo_clases.bind("<<ComboboxSelected>>", self.cargar_equipos)

        tk.Label(self.frame, text="Seleccione equipos para alquilar (opcional):").grid(row=1, column=0, padx=5, pady=5)
        self.lista_equipamientos = tk.Listbox(self.frame, selectmode=tk.MULTIPLE)
        self.lista_equipamientos.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self.frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Confirmar Inscripción", command=self.confirmar_inscripcion).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Volver", command=self.volver).grid(row=0, column=1, padx=5)

    def cargar_equipos(self, event):
        seleccion_clase = self.combo_clases.get()
        if seleccion_clase:
            clase_id = int(seleccion_clase.split(" - ")[0])
            clase = clase_controller.obtener_clase_por_id(clase_id)
            id_actividad = clase.id_actividad
            equipos = equipo_alquiler_controller.obtener_equipos_por_actividad(id_actividad)
            self.lista_equipamientos.delete(0, tk.END)
            for equipo in equipos:
                self.lista_equipamientos.insert(tk.END, f"{equipo.id} - {equipo.descripcion} - ${equipo.costo}")

    def confirmar_inscripcion(self):
        seleccion_clase = self.combo_clases.get()
        if not seleccion_clase:
            messagebox.showwarning("Advertencia", "Debe seleccionar una clase.")
            return
        clase_id = int(seleccion_clase.split(" - ")[0])
        indices_equipamientos = self.lista_equipamientos.curselection()
        equipos_seleccionados = [self.lista_equipamientos.get(i) for i in indices_equipamientos]
        equipos_ids = [int(e.split(" - ")[0]) for e in equipos_seleccionados]

        # Registrar inscripción en la clase
        alumno_ci = session.usuario_actual.get('ci_persona')
        exito = clase_controller.inscribir_alumno_en_clase(clase_id, alumno_ci)
        if not exito:
            messagebox.showerror("Error", "No se pudo inscribir en la clase. Es posible que ya esté inscrito en otra clase en el mismo turno.")
            return

        # Registrar alquileres
        for equipo_id in equipos_ids:
            alquiler = Alquiler(alumno_ci=alumno_ci, clase_id=clase_id, equipo_id_alquiler=equipo_id)
            alquiler_controller.registrar_alquiler(alquiler)

        # Obtener los equipos seleccionados
        equipos = equipo_alquiler_controller.obtener_equipos_por_ids(equipos_ids)
        # Calcular el costo total
        costo_clase = clase_controller.obtener_costo_clase(clase_id)
        costo_equipos = sum(e.costo for e in equipos)
        costo_total = costo_clase + costo_equipos

        messagebox.showinfo("Éxito", f"Inscripción completada.\nCosto total: ${costo_total}")
        self.frame.destroy()
        MainMenuView(self.master)

    def volver(self):
        self.frame.destroy()

        MainMenuView(self.master)