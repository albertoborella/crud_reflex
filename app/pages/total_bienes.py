import reflex as rx
from app.components.bien_alquiler import total_bienes_card
from app.components.tabla_pagos import tabla_pagos
from app.states.BienesAlquilerState import BienesAlquilerState 
 

def formulario():
    return rx.center(  # Centra el bloque en la pantalla
        rx.card(      # Crea el efecto de caja/contenedor con sombra
            rx.form(
                rx.vstack(
                    rx.heading("Registro de Alquiler y Cobros", size="4", margin_bottom="4px"),
                    
                    # -------------------------
                    # FILA 1: Datos del Contrato y Pago
                    # -------------------------
                    rx.hstack(
                        rx.vstack(
                            rx.text("Inquilino", font_size="0.8em"),
                            rx.select(
                                BienesAlquilerState.nombres_inquilinos, 
                                value=BienesAlquilerState.nombre_inquilino_seleccionado,
                                on_change=BienesAlquilerState.handle_inquilino_change,
                                placeholder="Seleccione Inquilino",
                                width="100%",
                            ),
                            spacing="1",
                            flex="2.5",
                        ),
                        rx.vstack(
                            rx.text("Fin Contrato", font_size="0.8em"),
                            rx.input(
                                value=BienesAlquilerState.fecha_final_contrato,
                                type="date",
                                on_change=BienesAlquilerState.set_fecha_final_contrato,
                                width="100%",
                            ),
                            spacing="1",
                            flex="1.5",
                        ),
                        rx.vstack(
                            rx.text("Mes/Año Alq.", font_size="0.8em"),
                            rx.input(
                                name="mes_anio",
                                type="month",
                                value=BienesAlquilerState.mes_anio,
                                on_change=BienesAlquilerState.set_mes_anio,
                                width="100%",
                            ),
                            spacing="1",
                            flex="1.5",
                        ),
                        rx.vstack(
                            rx.text("Fecha Pago", font_size="0.8em"),
                            rx.input(
                                name="fecha_pago_mensual",
                                type="date",
                                value=BienesAlquilerState.fecha_pago_mensual,
                                on_change=BienesAlquilerState.set_fecha_pago_mensual,
                                width="100%",
                            ),
                            spacing="1",
                            flex="1.5",
                        ),
                        rx.vstack(
                            rx.text("Importe", font_size="0.8em"),
                            rx.input(
                                name="precio_mensual",
                                type="number",
                                step="0.01",
                                value=BienesAlquilerState.precio_mensual,
                                on_change=BienesAlquilerState.set_precio_mensual,
                                width="100%",
                            ),
                            spacing="1",
                            flex="1.2",
                        ),
                        rx.vstack(
                            rx.text("Alquilado", font_size="0.8em"),
                            rx.center(
                                rx.checkbox(
                                    checked=BienesAlquilerState.disponible,
                                    on_change=BienesAlquilerState.set_disponible,
                                ),
                                height="40px",
                            ),
                            spacing="1",
                            flex="0.8",
                        ),
                        spacing="4",
                        width="100%",
                        align_items="flex-end",
                    ),

                    # -------------------------
                    # FILA 2: Detalles y Acción
                    # -------------------------
                    rx.hstack(
                        rx.vstack(
                            rx.text("Descripción", font_size="0.8em"),
                            rx.input(
                                name="descripcion",
                                value=BienesAlquilerState.descripcion,
                                on_change=BienesAlquilerState.set_descripcion,
                                width="100%",
                            ),
                            spacing="1",
                            flex="3",
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
                            flex="3",
                        ),
                        rx.vstack(
                            rx.text("Observaciones", font_size="0.8em"),
                            rx.input(
                                name="observaciones",
                                value=BienesAlquilerState.observaciones,
                                on_change=BienesAlquilerState.set_observaciones,
                                width="100%",
                            ),
                            spacing="1",
                            flex="3",
                        ),
                        rx.vstack(
                            rx.text("", font_size="0.8em"),
                            rx.button(
                                rx.cond(
                                    BienesAlquilerState.modo_edicion,
                                    rx.hstack(rx.icon("save"), "Actualizar"),
                                    rx.hstack(rx.icon("plus"), "Guardar"),
                                ),
                                type="submit",
                                width="100%",
                                color_scheme="blue",
                                cursor="pointer",
                            ),
                            spacing="1",
                            flex="1.5",
                        ),
                        spacing="4",
                        width="100%",
                        align_items="flex-end",
                    ),
                    spacing="4",
                ),
                on_submit=BienesAlquilerState.submit_form,
            ),
            width="100%",
            variant="classic", # Le da un borde sutil y sombra
        ),
        width="100%",
        padding_x="20px",    # Margen lateral (izquierdo y derecho)
        padding_y="20px",    # Margen superior e inferior
    )

def total_bienes() -> rx.Component:
    return rx.vstack(

        # total_bienes_card(
        #     BienesAlquilerState.bienes.length()
        # ),
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
        spacing="2",
        align="center",
    )
    
