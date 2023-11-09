-- Registros para la tabla "departamentos"
INSERT INTO departamentos (nombre_departamento) VALUES
    ('Departamento de Ventas'),
    ('Departamento de Recursos Humanos'),
    ('Departamento de TI');

-- Registros para la tabla "puestos"
INSERT INTO puestos (nombre_puesto, descripcion, id_departamento) VALUES
    ('Gerente de Ventas', 'Encargado de la gestión del departamento de ventas', 1),
    ('Representante de Ventas', 'Encargado de la venta de productos', 1),
    ('Reclutador', 'Encargado de la contratación de personal', 2),
    ('Desarrollador de Software', 'Desarrollo de aplicaciones de software', 3),
    ('Analista de Seguridad', 'Supervisión de la seguridad informática', 3);
