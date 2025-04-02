
document.addEventListener("DOMContentLoaded", function () {
  const botonesEliminar = document.querySelectorAll(".eliminar-btn");

  botonesEliminar.forEach((boton) => {
    boton.addEventListener("click", function () {
      const historialId = this.dataset.id;

      if (confirm("¿Estás seguro de que deseas eliminar este historial?")) {
        fetch(`/eliminar_historial/${historialId}/`, {
          method: "DELETE",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"), // Para protegerse contra CSRF
          },
        }).then((response) => {
          if (response.ok) {
            alert("Historial eliminado con éxito.");
            location.reload(); // Recarga la página para actualizar la tabla
          } else {
            alert("Error al eliminar el historial.");
          }
        });
      }
    });
  });

  // Función para obtener el CSRF token de Django
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});