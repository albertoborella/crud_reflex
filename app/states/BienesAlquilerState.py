import reflex as rx
from sqlmodel import select
from sqlalchemy.orm import joinedload
from ..models import BienAlquilado, Contrato, Inquilino
from datetime import date, datetime

class BienesAlquilerState(rx.State):
    # Listas para la UI
    inquilinos: list[Inquilino] = []
    bienes: list[BienAlquilado] = []
    
    # Estado del formulario
    modo_edicion: bool = False
    id_editando: int | None = None
    
    # Campos vinculados al formulario
    inquilino_id: int | None = None
    nombre_inquilino_seleccionado: str = ""
    mes_anio: str = ""
    direccion: str = ""
    descripcion: str = ""
    precio_mensual: str = "0.0"
    fecha_pago_mensual: str = ""
    fecha_final_contrato: str = "" # Se auto-completa desde el Contrato
    fecha_final_sugerida: str = ""
    disponible: bool = True
    observaciones: str = ""

    @rx.var
    def nombres_inquilinos(self) -> list[str]:
        return [i.razon_social for i in self.inquilinos]
    
    #SETTERS EXPLICITOS
    @rx.event
    def set_descripcion(self, value: str):
        self.descripcion = value

    @rx.event
    def set_disponible(self, value: bool):
        self.disponible = value

    @rx.event
    def set_precio_mensual(self, value: str):
        self.precio_mensual = value

    @rx.event
    def set_observaciones(self, value: str):
        self.observaciones = value

    @rx.event
    def set_fecha_final_contrato(self, value: str):
        self.fecha_final_contrato = value

    @rx.event
    def set_fecha_pago_mensual(self, value: str):
        self.fecha_pago_mensual = value

    @rx.event
    def set_direccion(self, value: str):
        self.direccion = value

    @rx.event
    def set_mes_anio(self, value: str):
        self.mes_anio = value



    # --- CARGA DE DATOS ---
    @rx.event
    def cargar_datos_iniciales(self):
        self.get_bienes()
        self.cargar_inquilinos()

    @rx.event
    def cargar_inquilinos(self):
        with rx.session() as session:
            self.inquilinos = session.exec(
                select(Inquilino).order_by(Inquilino.razon_social)
            ).all()

    @rx.event
    def get_bienes(self):
        with rx.session() as session:
            # Importante: unique() para evitar duplicados por el joinedload
            statement = select(BienAlquilado).options(
                joinedload(BienAlquilado.inquilino)
            )
            self.bienes = session.exec(statement).unique().all()

    # --- LÓGICA DE CONEXIÓN CON CONTRATO ---
    @rx.event
    def set_inquilino_desde_nombre(self, nombre: str):
        """Al seleccionar un inquilino, busca su contrato activo para el bien."""
        self.nombre_inquilino_seleccionado = nombre
        with rx.session() as session:
            inquilino = session.exec(
                select(Inquilino).where(Inquilino.razon_social == nombre)
            ).first()
            
            if inquilino:
                self.inquilino_id = inquilino.id
                # Buscamos si este inquilino tiene un contrato vigente
                # (Opcional: filtrar también por el bien_id si lo tienes seleccionado)
                st = select(Contrato).where(
                    (Contrato.inquilino_id == inquilino.id) & 
                    (Contrato.contrato_vigente == True)
                )
                contrato = session.exec(st).first()
                
                if contrato:
                    self.fecha_final_contrato = contrato.fecha_final.isoformat()
                    # Si el contrato tiene un monto pactado, podrías setearlo aquí:
                    # self.precio_mensual = str(contrato.monto_pactado)
                else:
                    self.fecha_final_contrato = ""
                    rx.toast.warning("Inquilino sin contrato vigente activo")

    # --- GESTIÓN DEL FORMULARIO ---
    @rx.event
    def reset_form(self):
        self.modo_edicion = False
        self.id_editando = None
        self.nombre_inquilino_seleccionado = ""
        self.inquilino_id = None
        self.mes_anio = ""
        self.direccion = ""
        self.descripcion = ""
        self.precio_mensual = "0.0"
        self.fecha_pago_mensual = ""
        self.fecha_final_contrato = ""
        self.fecha_final_sugerida: str = ""
        self.disponible = True
        self.observaciones = ""

    @rx.event
    def cargar_registro(self, id: int):
        with rx.session() as session:
            r = session.get(BienAlquilado, id)
            if not r: return

            self.id_editando = r.id
            self.mes_anio = r.mes_anio.strftime("%Y-%m") if r.mes_anio else ""
            self.descripcion = r.descripcion
            self.direccion = r.direccion
            self.precio_mensual = str(r.precio_mensual)
            self.fecha_pago_mensual = r.fecha_pago_mensual.isoformat() if r.fecha_pago_mensual else ""
            self.fecha_final_contrato = r.fecha_final_contrato.isoformat() if r.fecha_final_contrato else ""
            self.disponible = r.disponible
            self.observaciones = r.observaciones
            self.inquilino_id = r.inquilino_id
            self.modo_edicion = True

            if r.inquilino:
                self.nombre_inquilino_seleccionado = r.inquilino.razon_social

    @rx.event
    def handle_submit(self, form_data: dict):
        """Maneja tanto la creación como la edición"""
        try:
            with rx.session() as session:
                # 1. Procesar fechas
                try:
                    year, month = self.mes_anio.split("-")
                    fecha_mes_anio = date(int(year), int(month), 1)
                except:
                    return rx.toast.error("Mes/Año inválido")

                f_pago = date.fromisoformat(self.fecha_pago_mensual) if self.fecha_pago_mensual else None
                f_final = date.fromisoformat(self.fecha_final_contrato) if self.fecha_final_contrato else None

                # 2. Preparar datos
                datos = {
                    "mes_anio": fecha_mes_anio,
                    "direccion": self.direccion,
                    "descripcion": self.descripcion,
                    "precio_mensual": float(self.precio_mensual) if self.precio_mensual else 0.0,
                    "fecha_pago_mensual": f_pago,
                    "fecha_final_contrato": f_final,
                    "disponible": self.disponible,
                    "observaciones": self.observaciones,
                    "inquilino_id": self.inquilino_id
                }

                if self.modo_edicion:
                    bien = session.get(BienAlquilado, self.id_editando)
                    if bien:
                        for key, value in datos.items():
                            setattr(bien, key, value)
                        session.add(bien)
                        mensaje = "Registro actualizado"
                else:
                    nuevo = BienAlquilado(**datos)
                    session.add(nuevo)
                    mensaje = "Registro creado"

                session.commit()
                self.reset_form()
                self.get_bienes()
                return rx.toast.success(mensaje)

        except Exception as e:
            return rx.window_alert(f"Error al guardar: {str(e)}")

    @rx.event
    def delete_registro(self, id: int):
        with rx.session() as session:
            registro = session.get(BienAlquilado, id)
            if registro:
                session.delete(registro)
                session.commit()
        self.get_bienes()
        return rx.toast.success("Registro eliminado")
    
        # --- ALIAS DE COMPATIBILIDAD CON LA UI ---
    
    @rx.event
    def get_inquilinos(self):
        """Redirige a la función de carga actual"""
        return self.cargar_inquilinos()

    @rx.event
    def handle_inquilino_change(self, nombre_seleccionado: str):
        """Redirige el cambio de select a la lógica de contrato"""
        return self.set_inquilino_desde_nombre(nombre_seleccionado)

    @rx.event
    def submit_form(self, form_data: dict):
        """Redirige el envío del formulario a la lógica unificada"""
        return self.handle_submit(form_data)

    @rx.event
    def set_fecha_final_sugerida(self, value: str):
        """Setter para la variable que pide la UI"""
        self.fecha_final_sugerida = value





