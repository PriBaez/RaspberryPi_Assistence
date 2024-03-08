from datetime import datetime
from typing import Optional

class Empleado:
    def __init__(self, id_empleado=0, nombre="", correo_electronico="", 
                 numero_telefono="", fecha_nacimiento=None, fecha_ingreso=None, 
                 id_puesto_empleado=0, activo=False):
        self.id: int = id_empleado
        self.nombre: str = nombre
        self.correo_electronico: str = correo_electronico
        self.numero_telefono: str = numero_telefono
        self.fecha_nacimiento: datetime = fecha_nacimiento
        self.fecha_ingreso: datetime = fecha_ingreso
        self.id_puesto_empleado: int = id_puesto_empleado
        self.activo: bool = activo
