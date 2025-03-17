document.addEventListener("DOMContentLoaded", function() {
    const botonesEliminar = document.querySelectorAll(".eliminartratamiento-btn");

    botonesEliminar.forEach(boton => {
        boton.addEventListener("click", function() {
            const id_Tratamiento = this.dataset.id;

            if (confirm("¿Estás seguro de que deseas eliminar este tratamiento?")) {
                fetch(`/eliminar_tratamiento/${id_Tratamiento}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        alert("Tratamiento eliminado con éxito.");
                        location.reload();
                    } else {
                        return response.json().then(data => {
                            alert("Error al eliminar: " + (data.error || "Error desconocido"));
                        });
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });

    // Función para obtener el token CSRF de Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
