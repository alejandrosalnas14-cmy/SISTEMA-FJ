from abc import ABC, abstractmethod
from excepciones import ClienteError, ServicioError, ReservaError
from logger import LoggerFJ

class EntidadSistema(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        return self._identificador

    @abstractmethod
    def validar_estado(self) -> bool:
        pass


class Cliente(EntidadSistema):
    """Clase Cliente con validaciones estrictas y encapsulación."""
    def __init__(self, identificador: str, nombre: str, email: str, telefono: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ClienteError("El nombre del cliente no puede estar vacío.", "CLI_001")
        self._nombre = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteError(f"Email inválido: '{valor}'.", "CLI_002")
        self._email = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteError(f"Teléfono inválido: '{valor}'. Debe contener solo dígitos (mín. 7).", "CLI_003")
        self._telefono = valor.strip()

    def validar_estado(self) -> bool:
        return bool(self._identificador and self._nombre and self._email and self._telefono)

    def __str__(self):
        return f"Cliente [{self._identificador}]: {self._nombre} ({self._email})"


class Servicio(EntidadSistema, ABC):
    """Clase abstracta Servicio que implementa polimorfismo."""
    def __init__(self, identificador: str, nombre_servicio: str, tarifa_base: float):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        if valor < 0:
            raise ServicioError("La tarifa base no puede ser negativa.", "SRV_001")
        self._tarifa_base = float(valor)

    @abstractmethod
    def calcular_costo(self, duracion_horas: float) -> float:
        pass

    @abstractmethod
    def describir(self) -> str:
        pass

    def validar_estado(self) -> bool:
        return self.tarifa_base >= 0 and bool(self.nombre_servicio)


# --- SERVICIOS ESPECIALIZADOS ---

class ReservaSala(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, capacidad: int, recursos_extra: bool = False):
        super().__init__(identificador, "Reserva de Sala", tarifa_base)
        self.capacidad = capacidad
        self.recursos_extra = recursos_extra

    def calcular_costo(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise ServicioError("La duración en horas debe ser mayor a cero.", "SRV_SALA_01")
        costo = self.tarifa_base * duracion_horas
        if self.recursos_extra:
            costo += 50.0
        return costo

    def describir(self) -> str:
        return f"Reserva de Sala (Capacidad: {self.capacidad} personas, Recursos extra: {self.recursos_extra})"


class AlquilerEquipos(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, tipo_equipo: str, seguro_incluido: bool = True):
        super().__init__(identificador, "Alquiler de Equipos", tarifa_base)
        self.tipo_equipo = tipo_equipo
        self.seguro_incluido = seguro_incluido

    def calcular_costo(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise ServicioError("La duración del alquiler debe ser mayor a cero.", "SRV_EQ_01")
        costo = self.tarifa_base * duracion_horas
        if not self.seguro_incluido:
            costo *= 0.90
        return costo

    def describir(self) -> str:
        return f"Alquiler de Equipo [{self.tipo_equipo}] (Seguro incluido: {self.seguro_incluido})"


class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, nivel_experticia: str):
        super().__init__(identificador, "Asesoría Especializada", tarifa_base)
        self.nivel_experticia = nivel_experticia.lower()

    def calcular_costo(self, duracion_horas: float) -> float:
        if duracion_horas <= 0:
            raise ServicioError("La duración de la asesoría debe ser mayor a cero.", "SRV_AS_01")
        multiplicador = 1.0
        if self.nivel_experticia == "senior":
            multiplicador = 1.5
        elif self.nivel_experticia == "master":
            multiplicador = 2.0
        return self.tarifa_base * duracion_horas * multiplicador

    def describir(self) -> str:
        return f"Asesoría Especializada ({self.nivel_experticia.upper()})"


class Reserva(EntidadSistema):
    ESTADOS = ["CREADA", "CONFIRMADA", "CANCELADA", "COMPLETADA"]

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        super().__init__(identificador)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "CREADA"

    @property
    def duracion_horas(self) -> float:
        return self._duracion_horas

    @duracion_horas.setter
    def duracion_horas(self, valor: float):
        if valor <= 0 or valor > 168:
            raise ReservaError(f"Duración inválida: {valor} horas. Debe estar entre 1 y 168.", "RES_001")
        self._duracion_horas = float(valor)

    def calcular_total_pago(self, descuento_porcentaje: float = 0.0, incluir_impuesto: bool = False) -> float:
        """Método con parámetros opcionales que soporta cálculo base, con descuento y con IVA."""
        base = self.servicio.calcular_costo(self.duracion_horas)
        if not (0 <= descuento_porcentaje <= 100):
            raise ReservaError("El porcentaje de descuento debe estar entre 0 y 100.", "RES_002")
        total = base * (1.0 - (descuento_porcentaje / 100.0))
        if incluir_impuesto:
            total *= 1.19
        return total

    def confirmar(self):
        try:
            if self.estado != "CREADA":
                raise ReservaError(f"No se puede confirmar una reserva en estado '{self.estado}'.", "RES_CONF_01")
            self.estado = "CONFIRMADA"
            LoggerFJ.info(f"Reserva {self.identificador} confirmada con éxito para el cliente {self.cliente.nombre}.")
        except Exception as e:
            LoggerFJ.error(f"Fallo al confirmar reserva {self.identificador}: {e}")
            raise ReservaError(f"Error crítico en confirmación de reserva.") from e

    def cancelar(self):
        try:
            if self.estado == "COMPLETADA":
                raise ReservaError("No se puede cancelar una reserva que ya fue completada.", "RES_CANC_01")
            self.estado = "CANCELADA"
            LoggerFJ.advertencia(f"Reserva {self.identificador} cancelada.")
        except Exception as e:
            LoggerFJ.error(f"Error al cancelar reserva {self.identificador}: {e}")
            raise

    def validar_estado(self) -> bool:
        return self.estado in self.ESTADOS and self.cliente.validar_estado() and self.servicio.validar_estado()
    