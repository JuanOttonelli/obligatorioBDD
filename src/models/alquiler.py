# src/models/alquiler.py

class Alquiler:
    def __init__(self, id=None, alumno_ci='', clase_id=None, equipo_id_alquiler=None):
        self.id = id
        self.alumno_ci = alumno_ci  # CI del alumno que realiza el alquiler
        self.clase_id = clase_id    # ID de la clase en la que está inscrito
        self.equipo_id_alquiler = equipo_id_alquiler  # ID del equipo de alquiler
