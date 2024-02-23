from ...repositories.GoogleRepository import GoogleSheetsRepository


class GoogleSheetsUtils:
    def __init__(self) -> None:
        self._repository = GoogleSheetsRepository()
        pass

    def open_worksheet(self, worksheet):
        gc = self._repository.connect_to_google_api()
        # Abre la hoja de cálculo por su nombre
        nombre_de_hoja = "ponchador"
        sh = gc.open(nombre_de_hoja)
        # Selecciona la hoja por su nombre (puedes cambiar el número según la hoja que desees)
        return sh.worksheet(worksheet)

    def get_last_id_from_google(self, worksheet):
        hoja = self.open_worksheet(worksheet)
        columna_id = hoja.col_values(1)  # Suponiendo que ID está en la primera columna (columna 1)
        # Eliminar el encabezado si existe
        if columna_id and columna_id[0] == "id_departamento":
            columna_id = columna_id[1:]
        ultimo_id = int(columna_id[-1]) if columna_id else None
        return ultimo_id + 1
     
    def obtener_indice_fila_por_id(self, id_buscar, worksheet):
        hoja = self.open_worksheet(worksheet)
        columna_id = hoja.col_values(1)  # Suponiendo que ID está en la primera columna (columna 1)

        # Eliminar el encabezado si existe
        if columna_id and columna_id[0] == "id_departamento":
            columna_id = columna_id[1:]

        try:
            indice_fila = columna_id.index(str(id_buscar)) + 2  # Sumar 2 por el índice base de la hoja
            return indice_fila
        except ValueError:
            return None

    def obtener_indice_columna(self, nombre_columna, worksheet):
        hoja = self.open_worksheet(worksheet=worksheet)
        return hoja.row_values(1).index(nombre_columna) + 1  # Sumar 1 por el índice base de la hoja
