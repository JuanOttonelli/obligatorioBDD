# src/models/turno.py

class Turno:
    def __init__(self, id=None, descripcion='', hora_inicio='', hora_fin=''):
        self.id = id
        self.descripcion = descripcion
        self.hora_inicio = hora_inicio  # Formato 'HH:MM'
        self.hora_fin = hora_fin        # Formato 'HH:MM'
