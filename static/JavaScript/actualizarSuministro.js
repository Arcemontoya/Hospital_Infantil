function actualizarTratamiento(expediente, id_tratamiento) {
    fetch(`/actualizar-tratamiento/${expediente}/${id_tratamiento}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("Tratamiento actualizado correctamente");

            // Actualizar la fecha de última aplicación en la interfaz
            let elementoFecha = document.getElementById(`ultima-aplicacion-${id_tratamiento}`);
            if (elementoFecha) {
                elementoFecha.innerText = data.fecha_aplicacion;
            }
        } else {
            alert("Error al actualizar el tratamiento");
        }
    })
    .catch(error => console.error("Error:", error));
}

// Función para obtener el CSRF Token desde las cookies
function getCSRFToken() {
    let csrfToken = null;
    document.cookie.split(";").forEach(cookie => {
        let [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") {
            csrfToken = value;
        }
    });
    return csrfToken;
}
