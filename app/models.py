import reflex as rx
from sqlmodel import Field, Relationship
from datetime import date


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

    inquilino_id: int | None = Field(default=None, foreign_key="inquilino.id")
    inquilino: "Inquilino" = Relationship(back_populates="bienes")

class Inquilino(rx.Model, table=True):
    razon_social: str
    domicilio: str
    celular: str | None = None
    condicion_iva: str | None = None
    cuit: str | None = None

    bienes: list["BienAlquilado"] = Relationship(back_populates="inquilino")