# import reflex as rx
# from app.models import BienAlquilado, Inquilino
# from sqlmodel import select
# from sqlalchemy.orm import joinedload
# from ..models import BienAlquilado, Contrato, Inquilino
# from datetime import date, datetime

# class BienesAlquilerState(rx.State):
#     inquilinos: list[Inquilino] = []
#     inquilinos_opciones: list[str] = []   # 👈 ESTA LÍNEA
#     inquilino_id: int | None = None
#     nombre_inquilino_seleccionado: str = ""

#     bienes: list[BienAlquilado] = []
#     form_data: dict = {}

#     modo_edicion: bool = False
#     id_editando: int | None = None

#     # Campos del formulario
#     mes_anio: str = ""
#     direccion: str = ""
#     descripcion: str = ""
#     precio_mensual: str = "0.0"
#     fecha_pago_mensual: str = ""
#     fecha_final_contrato: str = ""
#     fecha_final_sugerida: str = ""
#     disponible: bool = True
#     observaciones: str = ""

#     @rx.var
#     def nombres_inquilinos(self) -> list[str]:
#         return [i.razon_social for i in self.inquilinos]

#     # --------------------
#     # SETTERS EXPLÍCITOS
#     # --------------------
#     @rx.event
#     def set_mes_anio(self, value: str):
#         self.mes_anio = value

#     @rx.event
#     def set_direccion(self, value: str):
#         self.direccion = value

#     @rx.event
#     def set_descripcion(self, value: str):
#         self.descripcion = value

#     @rx.event
#     def set_precio_mensual(self, value: str):
#         self.precio_mensual = value

