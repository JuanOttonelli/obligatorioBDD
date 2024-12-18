# src/views/login_view.py

import tkinter as tk
from tkinter import messagebox
from src.controllers.login_controller import verificar_credenciales
from src.views import session  # Importamos el módulo session

class LoginView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Correo:").grid(row=0, column=0)
        self.entry_correo = tk.Entry(self.frame)
        self.entry_correo.grid(row=0, column=1)

        tk.Label(self.frame, text="Contraseña:").grid(row=1, column=0)
        self.entry_contraseña = tk.Entry(self.frame, show="*")
        self.entry_contraseña.grid(row=1, column=1)

        tk.Button(self.frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=2, column=0, columnspan=2, pady=10)

    def iniciar_sesion(self):
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()
        resultado = verificar_credenciales(correo, contraseña)
        if resultado['autenticado']:
            # Actualizamos usuario_actual a través del módulo session
            session.usuario_actual = {
                'correo': correo,
                'tipo_persona': resultado['tipo_persona'],
                'ci_persona': resultado['ci_persona']
            }
            self.frame.destroy()
            from src.views.main_menu_view import MainMenuView
            MainMenuView(self.master)
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")
