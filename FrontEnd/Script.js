document.addEventListener('DOMContentLoaded', function () {
    // Hacer una solicitud GET a la API para obtener la lista de estudiantes
    fetch('http://127.16.5.77:5000/api/students')
    .then(response => response.json())
    .then(data => {
    const studentsList = document.getElementById('students-list');
    // Iterar sobre la lista de estudiantes y crear elementos HTML para
   mostrarlos
    data.data.forEach(student => {
    const studentDiv = document.createElement('div');
    studentDiv.classList.add('student');
    studentDiv.innerHTML = `
    <h3>${student.nombre}</h3>
    <p>ID: ${student.id_estudiante}</p>
    <p>Clase: ${student.clase}</p>
    `;
    studentsList.appendChild(studentDiv);
    });
    })
    .catch(error => console.error('Error:', error));
   });