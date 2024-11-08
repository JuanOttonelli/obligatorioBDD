import mysql.connector
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Conexión a la base de datos
cnx = mysql.connector.connect(user='root', password='rootpassword', host='127.0.0.1', database='practico3')
cursor = cnx.cursor()

# Funciones de consulta
def query_database(query):
    cursor.execute(query)
    return cursor.fetchall()

def display_results(results):
    output_text.delete('1.0', tk.END)
    for row in results:
        output_text.insert(tk.END, f"{row}\n")

def query1():
    query = '''SELECT students.name FROM practico3.students;'''
    results = query_database(query)
    display_results(results)

def query2():
    query = '''SELECT students.name FROM students JOIN practico3.enrollments e on students.student_id = e.student_id JOIN practico3.courses c on c.course_id = e.course_id WHERE course_name = 'Base de datos I';'''
    results = query_database(query)
    display_results(results)

def query3():
    query = '''SELECT courses.course_name FROM courses ORDER BY course_name;'''
    results = query_database(query)
    display_results(results)

def query4():
    query = '''SELECT students.name, course_name FROM students LEFT JOIN practico3.enrollments e on students.student_id = e.student_id JOIN practico3.courses c on e.course_id = c.course_id;'''
    results = query_database(query)
    display_results(results)

def query5():
    query = '''SELECT students.name, course_name FROM students LEFT JOIN practico3.enrollments e on students.student_id = e.student_id LEFT JOIN practico3.courses c on e.course_id = c.course_id;'''
    results = query_database(query)
    display_results(results)

def query6():
    query = '''SELECT students.major, COUNT(students.student_id) FROM students GROUP BY students.major;'''
    results = query_database(query)
    display_results(results)

def query7():
    query = '''SELECT students.major, COUNT(students.student_id) AS Cantidad FROM students GROUP BY students.major HAVING Cantidad > 1;'''
    results = query_database(query)
    display_results(results)

def query8():
    query = '''SELECT students.name FROM students JOIN practico3.enrollments e on students.student_id = e.student_id JOIN practico3.courses c on c.course_id = e.course_id WHERE course_name = 'Algoritmos 1';'''
    results = query_database(query)
    display_results(results)

def query9():
    query = '''SELECT students.name, AVG(e.grade) FROM students JOIN enrollments e on students.student_id = e.student_id JOIN courses c on e.course_id = c.course_id WHERE c.course_name = 'Algoritmos 1' GROUP BY students.name;'''
    results = query_database(query)
    display_results(results)

def query10():
    query = '''SELECT students.name, COUNT(e.student_id) FROM students LEFT JOIN enrollments e on students.student_id = e.student_id GROUP BY students.name;'''
    results = query_database(query)
    display_results(results)

# Función principal para la GUI
def main_gui():
    window = tk.Tk()
    window.title("Consultas de Base de Datos")

    # Título
    tk.Label(window, text="Menú de Consultas", font=("Helvetica", 14)).pack(pady=10)

    # Área de resultados
    global output_text
    output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20, font=("Helvetica", 10))
    output_text.pack(pady=10)

    # Botones para cada consulta
    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=10)

    tk.Button(buttons_frame, text="1. Obtener todos los estudiantes", command=query1).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(buttons_frame, text="2. Estudiantes en 'Base de datos I'", command=query2).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(buttons_frame, text="3. Listar cursos ordenados", command=query3).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(buttons_frame, text="4. Estudiantes y sus cursos", command=query4).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(buttons_frame, text="5. Estudiantes e inscripciones", command=query5).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(buttons_frame, text="6. Número de estudiantes por carrera", command=query6).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(buttons_frame, text="7. Carreras con más de un estudiante", command=query7).grid(row=3, column=0, padx=5, pady=5)
    tk.Button(buttons_frame, text="8. Estudiantes en 'Algoritmos 1'", command=query8).grid(row=3, column=1, padx=5, pady=5)
    tk.Button(buttons_frame, text="9. Promedio en 'Algoritmos 1'", command=query9).grid(row=4, column=0, padx=5, pady=5)
    tk.Button(buttons_frame, text="10. Total de cursos por estudiante", command=query10).grid(row=4, column=1, padx=5, pady=5)

    # Botón de salir
    tk.Button(window, text="Salir", command=window.quit, bg="red", fg="white").pack(pady=10)

    window.mainloop()

# Ejecutar la GUI
main_gui()
