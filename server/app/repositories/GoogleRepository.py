import json
import gspread
import os.path
from google.oauth2.service_account import Credentials
import os

class GoogleSheetsRepository:
    def __init__(self) -> None:
        pass

    root_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(root_path)

    def connect_to_google_api(self):
        try:
            ruta_credenciales = os.path.join(os.path.abspath(os.path.dirname(__file__)), "credentials.json")
            file_exists = os.path.exists(ruta_credenciales)
            # Configura las credenciales (reemplaza 'ruta_al_archivo.json' con la ruta a tu archivo JSON de credenciales)
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials = Credentials.from_service_account_file(ruta_credenciales, scopes=scope)
            gc = gspread.authorize(credentials)
            return gc
        except FileNotFoundError as e:

            print(f"Archivo no encontrado: {e.filename}")
            # file_exists = os.path.exists("credentials.json")
            # print(f"Archivo credentials.json existe? {file_exists}")  # Output: True
