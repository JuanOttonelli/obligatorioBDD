# src/views/equipo_alquiler_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers import equipo_alquiler_controller, actividad_controller
from src.models.equipo_alquiler import EquipoDeAlquiler
from src.views import session

class EquipoAlquilerView:
    def __init__(self, master):
        tipo_usuario = session.usuario_actual.get('tipo_persona')
        if tipo_usuario != 1:
            messagebox.showerror("Acceso Denegado", "No tiene permisos para acceder a esta funcionalidad.")
            master.destroy()
            return

        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Gestión de Equipos de Alquiler", font=("Helvetica", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Descripción", "Costo", "Actividad"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Actividad", text="Actividad")
        self.tree.pack()

        self.cargar_equipos()

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar Equipo", command=self.agregar_equipo).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Modificar Equipo", command=self.modificar_equipo).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Equipo", command=self.eliminar_equipo).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Volver", command=self.volver).grid(row=0, column=3, padx=5)

    def cargar_equipos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        equipos = equipo_alquiler_controller.obtener_equipos()
        for equipo in equipos:
            self.tree.insert("", "end", values=(equipo.id, equipo.descripcion, equipo.costo, equipo.nombre_actividad))

    def agregar_equipo(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Equipo de Alquiler")

        tk.Label(ventana, text="Descripción:").grid(row=0, column=0, padx=5, pady=5)
        entry_descripcion = tk.Entry(ventana)
        entry_descripcion.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Costo:").grid(row=1, column=0, padx=5, pady=5)
        entry_costo = tk.Entry(ventana)
        entry_costo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Actividad:").grid(row=2, column=0, padx=5, pady=5)
        actividades = actividad_controller.obtener_actividades()
        combo_actividades = ttk.Combobox(ventana, values=[f"{a.id} - {a.nombre}" for a in actividades])
        combo_actividades.grid(row=2, column=1, padx=5, pady=5)

        def guardar_equipo():
            descripcion = entry_descripcion.get()
            costo = entry_costo.get()
            seleccion_actividad = combo_actividades.get()
            if not descripcion or not costo or not seleccion_actividad:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return
            try:
                costo = float(costo)
            except ValueError:
                messagebox.showwarning("Advertencia", "El costo debe ser un número válido.")
                return
            id_actividad = int(seleccion_actividad.split(" - ")[0])
            equipo = EquipoDeAlquiler(descripcion=descripcion, costo=costo, id_actividad=id_actividad)
            exito = equipo_alquiler_controller.agregar_equipo(equipo)
            if exito:
                messagebox.showinfo("Éxito", "Equipo de alquiler agregado correctamente.")
                ventana.destroy()
                self.cargar_equipos()
            else:
                messagebox.showerror("Error", "No se pudo agregar el equipo de alquiler.")

        tk.Button(ventana, text="Guardar", command=guardar_equipo).grid(row=3, column=0, columnspan=2, pady=10)

    def modificar_equipo(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un equipo para modificar.")
            return
        item = self.tree.item(seleccion)
        valores = item['values']
        id_equipo = valores[0]

        ventana = tk.Toplevel(self.master)
        ventana.title("Modificar Equipo de Alquiler")

        tk.Label(ventana, text="Descripción:").grid(row=0, column=0, padx=5, pady=5)
        entry_descripcion = tk.Entry(ventana)
        entry_descripcion.insert(0, valores[1])
        entry_descripcion.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Costo:").grid(row=1, column=0, padx=5, pady=5)
        entry_costo = tk.Entry(ventana)
        entry_costo.insert(0, valores[2])
        entry_costo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Actividad:").grid(row=2, column=0, padx=5, pady=5)
        actividades = actividad_controller.obtener_actividades()
        combo_actividades = ttk.Combobox(ventana, values=[f"{a.id} - {a.nombre}" for a in actividades])
        combo_actividades.set(f"{valores[3]}")
        combo_actividades.grid(row=2, column=1, padx=5, pady=5)

        def actualizar_equipo():
            descripcion = entry_descripcion.get()
            costo = entry_costo.get()
            seleccion_actividad = combo_actividades.get()
            if not descripcion or not costo or not seleccion_actividad:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return
            try:
                costo = float(costo)
            except ValueError:
                messagebox.showwarning("Advertencia", "El costo debe ser un número válido.")
                return
            id_actividad = int(seleccion_actividad.split(" - ")[0])
            equipo = EquipoDeAlquiler(id=id_equipo, descripcion=descripcion, costo=costo, id_actividad=id_actividad)
            exito = equipo_alquiler_controller.modificar_equipo(equipo)
            if exito:
                messagebox.showinfo("Éxito", "Equipo de alquiler modificado correctamente.")
                ventana.destroy()
                self.cargar_equipos()
            else:
                messagebox.showerror("Error", "No se pudo modificar el equipo de alquiler.")

        tk.Button(ventana, text="Guardar", command=actualizar_equipo).grid(row=3, column=0, columnspan=2, pady=10)

    def eliminar_equipo(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un equipo para eliminar.")
            return
        item = self.tree.item(seleccion)
        id_equipo = item['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este equipo de alquiler?")
        if confirmar:
            exito = equipo_alquiler_controller.eliminar_equipo(id_equipo)
            if exito:
                messagebox.showinfo("Éxito", "Equipo de alquiler eliminado correctamente.")
                self.cargar_equipos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el equipo de alquiler.")

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
