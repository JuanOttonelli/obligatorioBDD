# src/views/actividad_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers.actividad_controller import obtener_actividades, agregar_actividad, actualizar_actividad, \
    eliminar_actividad, obtener_actividad_por_id
from src.models.actividad import Actividad
from src.views.main_menu_view import MainMenuView

class ActividadView:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Actividades")
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Gestión de Actividades", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Tabla de actividades
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Descripción", "Costo", "Restricción de Edad"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Restricción de Edad", text="Restricción de Edad")

        self.tree.column("ID", width=50)
        self.tree.column("Descripción", width=200)
        self.tree.column("Costo", width=100)
        self.tree.column("Restricción de Edad", width=150)

        self.tree.grid(row=1, column=0, columnspan=4, pady=10)

        # Botones
        tk.Button(self.frame, text="Agregar", command=self.abrir_formulario_agregar, width=15).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Actualizar", command=self.abrir_formulario_actualizar, width=15).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Eliminar", command=self.eliminar_actividad, width=15).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver, width=15).grid(row=2, column=3, padx=5, pady=5)

        # Cargar actividades
        self.cargar_actividades()

    def cargar_actividades(self):
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener las actividades y cargarlas en la tabla
        actividades = obtener_actividades()
        for actividad in actividades:
            self.tree.insert("", "end", values=(actividad.id, actividad.descripcion, actividad.costo, actividad.restriccion_edad))

    def abrir_formulario_agregar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Actividad")

        labels = ["Descripción", "Costo", "Restricción de Edad"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(row=idx, column=0, sticky=tk.E, padx=5, pady=5)
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        def guardar_actividad():
            descripcion = entries[0].get()
            costo = entries[1].get()
            restriccion_edad = entries[2].get()

            if not descripcion or not costo or not restriccion_edad:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.", parent=ventana)
                return
            try:
                costo = float(costo)
                restriccion_edad = int(restriccion_edad)
            except ValueError:
                messagebox.showwarning("Advertencia", "El costo debe ser un número y la restricción de edad un entero.", parent=ventana)
                return

            actividad = Actividad(id=None, descripcion=descripcion, costo=costo, restriccion_edad=restriccion_edad)
            exito = agregar_actividad(actividad)
            if exito:
                messagebox.showinfo("Éxito", "Actividad agregada correctamente.", parent=ventana)
                ventana.destroy()
                self.cargar_actividades()
            else:
                messagebox.showerror("Error", "No se pudo agregar la actividad.", parent=ventana)

        tk.Button(ventana, text="Guardar", command=guardar_actividad).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def abrir_formulario_actualizar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar una actividad para actualizar.")
            return

        item = self.tree.item(seleccion)
        actividad_id = item['values'][0]

        ventana = tk.Toplevel(self.master)
        ventana.title("Actualizar Actividad")

        labels = ["Descripción", "Costo", "Restricción de Edad"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(row=idx, column=0, sticky=tk.E, padx=5, pady=5)
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        # Cargar datos actuales
        actividad = obtener_actividad_por_id(actividad_id)
        if actividad:
            entries[0].insert(0, actividad.descripcion)
            entries[1].insert(0, str(actividad.costo))
            entries[2].insert(0, str(actividad.restriccion_edad))
        else:
            messagebox.showerror("Error", "No se pudo obtener la información de la actividad.", parent=ventana)
            ventana.destroy()
            return

        def actualizar_actividad_bd():
            descripcion = entries[0].get()
            costo = entries[1].get()
            restriccion_edad = entries[2].get()

            if not descripcion or not costo or not restriccion_edad:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.", parent=ventana)
                return
            try:
                costo = float(costo)
                restriccion_edad = int(restriccion_edad)
            except ValueError:
                messagebox.showwarning("Advertencia", "El costo debe ser un número y la restricción de edad un entero.", parent=ventana)
                return

            actividad_actualizada = Actividad(id=actividad_id, descripcion=descripcion, costo=costo, restriccion_edad=restriccion_edad)
            exito = actualizar_actividad(actividad_actualizada)
            if exito:
                messagebox.showinfo("Éxito", "Actividad actualizada correctamente.", parent=ventana)
                ventana.destroy()
                self.cargar_actividades()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la actividad.", parent=ventana)

        tk.Button(ventana, text="Actualizar", command=actualizar_actividad_bd).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def eliminar_actividad(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar una actividad para eliminar.")
            return

        item = self.tree.item(seleccion)
        actividad_id = item['values'][0]

        confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar esta actividad?")
        if confirmacion:
            exito = eliminar_actividad(actividad_id)
            if exito:
                messagebox.showinfo("Éxito", "Actividad eliminada correctamente.")
                self.cargar_actividades()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la actividad.")

    def volver(self):
        self.frame.destroy()
        MainMenuView(self.master)
