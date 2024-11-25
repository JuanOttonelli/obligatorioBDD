# src/models/clase.py

class Clase:
    def __init__(self, id=None, ci_instructor=None, id_actividad=None, id_turno=None, dictada=False):
        self.id = id
        self.ci_instructor = ci_instructor
        self.id_actividad = id_actividad
        self.id_turno = id_turno
        self.dictada = dictada
