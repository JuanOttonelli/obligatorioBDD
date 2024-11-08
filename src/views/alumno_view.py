# alumno_view.py
import tkinter as tk
from tkinter import messagebox
from src.controllers.alumno_controller import obtener_alumnos, agregar_alumno, eliminar_alumno
from src.models.alumno import Alumno

class AlumnoView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Gestión de Alumnos", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.frame, text="Listar Alumnos", command=self.listar_alumnos, width=20).pack(pady=5)
        tk.Button(self.frame, text="Agregar Alumno", command=self.abrir_formulario_agregar, width=20).pack(pady=5)
        tk.Button(self.frame, text="Eliminar Alumno", command=self.eliminar_alumno, width=20).pack(pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver, width=20).pack(pady=5)

    def listar_alumnos(self):
        alumnos = obtener_alumnos()
        ventana = tk.Toplevel()
        ventana.title("Lista de Alumnos")
        text = tk.Text(ventana, width=80, height=20)
        text.pack()
        for alumno in alumnos:
            text.insert(tk.END, f"CI: {alumno.ci}, Nombre: {alumno.nombre} {alumno.apellido}, Email: {alumno.correo_electronico}\n")

    def abrir_formulario_agregar(self):
        ventana = tk.Toplevel()
        ventana.title("Agregar Alumno")

        labels = ["CI", "Nombre", "Apellido", "Fecha de Nacimiento (YYYY-MM-DD)", "Teléfono", "Correo Electrónico"]
        entries = []

        for idx, label_text in enumerate(labels):
            tk.Label(ventana, text=label_text + ":").grid(row=idx, column=0, sticky=tk.E)
            entry = tk.Entry(ventana)
            entry.grid(row=idx, column=1)
            entries.append(entry)

        def guardar_alumno():
            datos = [entry.get() for entry in entries]
            if "" in datos:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return
            alumno = Alumno(*datos)
            agregar_alumno(alumno)
            messagebox.showinfo("Éxito", "Alumno agregado correctamente.")
            ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar_alumno).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def eliminar_alumno(self):
        ventana = tk.Toplevel()
        ventana.title("Eliminar Alumno")

        tk.Label(ventana, text="CI del Alumno a eliminar:").grid(row=0, column=0)
        entry_ci = tk.Entry(ventana)
        entry_ci.grid(row=0, column=1)

        def confirmar_eliminacion():
            ci = entry_ci.get()
            if not ci:
                messagebox.showwarning("Advertencia", "Debe ingresar el CI del alumno.")
                return
            eliminar_alumno(ci)
            messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
            ventana.destroy()

        tk.Button(ventana, text="Eliminar", command=confirmar_eliminacion).grid(row=1, column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
