import reflex as rx
from app.components.bien_alquiler import total_bienes_card
from app.components.tabla_pagos import tabla_pagos
from app.states.BienesAlquilerState import BienesAlquilerState 
 

def formulario():
    return rx.form(
        rx.vstack(

            # -------------------------
            # FILA 1
            # -------------------------
            rx.hstack(

                rx.vstack(
                    rx.text("Mes y año de alquiler", font_size="0.8em"),
                    rx.input(
                        name="mes_anio",
                        type="month",
                        value=BienesAlquilerState.mes_anio,
                        on_change=BienesAlquilerState.set_mes_anio,
                        width="100%",
                    ),
                    spacing="1",
                    flex="1",
                ),

                rx.vstack(
                    rx.text("Fin del contrato", font_size="0.8em"),
                    rx.input(
                        name="fecha_final_contrato",
                        type="date",
                        value=BienesAlquilerState.fecha_final_contrato,
                        on_change=BienesAlquilerState.set_fecha_final_contrato,
                        width="100%",
                    ),
                    spacing="1",
                    flex="1",
                ),

                rx.vstack(
                    rx.text("Fecha de pago mensual", font_size="0.8em"),
                    rx.input(
                        name="fecha_pago_mensual",
                        type="date",
                        value=BienesAlquilerState.fecha_pago_mensual,
                        on_change=BienesAlquilerState.set_fecha_pago_mensual,
                        width="100%",
                    ),
                    spacing="1",
                    flex="1",
                ),

                rx.vstack(
                    rx.text("Inquilino", font_size="0.8em"),
                    rx.select(
                        items=BienesAlquilerState.inquilinos_opciones,
                        placeholder="Seleccionar inquilino",
                        value=BienesAlquilerState.inquilino_id,
                        on_change=BienesAlquilerState.set_inquilino_id,
                        width="100%",
                    ),
                    spacing="1",
                    flex="2",
                ),




                rx.vstack(
                    rx.text("Dirección", font_size="0.8em"),
                    rx.input(
                        name="direccion",
                        value=BienesAlquilerState.direccion,
                        on_change=BienesAlquilerState.set_direccion,
                        width="100%",
                    ),
                    spacing="1",
                    flex="2",
                ),

                rx.vstack(
                    rx.text("Descripción", font_size="0.8em"),
                    rx.input(
                        name="descripcion",
                        value=BienesAlquilerState.descripcion,
                        on_change=BienesAlquilerState.set_descripcion,
                        width="100%",
                    ),
                    spacing="1",
                    flex="2",
                ),

                rx.vstack(
                    rx.text("Alquilado", font_size="0.8em"),
                    rx.checkbox(
                        name="disponible",
                        checked=BienesAlquilerState.disponible,
                        on_change=BienesAlquilerState.set_disponible,
                    ),
                    spacing="1",
                    flex="1",
                ),

                spacing="4",
                width="100%",
                align="stretch",
            ),

            # -------------------------
            # FILA 2
            # -------------------------
            rx.hstack(

                rx.input(
                    name="precio_mensual",
                    type="number",
                    step="0.01",
                    value=BienesAlquilerState.precio_mensual,
                    on_change=BienesAlquilerState.set_precio_mensual,
                    placeholder="Precio mensual",
                    flex="1",
                ),

                rx.input(
                    name="observaciones",
                    value=BienesAlquilerState.observaciones,
                    on_change=BienesAlquilerState.set_observaciones,
                    placeholder="Observaciones",
                    flex="2",
                ),

                rx.button(
                    rx.cond(
                        BienesAlquilerState.modo_edicion,
                        "Actualizar",
                        "Guardar",
                    ),
                    type="submit",
                ),

                spacing="4",
                width="100%",
                align="stretch",
            ),

        ),
        on_submit=BienesAlquilerState.submit_form,
        width="90vw",
        max_width="1400px",
    )



def total_bienes() -> rx.Component:
    return rx.vstack(

        total_bienes_card(
            BienesAlquilerState.bienes.length()
        ),
        formulario(),

        rx.box(
            tabla_pagos(),
            overflow_x="auto",
            width="90vw",
            max_width="1400px",
            margin_bottom="40px",
        ),
        on_mount=[
            BienesAlquilerState.get_bienes,
            BienesAlquilerState.get_inquilinos,
            ],
        width="100%",
        spacing="8",
        align="center",
    )
    
