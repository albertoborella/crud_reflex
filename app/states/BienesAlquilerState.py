import reflex as rx
from app.models import BienAlquilado
from datetime import date

class BienesAlquilerState(rx.State):
    bienes: list[BienAlquilado] = []
    form_data: dict = {}

    modo_edicion: bool = False
    id_editando: int | None = None

    # Campos del formulario
    mes_anio: str = ""
    nombre: str = ""
    direccion: str = ""
    descripcion: str = ""
    precio_mensual: str = ""
    fecha_pago_mensual: str = ""
    fecha_inicio_contrato: str = ""
    disponible: bool = True
    observaciones: str = ""

    # --------------------
    # SETTERS EXPLÍCITOS
    # --------------------
    @rx.event
    def set_mes_anio(self, value: str):
        self.mes_anio = value

    @rx.event
    def set_nombre(self, value: str):
        self.nombre = value

    @rx.event
    def set_direccion(self, value: str):
        self.direccion = value

    @rx.event
    def set_descripcion(self, value: str):
        self.descripcion = value

    @rx.event
    def set_precio_mensual(self, value: str):
        self.precio_mensual = value

    @rx.event
    def set_fecha_pago_mensual(self, value: str):
        self.fecha_pago_mensual = value

    @rx.event
    def set_fecha_inicio_contrato(self, value: str):
        self.fecha_inicio_contrato = value

    @rx.event
    def set_disponible(self, value: bool):
        self.disponible = value

    @rx.event
    def set_observaciones(self, value: str):
        self.observaciones = value

    # Limpiar formulario
    @rx.event
    def reset_form(self):
        self.modo_edicion = False
        self.id_editando = None
        self.mes_anio = ""
        self.nombre = ""
        self.direccion = ""
        self.descripcion = ""
        self.precio_mensual = ""
        self.fecha_pago_mensual = ""
        self.fecha_inicio_contrato = ""
        self.disponible = True
        self.observaciones = ""

    # LISTAR BIENES
    @rx.event
    def get_bienes(self):
        with rx.session() as session:
            self.bienes = session.exec(BienAlquilado.select()).all()

    # GUARDAR BIEN (INSERTAR REGISTRO)
    @rx.event
    def handle_submit(self, form_data: dict):

        def parse_date(value):
            return date.fromisoformat(value) if value else None

        year, month = form_data["mes_anio"].split("-")
        mes_anio = date(int(year), int(month), 1)

        self.form_data = form_data
        print("Formulario enviado con los siguientes datos:")

        for clave, valor in form_data.items():
            print(f"{clave}: {valor}")

        nuevo_registro = BienAlquilado(
            mes_anio=mes_anio,
            nombre=form_data.get("nombre"),
            descripcion=form_data.get("descripcion"),
            direccion=form_data.get("direccion"),
            precio_mensual=float(form_data.get("precio_mensual", 0)),
            fecha_inicio_contrato=parse_date(form_data.get("fecha_inicio_contrato")),
            fecha_pago_mensual=parse_date(form_data.get("fecha_pago_mensual")),
            disponible=form_data.get("disponible") == "on",
            observaciones=form_data.get("observaciones"),
        )

        with rx.session() as session:
            session.add(nuevo_registro)
            session.commit()

        # Actualiza la lista de bienes despues de agregar un nuevo registro
        self.get_bienes()
        # Limpiar el formulario
        self.reset_form()

        return rx.toast.success("Bien agregado correctamente")

    # EDITAR REGISTRO
    @rx.event
    def cargar_registro(self, id: int):
        with rx.session() as session:
            r = session.get(BienAlquilado, id)
            if not r:
                return

            self.id_editando = r.id
            self.mes_anio = r.mes_anio.strftime("%Y-%m")
            self.nombre = r.nombre
            self.descripcion = r.descripcion
            self.direccion = r.direccion
            self.precio_mensual = str(r.precio_mensual or "")
            self.fecha_pago_mensual = str(r.fecha_pago_mensual)
            self.fecha_inicio_contrato = str(r.fecha_inicio_contrato)
            self.disponible = r.disponible
            self.observaciones = r.observaciones

            self.modo_edicion = True
    
    # GRABAR CAMBIOS EN REGISTRO EDITADO
    @rx.event
    def actualizar_registro(self):
        if not self.id_editando:
            return rx.toast.error("No hay registro seleccionado para editar.")

        with rx.session() as session:
            r = session.get(BienAlquilado, self.id_editando)
            if not r:
                return

            year, month = self.mes_anio.split("-")
            r.mes_anio = date(int(year), int(month), 1)
            r.nombre = self.nombre
            r.direccion = self.direccion
            r.descripcion = self.descripcion
            r.precio_mensual = self.precio_mensual
            r.fecha_pago_mensual = (
                date.fromisoformat(self.fecha_pago_mensual)
                if self.fecha_pago_mensual else None
            )
            r.fecha_inicio_contrato = (
                date.fromisoformat(self.fecha_inicio_contrato)
                if self.fecha_inicio_contrato else None
            )
            r.disponible = self.disponible
            r.observaciones = self.observaciones

            session.add(r)
            session.commit()

        self.reset_form()
        self.get_bienes()

        return rx.toast.success("Registro actualizado correctamente")

    # EVENTO GENERAL PARA SUBMIT DEL FORMULARIO
    @rx.event
    def submit_form(self, form_data: dict):
        if self.modo_edicion:
            return self.actualizar_registro()
        else:
            return self.handle_submit(form_data)
        
    # ELIMINAR UN REGISTRO
    @rx.event
    def delete_registro(self, id: int):
        with rx.session() as session:
            registro = session.get(BienAlquilado, id)
            if not registro:
                return rx.toast.error("Registro no encontrado")
            
            session.delete(registro)
            session.commit()
        
        self.get_bienes()

        return rx.toast.success("Registro eliminado correctamente")



            