
INSERT INTO `tipospersonas` VALUES (1,'Administrativo'),(2,'Instructor'),(3,'Estudiante');

INSERT INTO `turnos` VALUES (1,'09:00:00','11:00:00','Mañana'),(2,'12:00:00','14:00:00','Tarde'),(3,'16:00:00','18:00:00','Noche');

-- Inserción de actividades
INSERT INTO actividades (descripcion, costo, restriccion_edad)
VALUES
('Snowboard', 1000.00, 15),
('Ski', 900.00, 12),
('Moto de Nieve', 1500.00, 18);

-- Equipos de alquiler para Snowboard (id_actividad = 1)
INSERT INTO equiposDeAlquiler (descripcion, costo, id_actividad)
VALUES
('Antiparras', 100.00, 1),
('Casco', 150.00, 1),
('Tabla de Snowboard', 500.00, 1);

-- Equipos de alquiler para Ski (id_actividad = 2)
INSERT INTO equiposDeAlquiler (descripcion, costo, id_actividad)
VALUES
('Antiparras', 100.00, 2),
('Casco', 150.00, 2),
('Esquíes', 400.00, 2);

-- Equipos de alquiler para Moto de Nieve (id_actividad = 3)
INSERT INTO equiposDeAlquiler (descripcion, costo, id_actividad)
VALUES
('Casco', 150.00, 3),
('Mono de Nieve', 200.00, 3);

-- Inserts en la tabla 'estudiantes'
INSERT INTO estudiantes (ci, nombre, apellido, fecha_nacimiento, telefono, correo_electronico)
VALUES
('10000001', 'Juan', 'Pérez', '2000-01-01', '099111111', 'juan.perez@example.com'),
('10000002', 'María', 'Gómez', '1999-02-02', '099222222', 'maria.gomez@example.com'),
('10000003', 'Pedro', 'López', '2001-03-03', '099333333', 'pedro.lopez@example.com'),
('10000004', 'Ana', 'Martínez', '2002-04-04', '099444444', 'ana.martinez@example.com'),
('10000005', 'Luis', 'Rodríguez', '1998-05-05', '099555555', 'luis.rodriguez@example.com'),
('10000006', 'Sofía', 'González', '2000-06-06', '099666666', 'sofia.gonzalez@example.com'),
('10000007', 'Diego', 'Fernández', '1997-07-07', '099777777', 'diego.fernandez@example.com'),
('10000008', 'Laura', 'Sánchez', '2001-08-08', '099888888', 'laura.sanchez@example.com'),
('10000009', 'Jorge', 'Ramírez', '1999-09-09', '099999999', 'jorge.ramirez@example.com'),
('10000010', 'Lucía', 'Torres', '2000-10-10', '099000000', 'lucia.torres@example.com');

-- Inserts en la tabla 'instructores'
INSERT INTO instructores (ci, nombre, apellido, correo_electronico)
VALUES
('20000001', 'Carlos', 'Sosa', 'carlos.sosa@example.com'),
('20000002', 'Marta', 'Díaz', 'marta.diaz@example.com'),
('20000003', 'Roberto', 'Suárez', 'roberto.suarez@example.com'),
('20000004', 'Andrea', 'Romero', 'andrea.romero@example.com'),
('20000005', 'Fernando', 'Vargas', 'fernando.vargas@example.com');

-- Inserts en la tabla 'login' para alumnos
INSERT INTO login (correo, contraseña_hash, tipo_persona, ci_persona)
VALUES
('juan.perez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000001'),
('maria.gomez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000002'),
('pedro.lopez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000003'),
('ana.martinez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000004'),
('luis.rodriguez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000005'),
('sofia.gonzalez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000006'),
('diego.fernandez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000007'),
('laura.sanchez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000008'),
('jorge.ramirez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000009'),
('lucia.torres@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 3, '10000010');

-- Inserts en la tabla 'login' para instructores
INSERT INTO login (correo, contraseña_hash, tipo_persona, ci_persona)
VALUES
('carlos.sosa@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 2, '20000001'),
('marta.diaz@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 2, '20000002'),
('roberto.suarez@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 2, '20000003'),
('andrea.romero@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 2, '20000004'),
('fernando.vargas@example.com', '$2b$12$F6iJRTqQYFFi/6NvbG6L6O87hS7hfMILtlTtgFIAc2YXlxAWYw4Se', 2, '20000005');

INSERT INTO login   (correo, contraseña_hash, tipo_persona, ci_persona) VALUE
('admin@admin.com','$2b$12$yzGGvmmB4H56y/iY9.Kg4.6yP0hVKe7nn9ajvtqnV1acUBY.vjOs6',1,'00000000');


INSERT INTO `clase` VALUES
                           (4,'20000002',3,2,0),
                           (5,'20000002',1,1,0);

INSERT INTO `alquileres` VALUES
                                (13,'10000005',4,7),
                                (14,'10000005',4,8);

INSERT INTO `alumno_clase` VALUES
                                  (4,'10000001',NULL),
                                  (4,'10000002',NULL),
                                  (4,'10000003',NULL),
                                  (4,'10000005',NULL);



