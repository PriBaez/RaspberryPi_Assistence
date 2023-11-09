import sqlite_repository


conn = sqlite_repository.connect_to_database('ponchador_db.db')
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
    print(empleados_list)