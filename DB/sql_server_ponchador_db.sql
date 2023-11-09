-- Crear la tabla de personas
CREATE TABLE personas (
    id_persona INT PRIMARY KEY NOT NULL,
    nombre NVARCHAR(100) NOT NULL,
    huella VARBINARY(max),
    correo_electronico NVARCHAR(100) NOT NULL,
    numero_telefono NVARCHAR(10) NOT NULL,
    fecha_nacimiento DATETIME NOT NULL,
    fecha_ingreso DATETIME NOT NULL,
    id_puesto_empleado INT NOT NULL,
    activo BIT NOT NULL,
    FOREIGN KEY (id_puesto_empleado) REFERENCES puestos(id_puesto)
);

CREATE TABLE historial (
    historial_id INT PRIMARY KEY NOT NULL,
    persona_id INT NOT NULL,
    fecha_captura TEXT NOT NULL,
    FOREIGN KEY (persona_id) REFERENCES personas(id_persona)
);

-- Crear la tabla de departamentos
CREATE TABLE departamentos (
    id_departamento INT PRIMARY KEY NOT NULL,
    nombre_departamento NVARCHAR(100) NOT NULL
);

-- Crear la tabla de puestos
CREATE TABLE puestos (
    id_puesto INT PRIMARY KEY NOT NULL,
    nombre_puesto NVARCHAR(100) NOT NULL,
    id_departamento INT NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);

