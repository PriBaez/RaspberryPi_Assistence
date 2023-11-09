import sqlite3

# Conectarse a la base de datos (creará un archivo si no existe)
conn = sqlite3.connect('ponchador_db.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()
with open('./app/repositories/sqlite_ponchador_db.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)
conn.commit()

# Leer el contenido del archivo SQL
with open('./app/repositories/registros.sql', 'r') as sql_file:
    sql_script = sql_file.read()

# Ejecutar el script SQL
cursor.executescript(sql_script)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()