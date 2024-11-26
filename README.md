# Escuela de Deportes de Nieve

Aplicación desarrollada en Python para gestionar las actividades, alumnos, instructores y clases de la Escuela de Deportes de Nieve de la UCU.





## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/JuanOttonelli/obligatorioBDD.git
   Instructivo completo para correr la aplicación de forma local.
## A. Requisitos
Para utilizar la aplicación diseñada, asegúrate de cumplir con los siguientes
requisitos:

- Python 3.12 o superior. (Se puede descargar desde python.org).

- Gestor de base de datos: Se utilizó MySQL en este proyecto. (Se puede
descargar desde mysql.com).

- Bibliotecas de Python necesarias:

  - bcrypt: utilizado para hashing de contraseñas.

  - mysql-connector-python: utilizado para la conexión a base de datos
  y consultas.
  El siguiente comando se utiliza para instalar las dependencias:

pip install -r requirements.txt

## B. Configuración Inicial
1. Creación de la base de datos:

   1. Es necesario ubicar los archivos crear_bdd.sql y inserts_bdd.sql en la
carpeta sql en la raíz del proyecto.

   2. Conéctate a tu base de datos local a través de tu usuario de MySQL
cuando se te solicite.

   3. Ejecuta los archivos anteriores en DataGrip.

## C. Ejecución de la Aplicación
1. Actualiza valores de user y password en src/database.py
2. Inicia la aplicación ejecutando con Python el siguiente archivo:
src/main.py
3. Elige la correspondiente opción de login: alumno, administrativo o
instructor.

   
Por ejemplo:

- Usuario: admin@admin.com, Contraseña: adminadmin (Rol de
administrador)

- Usuario: marta.diaz@example.com, Contraseña: 1234 (Rol de
instructor)

- Usuario: juan.perez@example.com, Contraseña: 1234 (Rol de
alumno)


3. Accede al menú principal y selecciona las opciones deseadas, por ejemplo:

- Gestión de instructores.

- Gestión de turnos y actividades.

- Generación de reportes.

   Dependiendo del tipo de usuario, las opciones desplegadas en el menú.