-- Crear la base de datos
DROP DATABASE escuela_deportes_nieve;
CREATE DATABASE IF NOT EXISTS escuela_deportes_nieve;
USE escuela_deportes_nieve;

-- Tabla tiposPersonas
CREATE TABLE tiposPersonas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- Tabla login
CREATE TABLE login (
    correo VARCHAR(100) PRIMARY KEY,
    contraseña_hash VARCHAR(255) NOT NULL,
    tipo_persona INT NOT NULL,
    ci_persona VARCHAR(20) NOT NULL,
    FOREIGN KEY (tipo_persona) REFERENCES tiposPersonas(id)
);

-- Tabla actividades
CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    restriccion_edad INT NOT NULL
);

-- Tabla equiposDeAlquiler
CREATE TABLE equiposDeAlquiler (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    id_actividad INT NOT NULL,
    FOREIGN KEY (id_actividad) REFERENCES actividades(id)
);

-- Tabla estudiantes
CREATE TABLE estudiantes (
    ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    correo_electronico VARCHAR(100)
);

-- Tabla instructores
CREATE TABLE instructores (
    ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(255) NOT NULL
);

-- Tabla administrativos
CREATE TABLE administrativos (
    ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL
);

-- Tabla turnos
CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);

-- Tabla clase
CREATE TABLE clase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ci_instructor VARCHAR(20) NOT NULL,
    id_actividad INT NOT NULL,
    id_turno INT NOT NULL,
    dictada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (ci_instructor) REFERENCES instructores(ci),
    FOREIGN KEY (id_actividad) REFERENCES actividades(id),
    FOREIGN KEY (id_turno) REFERENCES turnos(id),
    CONSTRAINT instructor_unico_turno UNIQUE (ci_instructor, id_turno)
);

-- Tabla alumno_clase
CREATE TABLE alumno_clase (
    id_clase INT NOT NULL,
    ci_alumno VARCHAR(20) NOT NULL,
    id_equipamiento INT,
    PRIMARY KEY (id_clase, ci_alumno),
    FOREIGN KEY (id_clase) REFERENCES clase(id),
    FOREIGN KEY (ci_alumno) REFERENCES estudiantes(ci),
    FOREIGN KEY (id_equipamiento) REFERENCES equiposDeAlquiler(id)
);

-- Tabla alquileres
CREATE TABLE alquileres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_ci VARCHAR(20) NOT NULL,
    clase_id INT NOT NULL,
    equipo_id_alquiler INT NOT NULL,
    FOREIGN KEY (alumno_ci) REFERENCES estudiantes(ci),
    FOREIGN KEY (clase_id) REFERENCES clase(id),
    FOREIGN KEY (equipo_id_alquiler) REFERENCES equiposDeAlquiler(id)
);










