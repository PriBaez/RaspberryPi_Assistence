import pandas as pd
from ..Errors.ServiceError import ServiceError
from ..Model.Historial import Historial
from ..repositories.GoogleRepository import GoogleSheetsRepository
from ..repositories import sqlite_repository
from ..Services.utils.GoogleSheetsUtils import GoogleSheetsUtils


class HistorialService:
    def __init__(self) -> None:
        self._utils = GoogleSheetsUtils()
        self._google_repo = GoogleSheetsRepository()
        self.worksheet = "personas"
        pass   

    def get_historial_from_google(self):
        try:
            hoja = self._utils.open_worksheet(worksheet=self.worksheet)
            # Lee los datos de la hoja de cálculo
            datos = hoja.get_all_values()
            df = pd.DataFrame(datos[1:], columns=datos[0])
            return df
        except Exception as e:
            raise ServiceError(f"Error obteniendo historials desde G-Sheets: {e}")
    
    def get_historial_from_db(self):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historial")
            historials = cursor.fetchall()
            conn.close()
            historial_list = []
            for historial in historials:
               historial_dict = {
                 "HistorialId": historial[0],
                 "PersonaId": historial[1],
                 "FechaCaptura": historial[2]
                }
            historial_list.append(historial_dict)
            return historial_list
        except Exception as e:
            raise ServiceError(f"Error obteniendo historials desde DB: {str(e)}")
    
    def get_historial_per_user_from_google(self, id:int):
        try:
            df = self.get_historial_from_google()
            registros_filtrados = [registro for registro in df if registro['persona_id'] == id]
            print(registros_filtrados)
            #pd.DataFrame(registros_filtrados)
            return registros_filtrados
        except Exception as e:
            raise ServiceError(f"Error obteniendo historial #{id} desde G-sheets:{e}")
    
    def get_historial_per_user_from_db(self, id:int):
        try:
            conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historials WHERE id = ?", (id,))
            historial = cursor.fetchone()
            conn.close()

            if historial:
                # Transforma el resultado en un diccionario
                historial_dict = {
                 "HistorialId": historial[0],
                 "PersonaId": historial[1],
                 "FechaCaptura": historial[2]
                }
            return historial_dict
        
        except Exception as e:
            raise ServiceError(f"Error obteniendo historial #{id} desde DB:{e}")

