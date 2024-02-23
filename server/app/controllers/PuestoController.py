import json
import pandas as pd
from flask import Blueprint, request, jsonify

from app.Errors.ServiceError import ServiceError
from ..Model.Puesto import Puesto
from ..Services.PuestoService import puestoService
from ..repositories import sqlite_repository

puesto_bp = Blueprint('puestos', __name__)
_puestos = puestoService()

@puesto_bp.route('/puestos', methods=['GET'])
def get_puestos():
    try:
        df = _puestos.get_puestos_from_google()
        if not df.empty and isinstance(df, pd.DataFrame):
            return df.to_json(orient='records', indent=2), 200
   
        puesto_list = _puestos.get_puestos_from_db()
        if isinstance(puesto_list, list):
            return jsonify(puesto_list), 200
    
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500
    
@puesto_bp.route('/puesto/<int:id>', methods=['GET'])
def get_puesto_by_id(id):
    try:
        registro = _puestos.get_puesto_by_id_from_google(id)
        if isinstance(registro, dict):
            return json.dumps(registro), 200
       
        puesto_list = _puestos.get_puesto_by_id_from_db(id)
        if puesto_list is not None:
            return jsonify(puesto_list), 200
        else:
            return jsonify({"message": "puesto no encontrado"}), 404
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500

    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@puesto_bp.route('/puesto', methods=['POST'])
def create_puesto():
    try:
        data = request.get_json()
        puesto = Puesto(nombre_puesto=data['NombrePuesto'], descripcion=data["Descripcion"], 
                        id_departamento=data["IdDepartamento"])
        response_google = _puestos.create_puesto_from_google(puesto)
        response_db = _puestos.create_puesto_from_db(puesto)
        print(f"google: {response_google}, DB: {response_db}")
        if response_google and response_db == 201:
            return jsonify({"message": "puesto creado exitosamente!"}), 201
    
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@puesto_bp.route('/puesto/<int:id>', methods=['PUT'])
def update_puesto(id):
    try:
        data = request.get_json()
        puesto = Puesto(id_puesto=data["IdPuesto"], nombre_puesto=data['NombrePuesto'], 
                        descripcion=data["Descripcion"], id_departamento=data["IdDepartamento"])
        if id != puesto.id:
            return jsonify({"message": "Hay una discrepancia en el envio de los datos!"}), 400
        
        response_google = _puestos.update_puesto_from_google(puesto)
        response_db = _puestos.update_puesto_from_db(puesto)
        if response_google and response_db == 200:
            return jsonify({"message": "puesto actualizado exitosamente!"}), 200
            
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@puesto_bp.route('/puesto/<int:id>', methods=['DELETE'])
def delete_puesto(id):
    try:
        response_google = _puestos.delete_puesto_from_google(int(id))
        response_db = _puestos.delete_puesto_from_db(id)
        if response_google and response_db == 200:
           return jsonify({"message": "puesto eliminado exitosamente!"}), 200
            
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500
