class SoftwareFJError(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERICO"):
        super().__init__(mensaje)
        self.codigo_error = codigo_error


class ClienteError(SoftwareFJError):
    """Errores relacionados con la validación, creación o gestión de clientes."""
    pass


class ServicioError(SoftwareFJError):
    """Errores relacionados con la definición o parámetros de los servicios."""
    pass


class ReservaError(SoftwareFJError):
    """Errores en el proceso de reserva (disponibilidad, estados, pagos)."""
    pass


class ErrorOperacionCritica(SoftwareFJError):
    """Excepción para errores graves encadenados."""
    pass
