import datetime
import json
import pandas as pd
from app.repositories import sqlite_repository
from ..Errors.ServiceError import ServiceError
from ..Model.Empleado import Empleado
from ..Services.EmpleadoService import EmpleadoService
from flask import Blueprint, jsonify, request

empleado_bp = Blueprint('empleados', __name__)
_empleados = EmpleadoService()

@empleado_bp.route('/empleados', methods=['GET'])
def get_empleados():
    try:
        df = _empleados.get_empleados_from_google()
        if not df.empty and isinstance(df, pd.DataFrame):
            return df.to_json(orient='records', indent=2), 200
   
        empleado_list = _empleados.get_empleados_from_db()
        if isinstance(empleado_list, list):
            return jsonify(empleado_list), 200
    
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500
    
@empleado_bp.route('/empleado/<int:id>', methods=['GET'])
def get_empleado_by_id(id):
    try:
        registro = _empleados.get_empleado_by_id_from_google(id)
        if isinstance(registro, dict):
            return json.dumps(registro), 200
       
        empleado_list = _empleados.get_empleado_by_id_from_db(id)
        if empleado_list is not None:
            return jsonify(empleado_list), 200
        else:
            return jsonify({"message": "empleado no encontrado"}), 404
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500

    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@empleado_bp.route('/empleado', methods=['POST'])
def create_empleado():
    try:
        data = request.get_json()
        empleado = Empleado(nombre=data["Nombre"], 
                            correo_electronico=data["CorreoElectronico"], 
                            numero_telefono=data["NumeroTelefono"],
                            fecha_nacimiento=data["FechaNacimiento"],
                            fecha_ingreso=datetime.datetime.now(),
                            id_puesto_empleado=data["IdPuestoEmpleado"],
                            activo="1"
                            )
        response_google = _empleados.create_empleado_from_google(empleado)
        response_db = _empleados.create_empleado_from_db(empleado)
        print(f"google: {response_google}, DB: {response_db}")
        if response_google and response_db == 201:
            return jsonify({"message": "empleado creado exitosamente!"}), 201
    
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@empleado_bp.route('/empleado/<int:id>', methods=['PUT'])
def update_empleado(id):
    try:
        data = request.get_json()
        empleado = Empleado(id_empleado=data["Id"],
                            nombre=data["Nombre"], 
                            correo_electronico=data["CorreoElectronico"], 
                            numero_telefono=data["NumeroTelefono"],
                            fecha_nacimiento=data["FechaNacimiento"],
                            fecha_ingreso=data["FechaIngreso"],
                            id_puesto_empleado=data["IdPuestoEmpleado"],
                            activo=data["Activo"])
        if id != empleado.id:
            return jsonify({"message": "Hay una discrepancia en el envio de los datos!"}), 400
        
        response_google = _empleados.update_empleado_from_google(empleado)
        response_db = _empleados.update_empleado_from_db(empleado)
        if response_google and response_db == 200:
            return jsonify({"message": "empleado actualizado exitosamente!"}), 200
            
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500

@empleado_bp.route('/empleado/<int:id>', methods=['DELETE'])
def delete_empleado(id):
    try:
        response_google = _empleados.delete_empleado_from_google(int(id))
        response_db = _empleados.delete_empleado_from_db(int(id))
        if response_google and response_db == 200:
           return jsonify({"message": "empleado eliminado exitosamente!"}), 200
            
    except ServiceError as se:
        return jsonify({f"Error en capa de servicio: {str(se)}"}), 500
    except Exception as e:
        return jsonify({f"Error en el controlador: {str(e)}"}), 500
