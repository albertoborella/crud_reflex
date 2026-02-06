import reflex as rx
from datetime import date
from rxconfig import config

class BienAlquilado(rx.Model, table=True):
    mes_anio: date
    nombre: str
    descripcion: str | None = None
    direccion: str | None = None
    precio_mensual: float
    fecha_inicio_contrato: date | None = None
    fecha_pago_mensual: date | None = None
    disponible: bool | None = None
    observaciones: str | None = None

    