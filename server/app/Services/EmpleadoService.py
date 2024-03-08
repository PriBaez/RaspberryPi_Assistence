import pandas as pd
from ..Errors.ServiceError import ServiceError
from ..Model.Empleado import Empleado
from ..repositories.GoogleRepository import GoogleSheetsRepository
from ..repositories import sqlite_repository
from ..Services.utils.GoogleSheetsUtils import GoogleSheetsUtils


class EmpleadoService:
    def __init__(self) -> None:
        self._utils = GoogleSheetsUtils()
        self._google_repo = GoogleSheetsRepository()
        self.worksheet = "personas"
        pass   

    def get_empleados_from_google(self):
        try:
            hoja = self._utils.open_worksheet(worksheet=self.worksheet)
            # Lee los datos de la hoja de cálculo
            datos = hoja.get_all_values()
            df = pd.DataFrame(datos[1:], columns=datos[0])
            pd.set_option('display.max_columns', None)
            pd.set_option('display.expand_frame_repr', False)
            return df
        except Exception as e:
            raise ServiceError(f"Error obteniendo empleados desde G-Sheets: {e}")
    
    def get_empleados_from_db(self):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas")
            empleados = cursor.fetchall()
            conn.close()
            empleado_list = []
            for empleado in empleados:
                empleado_dict = {
                    "id": empleado[0],
                    "nombre": empleado[1],
                    "huella": empleado[2],
                    "correo_electronico": empleado[3],
                    "numero_telefono": empleado[4],
                    "fecha_nacimiento": empleado[5],
                    "fecha_ingreso": empleado[6],
                    "id_puesto_empleado": empleado[7],
                    "activo": empleado[8]
                }
                empleado_list.append(empleado_dict)
            return empleado_list
        except Exception as e:
            raise ServiceError(f"Error obteniendo empleados desde DB: {str(e)}")
    
    def get_empleado_by_id_from_google(self, id:int):
        try:
            df = self.get_empleados_from_google()
            registro = df[df['id'] == str(id)]
            return registro.to_dict(orient='records')[0] if not registro.empty else None
        except Exception as e:
            raise ServiceError(f"Error obteniendo empleado #{id} desde G-sheets:{e}")
    
    def get_empleado_by_id_from_db(self, id:int):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empleados WHERE id = ?", (id,))
            empleado = cursor.fetchone()
            conn.close()

            if empleado:
                # Transforma el resultado en un diccionario
                empleado_dict = {
                    "id": empleado[0],
                    "nombre": empleado[1],
                    "huella": empleado[2],
                    "correo_electronico": empleado[3],
                    "numero_telefono": empleado[4],
                    "fecha_nacimiento": empleado[5],
                    "fecha_ingreso": empleado[6],
                    "id_puesto_empleado": empleado[7],
                    "activo": empleado[8]
                }

            return empleado_dict
        
        except Exception as e:
            raise ServiceError(f"Error obteniendo empleado #{id} desde DB:{e}")

    def create_empleado_from_google(self, empleado:Empleado):
        try:
            self.hoja = self._utils.open_worksheet(worksheet=self.worksheet)
            id = self._utils.get_last_id_from_google(worksheet=self.worksheet)
            fila = [id, empleado.nombre, "0" ,empleado.correo_electronico, 
                    empleado.numero_telefono, empleado.fecha_nacimiento, empleado.fecha_ingreso, 
                    empleado.id_puesto_empleado, empleado.activo]
            self.hoja.append_row(fila)
            return 201
        except Exception as e:
            raise ServiceError(f"Error creando empleado desde G-Sheets:{e}")
    
    def create_empleado_from_db(self, empleado:Empleado):
        try: 
            with sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO personas (nombre, correo_electronico, numero_telefono, fecha_nacimiento, fecha_ingreso, id_puesto_empleado, activo) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                            (empleado.nombre, empleado.correo_electronico, empleado.numero_telefono, 
                                empleado.fecha_nacimiento, empleado.fecha_ingreso, empleado.id_puesto_empleado, 
                                empleado.activo))
                conn.commit()
                conn.close()
            return 201
        except Exception as e:
            raise ServiceError(f"Error creando empleado desde DB:{e}")

    def update_empleado_from_google(self, empleado:Empleado):
        try:
            self.hoja = self._utils.open_worksheet(worksheet=self.worksheet)
            # Obtener la fila que contiene el ID a actualizar
            indice_fila = self._utils.obtener_indice_fila_por_id(empleado.id, worksheet=self.worksheet)

            if indice_fila:
                # Actualizar cada celda con los nuevos datos del modelo empleado
                empleado = Empleado(empleado.id, empleado.nombre, empleado.correo_electronico, 
                    empleado.numero_telefono, empleado.fecha_nacimiento, empleado.fecha_ingreso, 
                    empleado.id_puesto_empleado, empleado.activo)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('id', self.worksheet), empleado.id)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('nombre', self.worksheet), empleado.nombre)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('correo_electronico', self.worksheet), empleado.correo_electronico)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('numero_telefono', self.worksheet), empleado.numero_telefono)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('fecha_nacimiento', self.worksheet), empleado.fecha_nacimiento)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('fecha_ingreso', self.worksheet), empleado.fecha_ingreso)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('id_puesto_empleado', self.worksheet), empleado.id_puesto_empleado)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('activo', self.worksheet), empleado.activo)
                return 200
            else:
                raise ServiceError(f"No se encontró ningún registro con ID {empleado.id}.")
        except Exception as e:
            raise ServiceError(f"Error actualizando empleado #{empleado.id} desde G-Sheets:{e}")

    def update_empleado_from_db(self, empleado:Empleado):
       try:
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE personas SET nombre=?, correo_electronico=?,  numero_telefono=?, fecha_nacimiento=?, fecha_ingreso=?, id_puesto_empleado=?, activo=? WHERE id = ?", 
                       (empleado.nombre, empleado.correo_electronico, empleado.numero_telefono, 
                            empleado.fecha_nacimiento, empleado.fecha_ingreso, empleado.id_puesto_empleado, 
                            empleado.activo, empleado.id))
        conn.commit()
        conn.close()
        return 200
       except Exception as e:
           raise ServiceError(f"Error actualizando empleado #{str(empleado.id)} desde DB:{str(e)}")

    def delete_empleado_from_google(self, id:int):
       try:
        self.hoja = self._utils.open_worksheet(worksheet=self.worksheet)
        # Obtener el índice de la fila que contiene el ID a borrar
        indice_fila = self._utils.obtener_indice_fila_por_id(id, worksheet=self.worksheet)
        if indice_fila:
            # Borrar la fila en la hoja
            self.hoja.delete_rows(indice_fila)
            return 200
        else:
            raise ServiceError(f"No se encontró ningún registro con ID #{id}.")
       except Exception as e:
           raise ServiceError(f"Error eliminando empleado #{id} desde G-Sheets:{e}")
    
    def delete_empleado_from_db(self, id:int):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM personas WHERE id = ?", (str(id)))
            conn.commit()
            conn.close()
            return 200
        except Exception as e:
            raise ServiceError(f"Error eliminando empleado #{str(id)} desde DB:{str(e)}")
    
