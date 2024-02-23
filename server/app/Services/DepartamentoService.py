import pandas as pd
from ..Errors.ServiceError import ServiceError
from ..Model.Departamento import Departamento
from ..repositories.GoogleRepository import GoogleSheetsRepository
from ..repositories import sqlite_repository
from ..Services.utils.GoogleSheetsUtils import GoogleSheetsUtils


class DepartamentoService:
    def __init__(self) -> None:
        self._utils = GoogleSheetsUtils()
        self._google_repo = GoogleSheetsRepository()
        pass
    

    def get_departamentos_from_google(self):
        try:
            hoja = self._utils.open_worksheet()
            # Lee los datos de la hoja de cálculo
            datos = hoja.get_all_values()
            df = pd.DataFrame(datos[1:], columns=datos[0])
            return df
        except Exception as e:
            raise ServiceError(f"Error obteniendo departamentos desde G-Sheets: {e}")
    
    def get_departamentos_from_db(self):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamentos")
            departamentos = cursor.fetchall()
            conn.close()
            departamento_list = []
            for puesto in departamentos:
                departamento_dict = {
                    "IdDepartamento": puesto[0],
                    "NombreDepartamento": puesto[1]
                }
                departamento_list.append(departamento_dict)
            return departamento_list
        except Exception as e:
            raise ServiceError(f"Error obteniendo departamentos desde DB: {str(e)}")
    
    def get_departamento_by_id_from_google(self, id:int):
        try:
            df = self.get_departamentos_from_google()
            registro = df[df['id_departamento'] == str(id)]
            return registro.to_dict(orient='records')[0] if not registro.empty else None
        except Exception as e:
            raise ServiceError(f"Error obteniendo departamento #{id} desde G-sheets:{e}")
    
    def get_departamento_by_id_from_db(self, id:int):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departamentos WHERE id_departamento = ?", (id,))
            departamento = cursor.fetchone()
            conn.close()

            if departamento:
                # Transforma el resultado en un diccionario
                departamento_dict = {
                    "IdDepartamento": departamento[0],
                    "NombreDepartamento": departamento[1]
                }
            return departamento_dict
        
        except Exception as e:
            raise ServiceError(f"Error obteniendo departamento #{id} desde DB:{e}")

    def create_departamento_from_google(self, departamento:Departamento):
        try:
            self.hoja = self._utils.open_worksheet()
            id = self._utils.get_last_id_from_google()
            fila = [id, departamento.Nombre]
            self.hoja.append_row(fila)
            return 201
        except Exception as e:
            raise ServiceError(f"Error creando departamento desde G-Sheets:{e}")
    
    def create_departamento_from_db(self, departamento:Departamento):
        try:
            nombre_departamento = departamento.Nombre   
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO departamentos (nombre_departamento) VALUES (?)", (nombre_departamento,))
            conn.commit()
            conn.close()
            return 201
        except Exception as e:
            raise ServiceError(f"Error creando departamento desde DB:{e}")

    def update_departamento_from_google(self, departamento:Departamento):
        try:
            self.hoja = self._utils.open_worksheet()
            # Obtener la fila que contiene el ID a actualizar
            indice_fila = self._utils.obtener_indice_fila_por_id(departamento.Id)

            if indice_fila:
                # Actualizar cada celda con los nuevos datos del modelo Departamento
                departamento = Departamento(id_departamento=departamento.Id, nombre_departamento=departamento.Nombre)
                self.hoja.update_cell(indice_fila, self._utils.obtener_indice_columna('id_departamento'), departamento.Id)
                self.hoja.update_cell(indice_fila, self._utils.obtener_indice_columna('nombre_departamento'), departamento.Nombre)
                return 200
            else:
                raise ServiceError(f"No se encontró ningún registro con ID {departamento.Id}.")
        except Exception as e:
            raise ServiceError(f"Error actualizando departamento #{departamento.Id} desde G-Sheets:{e}")

    def update_departamento_from_db(self, departamento:Departamento):
       try:
        nombre_departamento = departamento.Nombre
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE departamentos SET nombre_departamento = ? WHERE id_departamento = ?", (nombre_departamento, departamento.Id))
        conn.commit()
        conn.close()
        return 200
       except Exception as e:
           raise ServiceError(f"Error actualizando departamento #{departamento.Id} desde DB:{e}")

    def delete_departamento_from_google(self, id:int):
       try:
        self.hoja = self._utils.open_worksheet()
        # Obtener el índice de la fila que contiene el ID a borrar
        indice_fila = self._utils.obtener_indice_fila_por_id(id)

        if indice_fila:
            # Borrar la fila en la hoja
            self.hoja.delete_rows(indice_fila)
            print(f"Registro con ID #{id} borrado con éxito.")
            return 200
        else:
            raise ServiceError(f"No se encontró ningún registro con ID #{id}.")
       except Exception as e:
           raise ServiceError(f"Error eliminando departamento #{id} desde G-Sheets:{e}")
    
    def delete_departamento_from_db(self, id:int):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM departamentos WHERE id_departamento = ?", (str(id)))
            conn.commit()
            conn.close()
            return 200
        except Exception as e:
            raise ServiceError(f"Error eliminando departamento #{str(id)} desde DB:{str(e)}")
    
