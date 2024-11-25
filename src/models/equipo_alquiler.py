# src/models/equipo_alquiler.py

class EquipoDeAlquiler:
    def __init__(self, id=None, descripcion='', costo=0.0, id_actividad=None):
        self.id = id
        self.descripcion = descripcion
        self.costo = costo
        self.id_actividad = id_actividad
