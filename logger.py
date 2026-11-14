import datetime
import os

class LoggerFJ:
    _archivo = "sistema_fj.log"

    @classmethod
    def registrar(cls, nivel: str, mensaje: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel.upper()}] {mensaje}\n"
        try:
            with open(cls._archivo, "a", encoding="utf-8") as f:
                f.write(linea)
        except Exception as e:
            print(f"Error crítico al escribir en el log: {e}")

    @classmethod
    def info(cls, mensaje: str):
        cls.registrar("INFO", mensaje)

    @classmethod
    def error(cls, mensaje: str):
        cls.registrar("ERROR", mensaje)

    @classmethod
    def advertencia(cls, mensaje: str):
        cls.registrar("ADVERTENCIA", mensaje)
        