#     @rx.event
#     def set_fecha_pago_mensual(self, value: str):
#         self.fecha_pago_mensual = value

#     @rx.event
#     def set_fecha_final_sugerida(self, value: str):
#         self.fecha_final_sugerida = value

#     @rx.event
#     def set_disponible(self, value: bool):
#         self.disponible = value

#     @rx.event
#     def set_observaciones(self, value: str):
#         self.observaciones = value

#     @rx.event
#     def set_inquilino_id(self, value: str):
#         if value and value != "":
#             self.inquilino_id = int(value)
#         else:
#             self.inquilino_id = None

#     @rx.event
#     def cargar_datos_iniciales(self):
#         self.get_bienes()
#         self.cargar_inquilinos()

#     # LIMPIAR FORMULARIO
#     @rx.event
#     def reset_form(self):
#         self.modo_edicion = False
#         self.id_editando = None
#         self.nombre_inquilino_seleccionado = ""
#         self.mes_anio = ""
#         self.direccion = ""
#         self.descripcion = ""
#         self.precio_mensual = ""
#         self.fecha_pago_mensual = ""
#         self.fecha_final_contrato = ""
#         self.disponible = True
#         self.observaciones = ""
#         self.inquilino_id = None

#     # LISTAR BIENES
#     @rx.event
#     def get_bienes(self):
#         with rx.session() as session:
#             statement = select(BienAlquilado).options(joinedload(BienAlquilado.inquilino))
#             self.bienes = session.exec(statement).unique().all()

#     # GUARDAR BIEN (INSERTAR REGISTRO)
#     @rx.event
#     def handle_submit(self, form_data: dict):
#         def parse_date(value):
#             if not value or value == "": return None
#             try:
#                 return date.fromisoformat(str(value))
#             except:
#                 return None
#         try:
#             year, month = self.mes_anio.split("-")
#             fecha_mes_anio = date(int(year), int(month), 1)
#         except (ValueError, AttributeError):
#             return rx.toast.error("Formato de Mes/Año inválido")

#         nuevo_registro = BienAlquilado(
#             mes_anio=fecha_mes_anio,
#             descripcion=self.descripcion,
#             direccion=self.direccion,
#             precio_mensual=float(self.precio_mensual) if self.precio_mensual else 0.0,
#             fecha_final_contrato=parse_date(self.fecha_final_contrato),
#             fecha_pago_mensual=parse_date(self.fecha_pago_mensual),
#             disponible=self.disponible,
#             observaciones=self.observaciones,
#             inquilino_id=self.inquilino_id, # 👈 Esto ya funciona con el Select anterior
#         )
#         with rx.session() as session:
#             session.add(nuevo_registro)
#             session.commit()
#         self.get_bienes()
#         self.reset_form()
#         return rx.toast.success("Bien agregado correctamente")

#     # EDITAR REGISTRO
#     @rx.event
#     def cargar_registro(self, id: int):
#         with rx.session() as session:
#             r = session.get(BienAlquilado, id)
#             if not r:
#                 return

#             self.id_editando = r.id
#             self.mes_anio = r.mes_anio.strftime("%Y-%m")
#             self.descripcion = r.descripcion
#             self.direccion = r.direccion
#             self.precio_mensual = str(r.precio_mensual or "")
#             self.fecha_pago_mensual = str(r.fecha_pago_mensual)
#             self.fecha_final_contrato = str(r.fecha_final_contrato)
#             self.disponible = r.disponible
#             self.observaciones = r.observaciones
#             self.inquilino_id = r.inquilino_id
#             self.modo_edicion = True

#             # BUSCAR EL NOMBRE PARA EL SELECT
#             self.nombre_inquilino_seleccionado = ""
#             for i in self.inquilinos:
#                 if i.id == r.inquilino_id:
#                     self.nombre_inquilino_seleccionado = i.razon_social
#                     break
    
#     # GRABAR CAMBIOS EN REGISTRO EDITADO
#     @rx.event
#     def actualizar_registro(self):
#         if not self.id_editando:
#             return rx.toast.error("No hay registro seleccionado para editar.")
#         with rx.session() as session:
#             r = session.get(BienAlquilado, self.id_editando)
#             if not r:
#                 return

#             year, month = self.mes_anio.split("-")
#             r.mes_anio = date(int(year), int(month), 1)
#             r.direccion = self.direccion
#             r.descripcion = self.descripcion
#             r.precio_mensual = self.precio_mensual
#             r.fecha_pago_mensual = (
#                 date.fromisoformat(self.fecha_pago_mensual)
#                 if self.fecha_pago_mensual else None
#             )
#             r.fecha_final_contrato = (
#                 date.fromisoformat(self.fecha_final_contrato)
#                 if self.fecha_final_contrato else None
#             )
#             r.disponible = self.disponible
#             r.observaciones = self.observaciones

