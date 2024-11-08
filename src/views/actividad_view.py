# src/views/actividad_view.py

import tkinter as tk
from tkinter import messagebox
from src.controllers.actividad_controller import obtener_actividades, agregar_actividad, actualizar_actividad, eliminar_actividad
from src.models.actividad import Actividad

class ActividadView:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Actividades")
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Gestión de Actividades", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.frame, text="Listar Actividades", command=self.listar_actividades, width=20).pack(pady=5)
        tk.Button(self.frame, text="Agregar Actividad", command=self.abrir_formulario_agregar, width=20).pack(pady=5)
        tk.Button(self.frame, text="Actualizar Actividad", command=self.abrir_formulario_actualizar, width=20).pack(pady=5)
        tk.Button(self.frame, text="Eliminar Actividad", command=self.eliminar_actividad, width=20).pack(pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver, width=20).pack(pady=10)

    def listar_actividades(self):
        actividades = obtener_actividades()
        ventana = tk.Toplevel(self.master)
        ventana.title("Lista de Actividades")
        text = tk.Text(ventana, width=80, height=20)
        text.pack()
        for actividad in actividades:
            text.insert(tk.END, f"ID: {actividad.id}, Descripción: {actividad.descripcion}, Costo: {actividad.costo}, Restricción de Edad: {actividad.restriccion_edad}\n")

    def abrir_formulario_agregar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Actividad")

        labels = ["Descripción", "Costo", "Restricción de Edad"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(row=idx, column=0, sticky=tk.E)
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1)
            entries.append(entry)

        def guardar_actividad():
            descripcion = entries[0].get()
            costo = entries[1].get()
            restriccion_edad = entries[2].get()

            if not descripcion or not costo or not restriccion_edad:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return
            try:
                costo = float(costo)
                restriccion_edad = int(restriccion_edad)
            except ValueError:
                messagebox.showwarning("Advertencia", "El costo debe ser un número y la restricción de edad un entero.")
                return

            actividad = Actividad(id=None, descripcion=descripcion, costo=costo, restriccion_edad=restriccion_edad)
            exito = agregar_actividad(actividad)
            if exito:
                messagebox.showinfo("Éxito", "Actividad agregada correctamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar la actividad.")

        tk.Button(ventana, text="Guardar", command=guardar_actividad).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def abrir_formulario_actualizar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Actualizar Actividad")

        tk.Label(ventana, text="ID de la Actividad a actualizar:").grid(row=0, column=0)
        entry_id = tk.Entry(ventana)
        entry_id.grid(row=0, column=1)

        def cargar_datos():
            id_actividad = entry_id.get()
            if not id_actividad:
                messagebox.showwarning("Advertencia", "Debe ingresar el ID de la actividad.")
                return
            try:
                id_actividad = int(id_actividad)
            except ValueError:
                messagebox.showwarning("Advertencia", "El ID debe ser un número entero.")
                return

            actividades = obtener_actividades()
            actividad_encontrada = None
            for actividad in actividades:
                if actividad.id == id_actividad:
                    actividad_encontrada = actividad
                    break
            if actividad_encontrada is None:
                messagebox.showerror("Error", "Actividad no encontrada.")
                return

            labels = ["Descripción", "Costo", "Restricción de Edad"]
            entries = []

            for idx, label_text in enumerate(labels):
                tk.Label(ventana, text=label_text + ":").grid(row=idx+1, column=0, sticky=tk.E)
                entry = tk.Entry(ventana)
                entry.grid(row=idx+1, column=1)
                entries.append(entry)

            entries[0].insert(0, actividad_encontrada.descripcion)
            entries[1].insert(0, str(actividad_encontrada.costo))
            entries[2].insert(0, str(actividad_encontrada.restriccion_edad))

            def actualizar_actividad_bd():
                descripcion = entries[0].get()
                costo = entries[1].get()
                restriccion_edad = entries[2].get()

                if not descripcion or not costo or not restriccion_edad:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return
                try:
                    costo = float(costo)
                    restriccion_edad = int(restriccion_edad)
                except ValueError:
                    messagebox.showwarning("Advertencia", "El costo debe ser un número y la restricción de edad un entero.")
                    return

                actividad_actualizada = Actividad(id=id_actividad, descripcion=descripcion, costo=costo, restriccion_edad=restriccion_edad)
                exito = actualizar_actividad(actividad_actualizada)
                if exito:
                    messagebox.showinfo("Éxito", "Actividad actualizada correctamente.")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la actividad.")

            tk.Button(ventana, text="Actualizar", command=actualizar_actividad_bd).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Cargar Datos", command=cargar_datos).grid(row=0, column=2, padx=5)

    def eliminar_actividad(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Eliminar Actividad")

        tk.Label(ventana, text="ID de la Actividad a eliminar:").grid(row=0, column=0)
        entry_id = tk.Entry(ventana)
        entry_id.grid(row=0, column=1)

        def confirmar_eliminacion():
            id_actividad = entry_id.get()
            if not id_actividad:
                messagebox.showwarning("Advertencia", "Debe ingresar el ID de la actividad.")
                return
            try:
                id_actividad = int(id_actividad)
            except ValueError:
                messagebox.showwarning("Advertencia", "El ID debe ser un número entero.")
                return

            confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar esta actividad?")
            if confirmacion:
                exito = eliminar_actividad(id_actividad)
                if exito:
                    messagebox.showinfo("Éxito", "Actividad eliminada correctamente.")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la actividad.")

        tk.Button(ventana, text="Eliminar", command=confirmar_eliminacion).grid(row=1, column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
