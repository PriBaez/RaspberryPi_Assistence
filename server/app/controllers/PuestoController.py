from flask import Blueprint, request, jsonify
from ..repositories import sqlite_repository

puesto_bp = Blueprint('puestos', __name__)


@puesto_bp.route('/puesto', methods=['GET'])
def get_puestos():
    try:
    
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM puestos")
        puestos = cursor.fetchall()

        conn.close()
        puestos_list = []
        for puesto in puestos:
            empleado_dict = {
                 "IdPuestoEmpleado": puesto[0],
                 "NombrePuesto": puesto[1],
                 "Descripcion": puesto[2],
                 "IdDepartamento": puesto[3]
            }
            puestos_list.append(empleado_dict)
        

        return jsonify(puestos_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@puesto_bp.route('/puesto/<int:id>', methods=['GET'])
def get_puesto_by_id(id):
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
        return jsonify(puesto_dict)
    else:
        return jsonify({"message": "Puesto no encontrado"}), 404

@puesto_bp.route('/puesto', methods=['POST'])
def create_puesto():
    try:
        data = request.get_json()
        nombre_puesto = data['NombrePuesto']
        descripcion = data['Descripcion']
        id_departamento = data['IdDepartamento']

        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO puestos (nombre_puesto, descripcion, id_departamento) VALUES (?, ?, ?)", (nombre_puesto, descripcion, id_departamento))
        conn.commit()
        conn.close()

        return jsonify({"message": "Puesto creado exitosamente!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@puesto_bp.route('/puesto/<int:id>', methods=['PUT'])
def update_puesto(id):
    try:
        data = request.get_json()
        nombre_puesto = data['NombrePuesto']
        descripcion = data['Descripcion']
        id_departamento = data['IdDepartamento']
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE puestos SET nombre_puesto = ?, descripcion = ?, id_departamento = ? WHERE id_puesto = ?",
                        (nombre_puesto, descripcion, id_departamento, id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Puesto actualizado exitosamente!"}), 200
    
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    
@puesto_bp.route('/puesto/<int:id>', methods=['DELETE'])
def delete_puesto(id):
    try:
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM puestos WHERE id_puesto = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Puesto eliminado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

