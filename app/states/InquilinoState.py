import reflex as rx
from app.models import Inquilino

class InquilinoState(rx.State):
    inquilinos: list[Inquilino] = []
    inquilino_id: str = ""
    razon_social: str = ""
    domicilio: str = ""
    celular: str = ""
    condicion_iva: str = ""
    cuit: str = "" 

    value_condicion_iva: str = "Monotributo"

    @rx.event
    def set_razon_social(self, value: str):
        self.razon_social = value

    @rx.event
    def change_inquilino_id(self, value: str):
        self.inquilino_id = value

    @rx.event
    def set_inquilino_id(self, value: str):
        self.inquilino_id = value

    @rx.event
    def set_domicilio(self, value: str):
        self.domicilio = value

    @rx.event
    def set_celular(self, value: str):
        self.celular = value 

    @rx.event
    def set_condicion_iva(self, value: str):
        self.condicion_iva = value

    @rx.event
    def set_value_condicion_iva(self, value: str):
        self.condicion_iva = value

    @rx.event
    def set_cuit(self, value: str):
        self.cuit = value

    @rx.event
    def get_inquilinos(self):
        with rx.session() as session:
            self.inquilinos = session.exec(
                Inquilino.select().order_by(Inquilino.razon_social)
            ).all()
    
    @rx.event
    def nuevo_inquilino(self):
        with rx.session() as session:
            inquilino = Inquilino(
                razon_social = self.razon_social,
                domicilio = self.domicilio,
                celular = self.celular,
                condicion_iva = self.value_condicion_iva,
                cuit = self.cuit
            )
            session.add(inquilino)
            session.commit()

        self.limpiar_formulario()
        self.get_inquilinos()
        return rx.toast.success("Inquilino creado correctamente")
    
    # Cargar inquilino
    @rx.event
    def cargar_inquilinos(self):
        with rx.session() as session:
            self.inquilinos = session.exec(
                Inquilino.select().order_by(Inquilino.razon_social)
            ).all()

              
    # Editar Inquilino
    @rx.event
    def editar_inquilino(self, id: int):
        with rx.session() as session:
            inq = session.get(Inquilino, id)
            if not inq:
                return rx.toast.error("Inquilino no encontrado")

            self.inquilino_id = str(inq.id)
            self.razon_social = inq.razon_social
            self.domicilio = inq.domicilio
            self.celular = str(inq.celular) if inq.celular else ""
            self.condicion_iva = inq.condicion_iva or ""
            self.cuit = inq.cuit or ""

    #Actualizar inquilino
    @rx.event
    def actualizar_inquilino(self):
        if not self.inquilino_id:
            return rx.toast.warning("No hay inquilino seleccionado")

        with rx.session() as session:
            inq = session.get(Inquilino, self.inquilino_id)
            if not inq:
                return rx.toast.error("Inquilino no encontrado")

            inq.razon_social = self.razon_social
            inq.domicilio = self.domicilio
            inq.celular = self.celular or None
            inq.condicion_iva = self.condicion_iva or None
            inq.cuit = self.cuit or None

            session.add(inq)
            session.commit()

        self.limpiar_formulario()
        self.get_inquilinos()
        return rx.toast.success("Inquilino actualizado")
    
    # Eliminar inquilino
    @rx.event
    def eliminar_inquilino(self, id: int):
        with rx.session() as session:
            inq = session.get(Inquilino, id)
            if not inq:
                return rx.toast.error("Inquilino no encontrado")

            session.delete(inq)
            session.commit()

        self.get_inquilinos()
        return rx.toast.success("Inquilino eliminado")
    
    # Limpiar formulario
    def limpiar_formulario(self):
        self.inquilino_id = ""
        self.razon_social = ""
        self.domicilio = ""
        self.celular = ""
        self.condicion_iva = ""
        self.cuit = ""




