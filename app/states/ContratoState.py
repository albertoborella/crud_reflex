import reflex as rx
from sqlmodel import select
from sqlalchemy.orm import joinedload
from ..models import Contrato, Inquilino, BienAlquilado
from datetime import date

class ContratoState(rx.State):
    # Campos del formulario
    inquilino_id: str = ""
    bien_id: str = ""
    fecha_inicial: str = date.today().isoformat()
    fecha_final: str = ""
    monto_pactado: float = 0.0
    contrato_vigente: bool = True
    contratos: list[Contrato] = []
    inquilinos: list[Inquilino] = []
    bienes_disponibles: list[BienAlquilado] = []

    @rx.var
    def nombres_inquilinos(self) -> list[str]:
        return [i.razon_social for i in self.inquilinos]
    
    @rx.var
    def direcciones_bienes_disponibles(self) -> list[str]:
        return [b.direccion for b in self.bienes_disponibles]
        
    @rx.event
    def set_fecha_inicial(self, value: str):
        self.fecha_inicial = value

    @rx.event
    def set_fecha_final(self, value: str):
        self.fecha_final = value

    @rx.event
    def set_inquilino_id_por_nombre(self, nombre: str):
        for i in self.inquilinos:
            if i.razon_social == nombre:
                self.inquilino_id = str(i.id)
                break

    @rx.event
    def set_bien_id_por_direccion(self, direccion: str):
        for b in self.bienes_disponibles:
            if b.direccion == direccion:
                self.bien_id = str(b.id)
                break


    @rx.event
    def cargar_datos(self):
        with rx.session() as session:
            # Traemos contratos con sus relaciones para mostrar nombres en la tabla
            st = select(Contrato).options(
                joinedload(Contrato.inquilino), 
                joinedload(Contrato.bien)
            )
            self.contratos = session.exec(st).unique().all()
            
            # Traemos inquilinos y bienes para los selects
            self.inquilinos = session.exec(select(Inquilino)).all()
            self.bienes_disponibles = session.exec(
                select(BienAlquilado).where(BienAlquilado.disponible == True)
            ).all()

    @rx.event
    def guardar_contrato(self):
        if not self.inquilino_id or not self.bien_id or not self.fecha_final:
            return rx.toast.error("Por favor complete todos los campos")

        with rx.session() as session:
            # 1. Crear el contrato
            nuevo = Contrato(
                inquilino_id=int(self.inquilino_id),
                bien_id=int(self.bien_id),
                fecha_inicial=date.fromisoformat(self.fecha_inicial),
                fecha_final=date.fromisoformat(self.fecha_final),
                contrato_vigente=True
            )
            
            # 2. Actualizar el Bien a NO disponible
            bien = session.get(BienAlquilado, int(self.bien_id))
            if bien:
                bien.disponible = False
                session.add(bien)
            
            session.add(nuevo)
            session.commit()
            
        self.cargar_datos() # Refrescar tabla
        return rx.toast.success("Contrato registrado con éxito")

    @rx.event
    def finalizar_contrato_actual(self, id_contrato: int):
        """Función útil para dar de baja un contrato antes de expirar"""
        with rx.session() as session:
            contrato = session.get(Contrato, id_contrato)
            if contrato:
                contrato.contrato_vigente = False
                # Al finalizar contrato, el bien vuelve a estar disponible
                bien = session.get(BienAlquilado, contrato.bien_id)
                if bien:
                    bien.disponible = True
                session.commit()
                return rx.toast.info("Contrato finalizado. El bien ahora está disponible.")
