from flask import Blueprint, request, jsonify
import pandas as pd
from app.repositories import sqlite_repository
from app.Errors.ServiceError import ServiceError
from ..Model.Historial import Historial
from ..Services.HistorialService import HistorialService

historial_bp = Blueprint('historial', __name__)

_historial = HistorialService()

@historial_bp.route('/historial', methods=['GET'])
def get_historial():
    try:
        df = _historial.get_historial_from_google()
        if not df.empty and isinstance(df, pd.DataFrame):
            return df.to_json(orient='records', indent=2), 200
   
        return jsonify(list(), 200)
        # empleado_list = _historial
        # if isinstance(empleado_list, list):
        #     return jsonify(empleado_list), 200
    
        #return jsonify(historial_list), 200

    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

# @historial_bp.route('/historial/<int:id>', methods=['GET'])
# def get_historial_per_user(id):
#     try:
#         conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM historial WHERE p = ?", (id,))
#         historial = cursor.fetchall()
#         conn.close()
        
#         historial_list = []
#         for registro in historial:
#             historial_dict = {
#                  "HistorialId": registro[0],
#                  "PersonaId": registro[1],
#                  "FechaCaptura": registro[2]
# 			}
            
#             historial_list.append(historial_dict)
			

#         return jsonify(historial_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

