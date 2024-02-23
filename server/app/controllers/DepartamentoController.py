import json
import pandas as pd
from app.repositories import sqlite_repository
from ..Errors.ServiceError import ServiceError
from ..Model.Departamento import Departamento
from ..Services.DepartamentoService import DepartamentoService
from flask import Blueprint, jsonify, request

departamento_bp = Blueprint('departamentos', __name__)
_departamentos = DepartamentoService()

@departamento_bp.route('/departamentos', methods=['GET'])
def get_departamentos():
    try:
        df = _departamentos.get_departamentos_from_google()
        if not df.empty and isinstance(df, pd.DataFrame):
            return df.to_json(orient='records', indent=2), 200
   
        departamento_list = _departamentos.get_departamentos_from_db()
        if isinstance(departamento_list, list):
            return jsonify(departamento_list), 200
    
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500
    
@departamento_bp.route('/departamento/<int:id>', methods=['GET'])
def get_departamento_by_id(id):
    try:
        registro = _departamentos.get_departamento_by_id_from_google(id)
        if isinstance(registro, dict):
            return json.dumps(registro), 200
       
        departamento_list = _departamentos.get_departamento_by_id_from_db(id)
        if departamento_list is not None:
            return jsonify(departamento_list), 200
        else:
            return jsonify({"message": "Departamento no encontrado"}), 404
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500

    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@departamento_bp.route('/departamento', methods=['POST'])
def create_departamento():
    try:
        data = request.get_json()
        departamento = Departamento(nombre_departamento=data['NombreDepartamento'])
        response_google = _departamentos.create_departamento_from_google(departamento)
        response_db = _departamentos.create_departamento_from_db(departamento)
        print(f"google: {response_google}, DB: {response_db}")
        if response_google and response_db == 201:
            return jsonify({"message": "Departamento creado exitosamente!"}), 201
    
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@departamento_bp.route('/departamento/<int:id>', methods=['PUT'])
def update_departamento(id):
    try:
        data = request.get_json()
        departamento = Departamento(id_departamento=data["IdDepartamento"], 
                                    nombre_departamento=data['NombreDepartamento'])
        if id != departamento.Id:
            return jsonify({"message": "Hay una discrepancia en el envio de los datos!"}), 400
        
        response_google = _departamentos.update_departamento_from_google(departamento)
        response_db = _departamentos.update_departamento_from_db(departamento)
        if response_google and response_db == 200:
            return jsonify({"message": "Departamento actualizado exitosamente!"}), 200
            
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@departamento_bp.route('/departamento/<int:id>', methods=['DELETE'])
def delete_departamento(id):
    try:
        response_google = _departamentos.delete_departamento_from_google(int(id))
        response_db = _departamentos.delete_departamento_from_db(int(id))
        if response_google and response_db == 200:
           return jsonify({"message": "Departamento eliminado exitosamente!"}), 200
            
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500
