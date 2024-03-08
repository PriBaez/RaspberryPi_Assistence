import pandas as pd
from ..Errors.ServiceError import ServiceError
from ..Model.Puesto import Puesto
from ..repositories.GoogleRepository import GoogleSheetsRepository
from ..repositories import sqlite_repository
from ..Services.utils.GoogleSheetsUtils import GoogleSheetsUtils


class PuestoService:
    def __init__(self) -> None:
        self._utils = GoogleSheetsUtils()
        self._google_repo = GoogleSheetsRepository()
        self.worksheet = "puestos"
        pass   

    def get_puestos_from_google(self):
        try:
            hoja = self._utils.open_worksheet(worksheet=self.worksheet)
            # Lee los datos de la hoja de cálculo
            datos = hoja.get_all_values()
            df = pd.DataFrame(datos[1:], columns=datos[0])
            return df
        except Exception as e:
            raise ServiceError(f"Error obteniendo puestos desde G-Sheets: {e}")
    
    def get_puestos_from_db(self):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM puestos")
            puestos = cursor.fetchall()
            conn.close()
            puesto_list = []
            for puesto in puestos:
                puesto_dict = {
                    "IdPuesto": puesto[0],
                    "NombrePuesto": puesto[1],
                    "Descripcion": puesto[2],
                    "IdDepartamento": puesto[3]
                }
                puesto_list.append(puesto_dict)
            return puesto_list
        except Exception as e:
            raise ServiceError(f"Error obteniendo puestos desde DB: {str(e)}")
    
    def get_puesto_by_id_from_google(self, id:int):
        try:
            df = self.get_puestos_from_google()
            registro = df[df['id_puesto'] == str(id)]
            return registro.to_dict(orient='records')[0] if not registro.empty else None
        except Exception as e:
            raise ServiceError(f"Error obteniendo puesto #{id} desde G-sheets:{e}")
    
    def get_puesto_by_id_from_db(self, id:int):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM puestos WHERE id_puesto = ?", (id,))
            puesto = cursor.fetchone()
            conn.close()

            if puesto:
                # Transforma el resultado en un diccionario
                puesto_dict = {
                    "IdPuestoEmpleado": puesto[0],
                    "NombrePuesto": puesto[1],
                    "Descripcion": puesto[2],
                    "IdDepartamento": puesto[3]
                }
            return puesto_dict
        
        except Exception as e:
            raise ServiceError(f"Error obteniendo puesto #{id} desde DB:{e}")

    def create_puesto_from_google(self, puesto:Puesto):
        try:
            self.hoja = self._utils.open_worksheet(worksheet=self.worksheet)
            id = self._utils.get_last_id_from_google(worksheet=self.worksheet)
            fila = [id, puesto.nombre, puesto.descripcion, puesto.id_departamento]
            self.hoja.append_row(fila)
            return 201
        except Exception as e:
            raise ServiceError(f"Error creando puesto desde G-Sheets:{e}")
    
    def create_puesto_from_db(self, puesto:Puesto):
        try: 
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO puestos (nombre_puesto, descripcion, id_departamento) VALUES (?, ?, ?)", (puesto.nombre, puesto.descripcion, puesto.id_departamento))
            conn.commit()
            conn.close()
            return 201
        except Exception as e:
            raise ServiceError(f"Error creando puesto desde DB:{e}")

    def update_puesto_from_google(
        self, puesto:Puesto):
        try:
            self.hoja = self._utils.open_worksheet(worksheet=self.worksheet)
            # Obtener la fila que contiene el ID a actualizar
            indice_fila = self._utils.obtener_indice_fila_por_id(puesto.id, worksheet=self.worksheet)

            if indice_fila:
                # Actualizar cada celda con los nuevos datos del modelo puesto
                puesto = Puesto(id_puesto=puesto.id, nombre_puesto=puesto.nombre, 
                                descripcion=puesto.descripcion, id_departamento=puesto.id_departamento)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('id_puesto', self.worksheet), puesto.id)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('nombre_puesto', self.worksheet), puesto.nombre)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('descripcion', self.worksheet), puesto.descripcion)
                self.hoja.update_cell(indice_fila, 
                self._utils.obtener_indice_columna('id_departamento', self.worksheet), puesto.id_departamento)
                return 200
            else:
                raise ServiceError(f"No se encontró ningún registro con ID {puesto.id}.")
        except Exception as e:
            raise ServiceError(f"Error actualizando puesto #{puesto.id} desde G-Sheets:{e}")

    def update_puesto_from_db(self, puesto:Puesto):
       try:
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE puestos SET nombre_puesto = ?, descripcion = ?, id_departamento = ? WHERE id_puesto = ?", 
                       (puesto.nombre, puesto.descripcion, puesto.id_departamento, puesto.id))
        conn.commit()
        conn.close()
        return 200
       except Exception as e:
           raise ServiceError(f"Error actualizando puesto #{puesto.id} desde DB:{e}")

    def delete_puesto_from_google(self, id:int):
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
           raise ServiceError(f"Error eliminando puesto #{id} desde G-Sheets:{e}")
    
    def delete_puesto_from_db(self, id:int):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM puestos WHERE id_puesto = ?", (str(id)))
            conn.commit()
            conn.close()
            return 200
        except Exception as e:
            raise ServiceError(f"Error eliminando puesto #{str(id)} desde DB:{str(e)}")
    
