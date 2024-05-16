from flask import Flask, jsonify, request
import mariadb
import sys

# Importar configuración de acceso a la base de datos
from config import DATABASE_CONFIG

app = Flask(__name__)

try:
    conn = mariadb.connect(**DATABASE_CONFIG)
except mariadb.Error as e:
    print(f"Error on connection: {e}")
    sys.exit(1)

cursor = conn.cursor()

# Ruta de prueba
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({'message': '¡Hola, mundo con Flask!'})

# Obtener todos los estudiantes
@app.route('/api/students', methods=['GET'])
def get_students():
    cursor.execute("SELECT * FROM Estudiantes")
    students = cursor.fetchall()
    student_list = []
    for student in students:
        student_list.append({
            "id_estudiante": student[0],
            "nombre": student[1],
            "clase": student[2]
        })
    response = jsonify({"data": student_list})
    response.headers.add("Content-type", "application/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Registrar la asistencia de un estudiante
@app.route('/api/attendance', methods=['POST'])
def register_attendance():
    datos = request.json
    id_estudiante = datos.get('id_estudiante')
    fecha = datos.get('fecha')
    asistio = datos.get('asistio')

    strQry = 'INSERT INTO Asistencias '
    strQry += "(id_estudiante, fecha, asistio) "
    strQry += f"VALUES ('{id_estudiante}', '{fecha}', '{asistio}')"

    cursor.execute(strQry)
    conn.commit()

    response = {"message": "Attendance recorded"}
    return jsonify(response), 200


# Obtener la lista de asistencias de un estudiante específico
@app.route('/api/attendance/<int:id_estudiante>', methods=['GET'])
def get_student_attendance(id_estudiante):
    cursor.execute("SELECT * FROM Asistencias WHERE id_estudiante = ?", (id_estudiante,))
    attendances = cursor.fetchall()
    attendance_list = []
    for attendance in attendances:
        attendance_list.append({
            "id_asistencia": attendance[0],
            "id_estudiante": attendance[1],
            "fecha": attendance[2],
            "asistio": attendance[3]
        })
    response = jsonify({"data": attendance_list})
    response.headers.add("Content-type", "application/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