#             session.add(r)
#             session.commit()
#         self.reset_form()
#         self.get_bienes()
#         return rx.toast.success("Registro actualizado correctamente")

#     # EVENTO GENERAL PARA SUBMIT DEL FORMULARIO
#     @rx.event
#     def submit_form(self, form_data: dict):
#         try:
#             with rx.session() as session:
#                 #Buscar ID del inquilino y limpiar el campo "inquilino" (texto)
#                 inquilino_obj = session.exec(
#                     select(Inquilino).where(Inquilino.razon_social == self.nombre_inquilino_seleccionado)
#                 ).first()
#                 form_data.pop("inquilino", None) 
#                 form_data["inquilino_id"] = inquilino_obj.id if inquilino_obj else None

#                 #CONVERTIR PRECIO A FLOAT
#                 precio = form_data.get("precio_mensual")
#                 form_data["precio_mensual"] = float(precio) if precio else 0.0

#                 #CONVERTIR CHECKBOX "on" A BOOLEAN
#                 form_data["disponible"] = form_data.get("disponible") == "on"

#                 #CONVERTIR TODAS LAS FECHAS A OBJETOS DATE
#                 for campo in ["mes_anio", "fecha_final_contrato", "fecha_pago_mensual"]:
#                     valor = form_data.get(campo)
#                     if isinstance(valor, str) and valor.strip() != "":
#                         # Manejo de mes (YYYY-MM) o fecha completa (YYYY-MM-DD)
#                         formato = "%Y-%m" if len(valor) == 7 else "%Y-%m-%d"
#                         form_data[campo] = datetime.strptime(valor, formato).date()
#                     elif valor == "":
#                         form_data[campo] = None

#                 #GUARDAR O EDITAR
#                 if self.modo_edicion:
#                     bien = session.get(BienAlquilado, self.id_editando)
#                     if bien:
#                         for key, value in form_data.items():
#                             setattr(bien, key, value)
#                         session.add(bien)
#                 else:
#                     nuevo_bien = BienAlquilado(**form_data)
#                     session.add(nuevo_bien)
#                 session.commit()
#             self.reset_form()
#             return self.get_bienes()
#         except Exception as e:
#             print(f"Error detallado: {e}")
#             return rx.window_alert(f"Error: {str(e)}")
        
#     @rx.event
#     def delete_registro(self, id: int):
#         with rx.session() as session:
#             registro = session.get(BienAlquilado, id)
#             if not registro:
#                 return rx.toast.error("Registro no encontrado")
#             session.delete(registro)
#             session.commit()
#         self.get_bienes()
#         return rx.toast.success("Registro eliminado correctamente")
    
#     @rx.event
#     def get_inquilinos(self):
#         with rx.session() as session:
#             self.inquilinos = session.exec(
#                 Inquilino.select().order_by(Inquilino.razon_social)
#             ).all()

#     @rx.event
#     def cargar_inquilinos(self):
#         with rx.session() as session:
#             self.inquilinos = session.exec(
#                 Inquilino.select().order_by(Inquilino.razon_social)
#             ).all()

#     @rx.event
#     def set_inquilino_desde_nombre(self, nombre: str):
#         self.nombre_inquilino_seleccionado = nombre
#         for i in self.inquilinos:
#             if i.razon_social == nombre:
#                 self.inquilino_id = i.id
#                 break

#     def guardar_contrato(self, datos_nuevo_contrato):
#         with rx.session() as session:
#             # Buscamos si ya existe uno activo para ese bien
#             existente = session.exec(
#                 select(Contrato).where(
#                     Contrato.bien_id == datos_nuevo_contrato.bien_id,
#                     Contrato.contrato_vigente == True
#                 )
#             ).first()
            
#             if existente:
#                 return rx.window_alert("Error: Este bien ya tiene un contrato activo.")

#     @rx.event
#     def handle_inquilino_change(self, nombre_seleccionado: str):
#         with rx.session() as session:
#             # 1. Buscamos al inquilino por el nombre que vino del Select
#             inquilino = session.exec(
#                 select(Inquilino).where(Inquilino.razon_social == nombre_seleccionado)
#             ).first()
            
#             if inquilino:
#                 self.inquilino_id = inquilino.id
#                 # 2. Buscamos el contrato vigente
#                 statement = select(Contrato).where(
#                     Contrato.inquilino_id == inquilino.id,
#                     Contrato.contrato_vigente == True
#                 )
#                 contrato_activo = session.exec(statement).first()
                
#                 if contrato_activo:
#                     self.fecha_final_contrato = contrato_activo.fecha_final.isoformat()
#                 else:
#                     self.fecha_final_contrato = ""

             








            