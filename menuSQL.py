import mysql.connector
cnx = mysql.connector.connect(user='root', password='rootpassword', host='127.0.0.1', database='practico3')
cursor = cnx.cursor()


def query1():
    query = (
        '''SELECT students.name 
        FROM practico3.students;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query2():
    query = (
        '''SELECT students.name
        FROM students
        JOIN practico3.enrollments e on students.student_id = e.student_id
        JOIN practico3.courses c on c.course_id = e.course_id
        WHERE course_name = 'Base de datos I';'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query3():
    query = (
        '''SELECT courses.course_name
        FROM courses ORDER BY course_name;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query4():
    query = (
        '''SELECT students.name, course_name FROM students
        LEFT JOIN practico3.enrollments e on students.student_id = e.student_id
        JOIN practico3.courses c on e.course_id = c.course_id;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query5():
    query = (
        '''SELECT students.name, course_name FROM students
LEFT JOIN practico3.enrollments e on students.student_id = e.student_id
LEFT JOIN practico3.courses c on e.course_id = c.course_id;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query6():
    query = (
        '''SELECT students.major, COUNT(students.student_id) FROM students
        GROUP BY students.major;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query7():
    query = (
        '''SELECT students.major, COUNT(students.student_id) AS Cantidad FROM students
        GROUP BY students.major
        HAVING Cantidad > 1;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query8():
    query = (
        '''SELECT students.name FROM students
        join practico3.enrollments e on students.student_id = e.student_id
        join practico3.courses c on c.course_id = e.course_id
        WHERE course_name = 'Algoritmos 1';'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query9():
    query = (
        '''SELECT students.name, AVG(e.grade)
        FROM students
        JOIN enrollments e on students.student_id = e.student_id
        JOIN courses c on e.course_id = c.course_id
        WHERE c.course_name = 'Algoritmos 1'
        GROUP BY students.name;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def query10():
    query = (
        '''SELECT students.name, COUNT(e.student_id)
        FROM students
        LEFT JOIN enrollments e on students.student_id = e.student_id
        GROUP BY students.name;'''
    )
    cursor.execute(query)
    print(cursor.fetchall())


def menu():
    print("Menú Principal")
    print("1. Obtener todos los estudiantes. ")
    print("2. Estudiantes que cursan “Base de datos I”")
    print("3. Listar todos los cursos ordenados por nombre.")
    print("4. Obtener el nombre de los estudiantes y los cursos en los que están inscritos.")
    print("5. Obtener todos los estudiantes y sus inscripciones, incluyendo estudiantes sin inscripciones. ")
    print("6. Obtener el número de estudiantes por carrera.")
    print("7. Obtener el número de estudiantes por carrera, pero solo mostrar las carreras con más de un estudiante. ")
    print("8. Obtener los estudiantes que están inscritos en el curso “Algoritmos 1”. ")
    print("9. Obtener el promedio de calificaciones de los estudiantes en el curso “Algoritmos I”.")
    print("10. Obtener el nombre de los estudiantes y el total de cursos en los que están inscritos. ")
    print("0. Salir")

def main():
    while True:
        menu()
        eleccion = input("Selecciona una opción (1-10): ")

        if eleccion == '1':
            query1()
        elif eleccion == '2':
            query2()
        elif eleccion == '3':
            query3()
        elif eleccion == '4':
            query4()
        elif eleccion == '5':
            query5()
        elif eleccion == '6':
            query6()
        elif eleccion == '7':
            query7()
        elif eleccion == '8':
            query8()
        elif eleccion == '9':
            query9()
        elif eleccion == '10':
            query10()
        elif eleccion == '0':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()