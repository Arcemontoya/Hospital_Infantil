        function editarFecha(id) {
            let input = document.getElementById("fecha_" + id);
            input.removeAttribute("readonly"); // Habilita la edición
            input.focus(); // Enfoca el campo
        }

        function guardarFecha(id) {
            let input = document.getElementById("fecha_" + id);
            let nuevaFecha = input.value;

            fetch(`/actualizar-fecha/${id}/`, {  // URL de la vista para actualizar
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}"
                },
                body: JSON.stringify({ fecha_aplicacion: nuevaFecha })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    alert("Fecha actualizada correctamente");
                    input.setAttribute("readonly", "true"); // Bloquear edición después de guardar
                } else {
                    alert("Error al actualizar la fecha");
                }
            });
        }