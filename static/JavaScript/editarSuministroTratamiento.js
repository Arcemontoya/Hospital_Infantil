        document.addEventListener("DOMContentLoaded", function() {
            const modal = new bootstrap.Modal(document.getElementById("editarModal"));
            const form = document.getElementById("editarForm");

            document.querySelectorAll(".historial-btn").forEach(button => {
                button.addEventListener("click", function() {
                    const id = this.getAttribute("data-id");
                    const fecha = this.getAttribute("data-fecha");

                    document.getElementById("historial_id").value = id;
                    document.getElementById("fecha_aplicacion").value = fecha;
                });
            });

            form.addEventListener("submit", function(event) {
                event.preventDefault();
                const id = document.getElementById("historial_id").value;
                const fecha = document.getElementById("fecha_aplicacion").value;

                fetch(`/actualizar-historial/${id}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": "{{ csrf_token }}",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ fecha_aplicacion: fecha })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert("Error al actualizar");
                    }
                });
            });
        });