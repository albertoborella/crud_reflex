import reflex as rx
from sqlmodel import Field, Relationship
from datetime import date


class BienAlquilado(rx.Model, table=True):
    mes_anio: date
    #nombre: str
    descripcion: str | None = None
    direccion: str | None = None
    precio_mensual: float
    fecha_final_contrato: date | None = None
    fecha_pago_mensual: date | None = None
    disponible: bool | None = None
    observaciones: str | None = None

    contratos: list["Contrato"] = Relationship(back_populates="bien")

    inquilino_id: int | None = Field(default=None, foreign_key="inquilino.id")
    inquilino: "Inquilino" = Relationship(back_populates="bienes")

class Inquilino(rx.Model, table=True):
    razon_social: str
    domicilio: str
    celular: str | None = None
    condicion_iva: str | None = None
    cuit: str | None = None

    bienes: list["BienAlquilado"] = Relationship(back_populates="inquilino")
    contratos: list["Contrato"] = Relationship(back_populates="inquilino")

class Contrato(rx.Model, table=True):
    fecha_inicial: date | None = None
    fecha_final: date | None = None
    contrato_vigente: bool = Field(default=True)
    # FOREIGN_KEY
    inquilino_id: int | None = Field(default=None,foreign_key="inquilino.id")
    bien_id: int | None = Field(foreign_key="bienalquilado.id") 
    # RELACIONES (Lado Muchos)
    inquilino : "Inquilino" = Relationship(back_populates="contratos")
    bien: "BienAlquilado" = Relationship(back_populates="contratos") 