from app.repositories import sqlite_repository
from flask import Blueprint, jsonify, request

departamento_bp = Blueprint('departamentos', __name__)

@departamento_bp.route('/departamentos', methods=['GET'])
def get_departamentos():
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
        

        return jsonify(departamento_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@departamento_bp.route('/departamento/<int:id>', methods=['GET'])
def get_departamento_by_id(id):
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
        return jsonify(departamento_dict)
    else:
        return jsonify({"message": "Departamento no encontrado"}), 404

@departamento_bp.route('/departamento', methods=['POST'])
def create_departamento():
    try:
        data = request.get_json()
        nombre_departamento = data['NombreDepartamento'] 
        print(data['NombreDepartamento'])
        
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO departamentos (nombre_departamento) VALUES (?)", (nombre_departamento,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Departamento creado exitosamente!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@departamento_bp.route('/departamento/<int:id>', methods=['PUT'])
def update_departamento(id):
    try:
        data = request.get_json()
        nombre_departamento = data['NombreDepartamento']

        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE departamentos SET nombre_departamento = ? WHERE id_departamento = ?", (nombre_departamento, id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Departamento actualizado exitosamente!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@departamento_bp.route('/departamento/<int:id>', methods=['DELETE'])
def delete_departamento(id):
    try:
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM departamentos WHERE id_departamento = ?", (id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Departamento eliminado exitosamente!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
