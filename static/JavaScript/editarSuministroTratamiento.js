document.addEventListener("DOMContentLoaded", function () {
    let modal = document.getElementById("editModal");
    let editId = document.getElementById("editId");
    let editFecha = document.getElementById("editFecha");
    let form = document.getElementById("editForm");

    // Verificar si hay botones disponibles
    let buttons = document.querySelectorAll(".historial-btn");
    console.log("Botones encontrados:", buttons.length);

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            let id = this.getAttribute("data-id");
            let fecha = this.getAttribute("data-fecha");

            console.log("Abriendo modal con ID:", id, "y Fecha:", fecha);

            // Llenar los campos del formulario
            editId.value = id;
            editFecha.value = fecha;

            // Mostrar el modal
            modal.classList.remove("hidden");
        });
    });

    // Función para cerrar el modal
    function closeModal() {
        console.log("Cerrando modal...");
        modal.classList.add("hidden");
    }

    // Asignar evento al botón "Cancelar"
    document.querySelector("#editModal button.bg-gray-400").addEventListener("click", closeModal);

    // Permitir cerrar el modal al hacer clic fuera del contenido
    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Manejar el envío del formulario sin recargar la página
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Evita la redirección

        let id = editId.value;
        let fecha = editFecha.value;
        let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

        console.log("Enviando actualización para ID:", id, "Fecha:", fecha);

        fetch(`/editar_historial/${id}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ fecha_aplicacion: fecha })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Fecha actualizada correctamente");
                alert("Fecha actualizada correctamente");

                // Opcional: Actualizar la fecha en la vista sin recargar
                let fechaTexto = document.querySelector(`[data-id='${id}']`).parentElement.querySelector("h3");
                if (fechaTexto) {
                    let fechaFormateada = new Date(fecha).toLocaleString("es-MX", {
                        day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit"
                    });
                    fechaTexto.innerText = `Aplicado el ${fechaFormateada}`;
                }

                closeModal(); // Cerrar modal después de actualizar
            } else {
                console.error("Error al actualizar la fecha");
                alert("Error al actualizar la fecha");
            }
        })
        .catch(error => {
            console.error("Error en la petición:", error);
            alert("Hubo un error al actualizar la fecha.");
        });
    });
});