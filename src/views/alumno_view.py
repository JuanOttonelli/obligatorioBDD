# src/views/alumno_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers.alumno_controller import obtener_alumnos, agregar_alumno, actualizar_alumno, eliminar_alumno, obtener_alumno_por_ci
from src.models.alumno import Alumno
from src.views.main_menu_view import MainMenuView

class AlumnoView:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Alumnos")
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Gestión de Alumnos", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Tabla de alumnos
        self.tree = ttk.Treeview(self.frame, columns=("CI", "Nombre", "Apellido", "Fecha Nacimiento", "Teléfono", "Correo"), show="headings")
        self.tree.heading("CI", text="CI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Fecha Nacimiento", text="Fecha Nacimiento")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")

        self.tree.column("CI", width=100)
        self.tree.column("Nombre", width=100)
        self.tree.column("Apellido", width=100)
        self.tree.column("Fecha Nacimiento", width=120)
        self.tree.column("Teléfono", width=100)
        self.tree.column("Correo", width=150)

        self.tree.grid(row=1, column=0, columnspan=4, pady=10)

        # Botones
        tk.Button(self.frame, text="Agregar", command=self.abrir_formulario_agregar, width=15).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Actualizar", command=self.abrir_formulario_actualizar, width=15).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Eliminar", command=self.eliminar_alumno, width=15).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver, width=15).grid(row=2, column=3, padx=5, pady=5)

        # Cargar alumnos
        self.cargar_alumnos()

    def cargar_alumnos(self):
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener los alumnos y cargarlos en la tabla
        alumnos = obtener_alumnos()
        for alumno in alumnos:
            self.tree.insert("", "end", values=(alumno.ci, alumno.nombre, alumno.apellido, alumno.fecha_nacimiento, alumno.telefono, alumno.correo_electronico))

    def abrir_formulario_agregar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Alumno")

        labels = ["CI", "Nombre", "Apellido", "Fecha de Nacimiento (YYYY-MM-DD)", "Teléfono", "Correo Electrónico"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(row=idx, column=0, sticky=tk.E, padx=5, pady=5)
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        def guardar_alumno():
            datos = [entry.get() for entry in entries]
            if "" in datos:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.", parent=ventana)
                return
            alumno = Alumno(ci=datos[0], nombre=datos[1], apellido=datos[2], fecha_nacimiento=datos[3], telefono=datos[4], correo_electronico=datos[5])
            exito, contraseña = agregar_alumno(alumno)
            if exito:
                messagebox.showinfo("Éxito", f"Alumno agregado correctamente.\nContraseña generada: {contraseña}", parent=ventana)
                ventana.destroy()
                self.cargar_alumnos()
            else:
                messagebox.showerror("Error", "No se pudo agregar el alumno.", parent=ventana)

        tk.Button(ventana, text="Guardar", command=guardar_alumno).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def abrir_formulario_actualizar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un alumno para actualizar.")
            return

        item = self.tree.item(seleccion)
        alumno_ci = item['values'][0]

        ventana = tk.Toplevel(self.master)
        ventana.title("Actualizar Alumno")

        labels = ["Nombre", "Apellido", "Fecha de Nacimiento (YYYY-MM-DD)", "Teléfono", "Correo Electrónico"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(row=idx, column=0, sticky=tk.E, padx=5, pady=5)
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        # Cargar datos actuales
        alumno = obtener_alumno_por_ci(alumno_ci)
        if alumno:
            entries[0].insert(0, alumno.nombre)
            entries[1].insert(0, alumno.apellido)
            entries[2].insert(0, alumno.fecha_nacimiento)
            entries[3].insert(0, alumno.telefono)
            entries[4].insert(0, alumno.correo_electronico)
        else:
            messagebox.showerror("Error", "No se pudo obtener la información del alumno.", parent=ventana)
            ventana.destroy()
            return

        def actualizar_alumno_bd():
            datos = [entry.get() for entry in entries]
            if "" in datos:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.", parent=ventana)
                return

            alumno_actualizado = Alumno(ci=alumno_ci, nombre=datos[0], apellido=datos[1], fecha_nacimiento=datos[2], telefono=datos[3], correo_electronico=datos[4])
            exito = actualizar_alumno(alumno_actualizado)
            if exito:
                messagebox.showinfo("Éxito", "Alumno actualizado correctamente.", parent=ventana)
                ventana.destroy()
                self.cargar_alumnos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el alumno.", parent=ventana)

        tk.Button(ventana, text="Actualizar", command=actualizar_alumno_bd).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def eliminar_alumno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un alumno para eliminar.")
            return

        item = self.tree.item(seleccion)
        alumno_ci = item['values'][0]

        confirmacion = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar al alumno con CI {alumno_ci}?")
        if confirmacion:
            exito = eliminar_alumno(alumno_ci)
            if exito:
                messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
                self.cargar_alumnos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el alumno.")

    def volver(self):
        self.frame.destroy()
        MainMenuView(self.master)
