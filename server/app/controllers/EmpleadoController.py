from ..repositories import sqlite_repository
from flask import Blueprint, jsonify, request

empleado_bp = Blueprint('empleado', __name__)

@empleado_bp.route('/empleados', methods=['GET'])
def get_empleados():
    try:
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM personas")
        empleados = cursor.fetchall()

        conn.close()
        empleados_list = []
        for empleado in empleados:
            empleado_dict = {
                "Id": empleado[0],
                "Nombre": empleado[1],
                "Huella": empleado[2],
                "CorreoElectronico": empleado[3],
                "NumeroTelefono": empleado[4],
                "FechaNacimiento": empleado[5],
                "FechaIngreso": empleado[6],
                "IdPuestoEmpleado": empleado[7],
                "Activo": empleado[8]
            }
            empleados_list.append(empleado_dict)

        return jsonify(empleados_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@empleado_bp.route('/empleado/<int:id>', methods=['GET'])
def get_empleado_by_id(id):
    conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
    empleado = cursor.fetchone()
    conn.close()

    if empleado:
        # Transforma el resultado en un diccionario
        empleado_dict = {
            "Id": empleado[0],
            "Nombre": empleado[1],
            "Huella": empleado[2],
            "CorreoElectronico": empleado[3],
            "NumeroTelefono": empleado[4],
            "FechaNacimiento": empleado[5],
            "FechaIngreso": empleado[6],
            "IdPuestoEmpleado": empleado[7],
            "Activo": empleado[8]
        }
        return jsonify(empleado_dict)
    else:
        return jsonify({"message": "Empleado no encontrado"}), 404

@empleado_bp.route('/empleado', methods=['POST'])
def create_empleado():
    try:
        data = request.get_json()
        id = data.get('Id')
        name = data.get('Nombre')
        email_address = data.get('CorreoElectronico')
        phone_number = data.get('NumeroTelefono')
        born_date = data.get('FechaNacimiento')
        entry_date = data.get('FechaIngreso')
        job_name_id = data.get('IdPuestoEmpleado')
        active = data.get('Activo')

        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        print('INSERT INTO personas (nombre, correo_electronico,  numero_telefono, fecha_nacimiento, fecha_ingreso, id_puesto_empleado, activo) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, email_address, phone_number, born_date, entry_date, job_name_id, active))
        cursor.execute('INSERT INTO personas (nombre, correo_electronico,  numero_telefono, fecha_nacimiento, fecha_ingreso, id_puesto_empleado, activo) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, email_address, phone_number, born_date, entry_date, job_name_id, active))
        print()
        conn.commit()
        conn.close()

        return jsonify({"message": "empleado creado exitosamente!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@empleado_bp.route('/empleado/<int:id>', methods=['PUT'])
def update_empleado(id):
    try:
        data = request.get_json()
        id = data.get('Id')
        name = data.get('Nombre')
        email_address = data.get('CorreoElectronico')
        phone_number = data.get('NumeroTelefono')
        born_date = data.get('FechaNacimiento')
        entry_date = data.get('FechaIngreso')
        job_name_id = data.get('IdPuestoEmpleado')
        active = data.get('Activo')

        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE personas SET nombre=?, correo_electronico=?,  numero_telefono=?, fecha_nacimiento=?, fecha_ingreso=?, id_puesto_empleado=?, activo=? WHERE id = ?", (name, email_address, phone_number, born_date, entry_date, job_name_id, active, id))
        conn.commit()
        conn.close()

        return jsonify({"message": "empleado actualizado exitosamente!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@empleado_bp.route('/empleado/<int:id>', methods=['DELETE'])
def delete_empleado(id):
    try:
        conn = sqlite_repository.connect_to_database('./app/repositories/ponchador_db.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM personas WHERE id = ?", (str(id)))
        conn.commit()
        conn.close()

        return jsonify({"message": "empleado eliminado exitosamente!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
