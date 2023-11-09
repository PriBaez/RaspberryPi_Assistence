
DROP TABLE IF EXISTS personas;

CREATE TABLE personas (
    id INTEGER PRIMARY KEY NOT NULL,
    nombre TEXT NOT NULL,
    huella BLOB,
    correo_electronico TEXT NOT NULL,
    numero_telefono TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_ingreso DATE NOT NULL,
    id_puesto_empleado INTEGER NOT NULL,
    activo BOOLEAN  NOT NULL,
    FOREIGN KEY (id_puesto_empleado) REFERENCES puestos(id_puesto)
);

DROP TABLE IF EXISTS historial;
CREATE TABLE historial (
    historial_id INTEGER PRIMARY KEY NOT NULL,
    persona_id INTEGER NOT NULL,
    fecha_captura TEXT NOT NULL,
    FOREIGN KEY (persona_id) REFERENCES personas(id)
);

DROP TABLE IF EXISTS puestos;
CREATE TABLE puestos (
    id_puesto INTEGER PRIMARY KEY NOT NULL,
    nombre_puesto TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    id_departamento TEXT NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);

DROP TABLE IF EXISTS departamentos;
CREATE TABLE departamentos (
    id_departamento INTEGER PRIMARY KEY NOT NULL,
    nombre_departamento TEXT NOT NULL
);
