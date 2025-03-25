from .models import Notificacion

class ManejadorNotificaciones():


    def crear_notificacion_asignacion(asignacion, paciente):
        mensaje = f"Se te ha asignado el paciente {paciente.getNombre()}."

        # Se crea la notificacion
        notificacion = Notificacion(
            usuario=asignacion,
            mensaje=mensaje,
        )
        notificacion.save()