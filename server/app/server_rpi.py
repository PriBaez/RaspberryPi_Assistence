#from fingerprint_utils import capture_fingerprint_image
from flask import Flask, request, jsonify
from repositories import sqlite_repository as sqlite

app = Flask(__name__)

# @app.route('/capture_fingerprint', methods=['POST'])

# def capture_fingerprint():
#     # Obtén los datos de la solicitud (ID y nombre)
#     data = request.get_json()
#     person_id = data.get('id')
#     person_name = data.get('name')

#     # Captura la huella dactilar
#     #fingerprint_data = capture_fingerprint_image()

#     # Actualiza la entrada en la base de datos con la huella dactilar
#         # success = database_module.update_fingerprint(person_id, person_name, fingerprint_data)

#     """
#     if success:
#         return jsonify({"message": "Fingerprint captured and stored successfully"})
#     else:
#         return jsonify({"message": "Failed to capture or store fingerprint"}), 500 
#     """
#     print(f"id: {person_id}, \n name: {person_name}")
#     response = ({"message": f"datos capturados correctamente"})
#     return jsonify(response), 200

# @app.route('/new-empleado', methods=['POST'])
# def get_info():
#     # Obtén los datos de la solicitud (ID y nombre)
#     data = request.get_json()
#     id = data.get('Id')
#     name = data.get('Nombre')
#     email_address = data.get('CorreoElectronico')
#     phone_number = data.get('NumeroTelefono')
#     born_date = data.get('FechaNacimiento')
#     entry_date = data.get('FechaIngreso')
#     job_name_id = data.get('IdPuestoEmpleado')
#     active = data.get('Activo')

#     try:

#         conn = sqlite.connect_to_database('./repositories/ponchador_db.db');

#         # Crear un cursor para ejecutar comandos SQL
#         cursor = conn.cursor()

#         # Insertar datos en la tabla
#         cursor.execute('INSERT INTO personas (nombre, correo_electronico,  numero_telefono, fecha_nacimiento, fecha_ingreso, id_puesto_empleado, activo) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, email_address, phone_number, born_date, entry_date, job_name_id, active))

#         # Guardar los cambios en la base de datos
#         conn.commit()
#         conn.close()

#         # print(f"id: {id}, \n name: {name} \n address:{address} \n phone_number:{phone_number} \n born date:{born_date} \n active:{active}")
#         response = ({"message": f"datos capturados correctamente"})
#         return jsonify(response), 200
    
#     except Exception as e:
#         print(e)
#         response = {"message": "Error al capturar datos"}
#         return jsonify(response), 500


# @app.route('/empleados', methods=['GET'])
# def get_empleados():
#     try:
#         # Conecta con la base de datos (asegúrate de que la base de datos existe)
#         connection = sqlite.connect_to_database('./repositories/ponchador_db.db')
#         cursor = connection.cursor()

#         # Ejecuta una consulta SQL para seleccionar todos los registros de la tabla empleados
#         cursor.execute('SELECT * FROM personas')
#         empleados = cursor.fetchall()

#         connection.close()
        
#         response = {"message": empleados}
        
#         return jsonify(response), 200
       
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
