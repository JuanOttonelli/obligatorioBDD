# gui.py
import tkinter as tk
from views.login_view import LoginView

#Inicio de interfaz gráfica
def iniciar_aplicacion():
    root = tk.Tk()
    root.title("Escuela de Deportes de Nieve")
    app = LoginView(root)
    root.mainloop()
