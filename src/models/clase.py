# src/models/clase.py

class Clase:
    def __init__(self, id, ci_instructor, id_actividad, id_turno, dictada=False, nombre_instructor=None, apellido_instructor=None, actividad=None, hora_inicio=None, hora_fin=None):
        self.id = id
        self.ci_instructor = ci_instructor
        self.id_actividad = id_actividad
        self.id_turno = id_turno
        self.dictada = dictada
        # Campos adicionales para mostrar información detallada
        self.nombre_instructor = nombre_instructor
        self.apellido_instructor = apellido_instructor
        self.actividad = actividad
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
