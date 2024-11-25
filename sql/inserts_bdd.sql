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
