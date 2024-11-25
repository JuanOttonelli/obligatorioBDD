# src/views/turno_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers import turno_controller
from src.models.turno import Turno
from src.views import session

class TurnoView:
    def __init__(self, master):
        tipo_usuario = session.usuario_actual.get('tipo_persona')
        if tipo_usuario != 1:
            messagebox.showerror("Acceso Denegado", "No tiene permisos para acceder a esta funcionalidad.")
            master.destroy()
            return

        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Gestión de Turnos", font=("Helvetica", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Descripción", "Hora Inicio", "Hora Fin"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Hora Inicio", text="Hora Inicio")
        self.tree.heading("Hora Fin", text="Hora Fin")
        self.tree.pack()

        self.cargar_turnos()

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar Turno", command=self.agregar_turno).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Modificar Turno", command=self.modificar_turno).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Turno", command=self.eliminar_turno).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Volver", command=self.volver).grid(row=0, column=3, padx=5)

    def cargar_turnos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        turnos = turno_controller.obtener_turnos()
        for turno in turnos:
            self.tree.insert("", "end", values=(turno.id, turno.descripcion, turno.hora_inicio, turno.hora_fin))

    def agregar_turno(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Turno")

        tk.Label(ventana, text="Descripción:").grid(row=0, column=0, padx=5, pady=5)
        entry_descripcion = tk.Entry(ventana)
        entry_descripcion.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Hora Inicio (HH:MM):").grid(row=1, column=0, padx=5, pady=5)
        entry_hora_inicio = tk.Entry(ventana)
        entry_hora_inicio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Hora Fin (HH:MM):").grid(row=2, column=0, padx=5, pady=5)
        entry_hora_fin = tk.Entry(ventana)
        entry_hora_fin.grid(row=2, column=1, padx=5, pady=5)

        def guardar_turno():
            descripcion = entry_descripcion.get()
            hora_inicio = entry_hora_inicio.get()
            hora_fin = entry_hora_fin.get()
            turno = Turno(descripcion=descripcion, hora_inicio=hora_inicio, hora_fin=hora_fin)
            exito = turno_controller.agregar_turno(turno)
            if exito:
                messagebox.showinfo("Éxito", "Turno agregado correctamente.")
                ventana.destroy()
                self.cargar_turnos()
            else:
                messagebox.showerror("Error", "No se pudo agregar el turno.")

        tk.Button(ventana, text="Guardar", command=guardar_turno).grid(row=3, column=0, columnspan=2, pady=10)

    def modificar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un turno para modificar.")
            return
        item = self.tree.item(seleccion)
        valores = item['values']
        id_turno = valores[0]

        ventana = tk.Toplevel(self.master)
        ventana.title("Modificar Turno")

        tk.Label(ventana, text="Descripción:").grid(row=0, column=0, padx=5, pady=5)
        entry_descripcion = tk.Entry(ventana)
        entry_descripcion.insert(0, valores[1])
        entry_descripcion.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Hora Inicio (HH:MM):").grid(row=1, column=0, padx=5, pady=5)
        entry_hora_inicio = tk.Entry(ventana)
        entry_hora_inicio.insert(0, valores[2])
        entry_hora_inicio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Hora Fin (HH:MM):").grid(row=2, column=0, padx=5, pady=5)
        entry_hora_fin = tk.Entry(ventana)
        entry_hora_fin.insert(0, valores[3])
        entry_hora_fin.grid(row=2, column=1, padx=5, pady=5)

        def actualizar_turno():
            descripcion = entry_descripcion.get()
            hora_inicio = entry_hora_inicio.get()
            hora_fin = entry_hora_fin.get()
            turno = Turno(id=id_turno, descripcion=descripcion, hora_inicio=hora_inicio, hora_fin=hora_fin)
            exito = turno_controller.modificar_turno(turno)
            if exito:
                messagebox.showinfo("Éxito", "Turno modificado correctamente.")
                ventana.destroy()
                self.cargar_turnos()
            else:
                messagebox.showerror("Error", "No se pudo modificar el turno.")

        tk.Button(ventana, text="Guardar", command=actualizar_turno).grid(row=3, column=0, columnspan=2, pady=10)

    def eliminar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un turno para eliminar.")
            return
        item = self.tree.item(seleccion)
        id_turno = item['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este turno?")
        if confirmar:
            exito = turno_controller.eliminar_turno(id_turno)
            if exito:
                messagebox.showinfo("Éxito", "Turno eliminado correctamente.")
                self.cargar_turnos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el turno.")

    def volver(self):
        self.frame.destroy()
        from src.views.main_menu_view import MainMenuView
        MainMenuView(self.master)
