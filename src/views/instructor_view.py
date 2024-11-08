# src/views/instructor_view.py

import tkinter as tk
from tkinter import messagebox
from src.controllers.instructor_controller import obtener_instructores, agregar_instructor, actualizar_instructor, eliminar_instructor, obtener_agenda_instructor
from src.models.instructor import Instructor

class InstructorView:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Instructores")
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Gestión de Instructores", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.frame, text="Listar Instructores", command=self.listar_instructores, width=20).pack(pady=5)
        tk.Button(self.frame, text="Agregar Instructor", command=self.abrir_formulario_agregar, width=20).pack(pady=5)
        tk.Button(self.frame, text="Actualizar Instructor", command=self.abrir_formulario_actualizar, width=20).pack(pady=5)
        tk.Button(self.frame, text="Eliminar Instructor", command=self.eliminar_instructor, width=20).pack(pady=5)
        tk.Button(self.frame, text="Ver Agenda Instructor", command=self.ver_agenda_instructor, width=20).pack(pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver, width=20).pack(pady=10)

    def listar_instructores(self):
        instructores = obtener_instructores()
        ventana = tk.Toplevel(self.master)
        ventana.title("Lista de Instructores")
        text = tk.Text(ventana, width=80, height=20)
        text.pack()
        for instructor in instructores:
            text.insert(tk.END, f"CI: {instructor.ci}, Nombre: {instructor.nombre} {instructor.apellido}\n")

    def abrir_formulario_agregar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Instructor")

        labels = ["CI", "Nombre", "Apellido"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(row=idx, column=0, sticky=tk.E)
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1)
            entries.append(entry)

        def guardar_instructor():
            ci = entries[0].get()
            nombre = entries[1].get()
            apellido = entries[2].get()

            if not ci or not nombre or not apellido:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            instructor = Instructor(ci=ci, nombre=nombre, apellido=apellido)
            exito = agregar_instructor(instructor)
            if exito:
                messagebox.showinfo("Éxito", "Instructor agregado correctamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar el instructor.")

        tk.Button(ventana, text="Guardar", command=guardar_instructor).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def abrir_formulario_actualizar(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Actualizar Instructor")

        tk.Label(ventana, text="CI del Instructor a actualizar:").grid(row=0, column=0)
        entry_ci = tk.Entry(ventana)
        entry_ci.grid(row=0, column=1)

        def cargar_datos():
            ci_instructor = entry_ci.get()
            if not ci_instructor:
                messagebox.showwarning("Advertencia", "Debe ingresar el CI del instructor.")
                return

            instructores = obtener_instructores()
            instructor_encontrado = None
            for instructor in instructores:
                if instructor.ci == ci_instructor:
                    instructor_encontrado = instructor
                    break
            if instructor_encontrado is None:
                messagebox.showerror("Error", "Instructor no encontrado.")
                return

            labels = ["Nombre", "Apellido"]
            entries = []

            for idx, label_text in enumerate(labels):
                tk.Label(ventana, text=label_text + ":").grid(row=idx+1, column=0, sticky=tk.E)
                entry = tk.Entry(ventana)
                entry.grid(row=idx+1, column=1)
                entries.append(entry)

            entries[0].insert(0, instructor_encontrado.nombre)
            entries[1].insert(0, instructor_encontrado.apellido)

            def actualizar_instructor_bd():
                nombre = entries[0].get()
                apellido = entries[1].get()

                if not nombre or not apellido:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                instructor_actualizado = Instructor(ci=ci_instructor, nombre=nombre, apellido=apellido)
                exito = actualizar_instructor(instructor_actualizado)
                if exito:
                    messagebox.showinfo("Éxito", "Instructor actualizado correctamente.")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el instructor.")

            tk.Button(ventana, text="Actualizar", command=actualizar_instructor_bd).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Cargar Datos", command=cargar_datos).grid(row=0, column=2, padx=5)

    def eliminar_instructor(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Eliminar Instructor")

        tk.Label(ventana, text="CI del Instructor a eliminar:").grid(row=0, column=0)
        entry_ci = tk.Entry(ventana)
        entry_ci.grid(row=0, column=1)

        def confirmar_eliminacion():
            ci_instructor = entry_ci.get()
            if not ci_instructor:
                messagebox.showwarning("Advertencia", "Debe ingresar el CI del instructor.")
                return

            confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este instructor?")
            if confirmacion:
                exito = eliminar_instructor(ci_instructor)
                if exito:
                    messagebox.showinfo("Éxito", "Instructor eliminado correctamente.")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el instructor.")

        tk.Button(ventana, text="Eliminar", command=confirmar_eliminacion).grid(row=1, column=0, columnspan=2, pady=10)

    def ver_agenda_instructor(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Ver Agenda del Instructor")

        tk.Label(ventana, text="CI del Instructor:").grid(row=0, column=0)
        entry_ci = tk.Entry(ventana)
        entry_ci.grid(row=0, column=1)

        def mostrar_agenda():
            ci_instructor = entry_ci.get()
            if not ci_instructor:
                messagebox.showwarning("Advertencia", "Debe ingresar el CI del instructor.")
                return

            agenda = obtener_agenda_instructor(ci_instructor)
            if not agenda:
                messagebox.showinfo("Información", "No se encontraron clases para este instructor.")
                return

            ventana_agenda = tk.Toplevel(self.master)
            ventana_agenda.title(f"Agenda del Instructor {ci_instructor}")
            text = tk.Text(ventana_agenda, width=80, height=20)
            text.pack()
            for clase in agenda:
                text.insert(tk.END, f"ID Clase: {clase['id']}, Actividad: {clase['actividad']}, Hora Inicio: {clase['hora_inicio']}, Hora Fin: {clase['hora_fin']}\n")

        tk.Button(ventana, text="Mostrar Agenda", command=mostrar_agenda).grid(row=0, column=2, padx=5)

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
