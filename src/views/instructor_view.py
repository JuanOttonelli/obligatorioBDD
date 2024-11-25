# src/views/instructor_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers.instructor_controller import (
    obtener_instructores,
    agregar_instructor,
    actualizar_instructor,
    eliminar_instructor,
    obtener_agenda_instructor,
    obtener_instructor_por_ci,
)
from src.models.instructor import Instructor
from src.views.main_menu_view import MainMenuView


class InstructorView:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Instructores")
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Gestión de Instructores", font=("Helvetica", 16)).grid(
            row=0, column=0, columnspan=4, pady=10
        )

        # Tabla de instructores
        self.tree = ttk.Treeview(
            self.frame,
            columns=("CI", "Nombre", "Apellido", "Correo Electrónico"),
            show="headings",
        )
        self.tree.heading("CI", text="CI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Correo Electrónico", text="Correo Electrónico")

        self.tree.column("CI", width=100)
        self.tree.column("Nombre", width=100)
        self.tree.column("Apellido", width=100)
        self.tree.column("Correo Electrónico", width=200)

        self.tree.grid(row=1, column=0, columnspan=4, pady=10)

        # Botones
        tk.Button(
            self.frame, text="Agregar", command=self.abrir_formulario_agregar, width=15
        ).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(
            self.frame,
            text="Actualizar",
            command=self.abrir_formulario_actualizar,
            width=15,
        ).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(
            self.frame, text="Eliminar", command=self.eliminar_instructor, width=15
        ).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(
            self.frame,
            text="Ver Agenda",
            command=self.ver_agenda_instructor,
            width=15,
        ).grid(row=2, column=3, padx=5, pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver, width=15).grid(
            row=3, column=0, columnspan=4, pady=10
        )

        # Cargar instructores
        self.cargar_instructores()

    def cargar_instructores(self):
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener los instructores y cargarlos en la tabla
        instructores = obtener_instructores()
        for instructor in instructores:
            self.tree.insert(
                "",
                "end",
                values=(
                    instructor.ci,
                    instructor.nombre,
                    instructor.apellido,
                    instructor.correo_electronico,
                ),
            )

    def abrir_formulario_agregar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Instructor")

        labels = ["CI", "Nombre", "Apellido", "Correo Electrónico"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(
                row=idx, column=0, sticky=tk.E, padx=5, pady=5
            )
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        def guardar_instructor():
            datos = [entry.get() for entry in entries]
            if "" in datos:
                messagebox.showwarning(
                    "Advertencia", "Todos los campos son obligatorios.", parent=ventana
                )
                return
            instructor = Instructor(
                ci=datos[0],
                nombre=datos[1],
                apellido=datos[2],
                correo_electronico=datos[3],
            )

            exito, contraseña = agregar_instructor(instructor)
            if exito:
                messagebox.showinfo(
                    "Éxito",
                    f"Instructor agregado correctamente.\nContraseña generada: {contraseña}",
                    parent=ventana,
                )
                ventana.destroy()
                self.cargar_instructores()
            else:
                messagebox.showerror(
                    "Error", "No se pudo agregar el instructor.", parent=ventana
                )

        tk.Button(ventana, text="Guardar", command=guardar_instructor).grid(
            row=len(labels), column=0, columnspan=2, pady=10
        )

    def abrir_formulario_actualizar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Debe seleccionar un instructor para actualizar."
            )
            return

        item = self.tree.item(seleccion)
        instructor_ci = item["values"][0]

        ventana = tk.Toplevel(self.master)
        ventana.title("Actualizar Instructor")

        labels = ["Nombre", "Apellido", "Correo Electrónico"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(
                row=idx, column=0, sticky=tk.E, padx=5, pady=5
            )
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        # Cargar datos actuales
        instructor = obtener_instructor_por_ci(instructor_ci)
        if instructor:
            entries[0].insert(0, instructor.nombre)
            entries[1].insert(0, instructor.apellido)
            entries[2].insert(0, instructor.correo_electronico)
        else:
            messagebox.showerror(
                "Error",
                "No se pudo obtener la información del instructor.",
                parent=ventana,
            )
            ventana.destroy()
            return

        def actualizar_instructor_bd():
            datos = [entry.get() for entry in entries]
            if "" in datos:
                messagebox.showwarning(
                    "Advertencia", "Todos los campos son obligatorios.", parent=ventana
                )
                return

            instructor_actualizado = Instructor(
                ci=instructor_ci,
                nombre=datos[0],
                apellido=datos[1],
                correo_electronico=datos[2],
            )
            exito = actualizar_instructor(instructor_actualizado)
            if exito:
                messagebox.showinfo(
                    "Éxito", "Instructor actualizado correctamente.", parent=ventana
                )
                ventana.destroy()
                self.cargar_instructores()
            else:
                messagebox.showerror(
                    "Error", "No se pudo actualizar el instructor.", parent=ventana
                )

        tk.Button(ventana, text="Actualizar", command=actualizar_instructor_bd).grid(
            row=len(labels), column=0, columnspan=2, pady=10
        )

    def eliminar_instructor(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Debe seleccionar un instructor para eliminar."
            )
            return

        item = self.tree.item(seleccion)
        instructor_ci = item["values"][0]

        confirmacion = messagebox.askyesno(
            "Confirmación",
            f"¿Está seguro de que desea eliminar al instructor con CI {instructor_ci}?",
        )
        if confirmacion:
            exito = eliminar_instructor(instructor_ci)
            if exito:
                messagebox.showinfo("Éxito", "Instructor eliminado correctamente.")
                self.cargar_instructores()
            else:
                messagebox.showerror(
                    "Error", "No se pudo eliminar el instructor.\nPuede que tenga clases asignadas."
                )

    def ver_agenda_instructor(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Debe seleccionar un instructor para ver su agenda."
            )
            return

        item = self.tree.item(seleccion)
        instructor_ci = item["values"][0]

        agenda = obtener_agenda_instructor(instructor_ci)
        if not agenda:
            messagebox.showinfo(
                "Información", "No se encontraron clases para este instructor."
            )
            return

        ventana_agenda = tk.Toplevel(self.master)
        ventana_agenda.title(f"Agenda del Instructor {instructor_ci}")

        tree_agenda = ttk.Treeview(
            ventana_agenda,
            columns=("ID Clase", "Actividad", "Turno", "Hora Inicio", "Hora Fin"),
            show="headings",
        )
        tree_agenda.heading("ID Clase", text="ID Clase")
        tree_agenda.heading("Actividad", text="Actividad")
        tree_agenda.heading("Turno", text="Turno")
        tree_agenda.heading("Hora Inicio", text="Hora Inicio")
        tree_agenda.heading("Hora Fin", text="Hora Fin")

        tree_agenda.column("ID Clase", width=80)
        tree_agenda.column("Actividad", width=150)
        tree_agenda.column("Turno", width=100)
        tree_agenda.column("Hora Inicio", width=100)
        tree_agenda.column("Hora Fin", width=100)

        tree_agenda.pack(padx=10, pady=10)

        for clase in agenda:
            tree_agenda.insert(
                "",
                "end",
                values=(
                    clase["id"],
                    clase["actividad"],
                    clase["turno"],
                    clase["hora_inicio"],
                    clase["hora_fin"],
                ),
            )

    def volver(self):
        self.frame.destroy()
        MainMenuView(self.master)
