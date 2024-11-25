# src/views/clase_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers import clase_controller, actividad_controller, turno_controller, instructor_controller, alumno_controller
from src.models.clase import Clase
from src.views import session

class ClaseView:
    def __init__(self, master):
        tipo_usuario = session.usuario_actual.get('tipo_persona')
        if tipo_usuario != 1:
            messagebox.showerror("Acceso Denegado", "No tiene permisos para acceder a esta funcionalidad.")
            master.destroy()
            return

        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Gestión de Clases", font=("Helvetica", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Instructor", "Actividad", "Turno", "Dictada"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Instructor", text="Instructor")
        self.tree.heading("Actividad", text="Actividad")
        self.tree.heading("Turno", text="Turno")
        self.tree.heading("Dictada", text="Dictada")
        self.tree.pack()

        self.cargar_clases()

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar Clase", command=self.agregar_clase).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Modificar Clase", command=self.modificar_clase).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Clase", command=self.eliminar_clase).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Gestionar Alumnos", command=self.gestionar_alumnos_clase).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Volver", command=self.volver).grid(row=0, column=4, padx=5)

    def cargar_clases(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        clases = clase_controller.obtener_clases()
        for clase in clases:
            instructor = f"{clase.nombre_instructor} {clase.apellido_instructor}"
            actividad = clase.actividad
            turno = clase.turno_descripcion
            dictada = "Sí" if clase.dictada else "No"
            self.tree.insert("", "end", values=(clase.id, instructor, actividad, turno, dictada))

    def agregar_clase(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Clase")

        tk.Label(ventana, text="Instructor:").grid(row=0, column=0, padx=5, pady=5)
        instructores = instructor_controller.obtener_instructores()
        combo_instructores = ttk.Combobox(ventana, values=[f"{i.ci} - {i.nombre} {i.apellido}" for i in instructores])
        combo_instructores.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Actividad:").grid(row=1, column=0, padx=5, pady=5)
        actividades = actividad_controller.obtener_actividades()
        combo_actividades = ttk.Combobox(ventana, values=[f"{a.id} - {a.descripcion}" for a in actividades])
        combo_actividades.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Turno:").grid(row=2, column=0, padx=5, pady=5)
        turnos = turno_controller.obtener_turnos()
        combo_turnos = ttk.Combobox(ventana, values=[f"{t.id} - {t.descripcion}" for t in turnos])
        combo_turnos.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Dictada:").grid(row=3, column=0, padx=5, pady=5)
        var_dictada = tk.BooleanVar()
        chk_dictada = tk.Checkbutton(ventana, variable=var_dictada)
        chk_dictada.grid(row=3, column=1, padx=5, pady=5)

        def guardar_clase():
            seleccion_instructor = combo_instructores.get()
            seleccion_actividad = combo_actividades.get()
            seleccion_turno = combo_turnos.get()
            dictada = var_dictada.get()

            if not seleccion_instructor or not seleccion_actividad or not seleccion_turno:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            ci_instructor = seleccion_instructor.split(" - ")[0]
            id_actividad = int(seleccion_actividad.split(" - ")[0])
            id_turno = int(seleccion_turno.split(" - ")[0])

            clase = Clase(ci_instructor=ci_instructor, id_actividad=id_actividad, id_turno=id_turno, dictada=dictada)
            exito = clase_controller.agregar_clase(clase)
            if exito:
                messagebox.showinfo("Éxito", "Clase agregada correctamente.")
                ventana.destroy()
                self.cargar_clases()
            else:
                messagebox.showerror("Error", "No se pudo agregar la clase.")

        tk.Button(ventana, text="Guardar", command=guardar_clase).grid(row=4, column=0, columnspan=2, pady=10)

    def modificar_clase(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una clase para modificar.")
            return
        item = self.tree.item(seleccion)
        valores = item['values']
        id_clase = valores[0]

        clase_actual = None
        clases = clase_controller.obtener_clases()
        for clase in clases:
            if clase.id == id_clase:
                clase_actual = clase
                break

        if not clase_actual:
            messagebox.showerror("Error", "No se encontró la clase seleccionada.")
            return

        ventana = tk.Toplevel(self.master)
        ventana.title("Modificar Clase")

        tk.Label(ventana, text="Instructor:").grid(row=0, column=0, padx=5, pady=5)
        instructores = instructor_controller.obtener_instructores()
        combo_instructores = ttk.Combobox(ventana, values=[f"{i.ci} - {i.nombre} {i.apellido}" for i in instructores])
        combo_instructores.set(f"{clase_actual.ci_instructor} - {clase_actual.nombre_instructor} {clase_actual.apellido_instructor}")
        combo_instructores.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Actividad:").grid(row=1, column=0, padx=5, pady=5)
        actividades = actividad_controller.obtener_actividades()
        combo_actividades = ttk.Combobox(ventana, values=[f"{a.id} - {a.descripcion}" for a in actividades])
        combo_actividades.set(f"{clase_actual.id_actividad} - {clase_actual.actividad}")
        combo_actividades.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Turno:").grid(row=2, column=0, padx=5, pady=5)
        turnos = turno_controller.obtener_turnos()
        combo_turnos = ttk.Combobox(ventana, values=[f"{t.id} - {t.descripcion}" for t in turnos])
        combo_turnos.set(f"{clase_actual.id_turno} - {clase_actual.turno_descripcion}")
        combo_turnos.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Dictada:").grid(row=3, column=0, padx=5, pady=5)
        var_dictada = tk.BooleanVar(value=clase_actual.dictada)
        chk_dictada = tk.Checkbutton(ventana, variable=var_dictada)
        chk_dictada.grid(row=3, column=1, padx=5, pady=5)

        def actualizar_clase():
            seleccion_instructor = combo_instructores.get()
            seleccion_actividad = combo_actividades.get()
            seleccion_turno = combo_turnos.get()
            dictada = var_dictada.get()

            if not seleccion_instructor or not seleccion_actividad or not seleccion_turno:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            ci_instructor = seleccion_instructor.split(" - ")[0]
            id_actividad = int(seleccion_actividad.split(" - ")[0])
            id_turno = int(seleccion_turno.split(" - ")[0])

            clase = Clase(id=id_clase, ci_instructor=ci_instructor, id_actividad=id_actividad, id_turno=id_turno, dictada=dictada)
            exito = clase_controller.actualizar_clase(clase)
            if exito:
                messagebox.showinfo("Éxito", "Clase modificada correctamente.")
                ventana.destroy()
                self.cargar_clases()
            else:
                messagebox.showerror("Error", "No se pudo modificar la clase.")

        tk.Button(ventana, text="Guardar", command=actualizar_clase).grid(row=4, column=0, columnspan=2, pady=10)

    def eliminar_clase(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una clase para eliminar.")
            return
        item = self.tree.item(seleccion)
        id_clase = item['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta clase?")
        if confirmar:
            exito = clase_controller.eliminar_clase(id_clase)
            if exito:
                messagebox.showinfo("Éxito", "Clase eliminada correctamente.")
                self.cargar_clases()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la clase.")

    def gestionar_alumnos_clase(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una clase para gestionar alumnos.")
            return
        item = self.tree.item(seleccion)
        id_clase = item['values'][0]
        ventana = tk.Toplevel(self.master)
        ventana.title("Gestionar Alumnos de la Clase")

        tk.Label(ventana, text="Alumnos Inscritos", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=2, pady=10)

        tree_alumnos = ttk.Treeview(ventana, columns=("CI", "Nombre"), show="headings")
        tree_alumnos.heading("CI", text="Cédula")
        tree_alumnos.heading("Nombre", text="Nombre")
        tree_alumnos.grid(row=1, column=0, columnspan=2)

        def cargar_alumnos():
            for item in tree_alumnos.get_children():
                tree_alumnos.delete(item)
            alumnos = clase_controller.obtener_alumnos_de_clase(id_clase)
            for alumno in alumnos:
                nombre_completo = f"{alumno['nombre']} {alumno['apellido']}"
                tree_alumnos.insert("", "end", values=(alumno['ci_alumno'], nombre_completo))

        cargar_alumnos()

        tk.Button(ventana, text="Agregar Alumno", command=lambda: self.agregar_alumno(id_clase, cargar_alumnos)).grid(row=2, column=0, padx=5, pady=10)
        tk.Button(ventana, text="Quitar Alumno", command=lambda: self.quitar_alumno(id_clase, tree_alumnos, cargar_alumnos)).grid(row=2, column=1, padx=5, pady=10)

    def agregar_alumno(self, id_clase, cargar_alumnos_callback):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Alumno a la Clase")

        tk.Label(ventana, text="Seleccione un alumno:").grid(row=0, column=0, padx=5, pady=5)
        alumnos = alumno_controller.obtener_alumnos()
        combo_alumnos = ttk.Combobox(ventana, values=[f"{a.ci} - {a.nombre} {a.apellido}" for a in alumnos])
        combo_alumnos.grid(row=0, column=1, padx=5, pady=5)

        def agregar():
            seleccion_alumno = combo_alumnos.get()
            if not seleccion_alumno:
                messagebox.showwarning("Advertencia", "Debe seleccionar un alumno.")
                return
            ci_alumno = seleccion_alumno.split(" - ")[0]
            exito = clase_controller.agregar_alumno_a_clase(id_clase, ci_alumno)
            if exito:
                messagebox.showinfo("Éxito", "Alumno agregado a la clase.")
                ventana.destroy()
                cargar_alumnos_callback()
            else:
                messagebox.showerror("Error", "No se pudo agregar el alumno a la clase.")

        tk.Button(ventana, text="Agregar", command=agregar).grid(row=1, column=0, columnspan=2, pady=10)

    def quitar_alumno(self, id_clase, tree_alumnos, cargar_alumnos_callback):
        seleccion = tree_alumnos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un alumno para quitar.")
            return
        item = tree_alumnos.item(seleccion)
        ci_alumno = item['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de quitar a este alumno de la clase?")
        if confirmar:
            exito = clase_controller.quitar_alumno_de_clase(id_clase, ci_alumno)
            if exito:
                messagebox.showinfo("Éxito", "Alumno quitado de la clase.")
                cargar_alumnos_callback()
            else:
                messagebox.showerror("Error", "No se pudo quitar al alumno de la clase.")

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
