import reflex as rx
from app.components.bien_alquiler import total_bienes_card
from app.components.tabla_pagos import tabla_pagos
from app.states.BienesAlquilerState import BienesAlquilerState 

def formulario():
    return rx.center(
        rx.card(
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.icon("clipboard-list", size=25, color="var(--blue-9)"),
                        rx.heading("Registro de Alquiler y Cobros", size="5", font_family="Montserrat"),
                        spacing="2",
                        margin_bottom="1.5em",
                        align="center",
                    ),
                    
                    # FILA 1
                    rx.hstack(
                        rx.vstack(
                            rx.text("Inquilino", font_size="0.8em", font_weight="bold"),
                            rx.select(
                                BienesAlquilerState.nombres_inquilinos, 
                                value=BienesAlquilerState.nombre_inquilino_seleccionado,
                                on_change=BienesAlquilerState.handle_inquilino_change,
                                placeholder="Seleccione Inquilino",
                                width="100%",
                                variant="surface",
                            ),
                            spacing="1", flex="2.5",
                        ),
                        rx.vstack(
                            rx.text("Fin Contrato", font_size="0.8em", font_weight="bold"),
                            rx.input(
                                value=BienesAlquilerState.fecha_final_contrato,
                                type="date",
                                on_change=BienesAlquilerState.set_fecha_final_contrato,
                                width="100%",
                            ),
                            spacing="1", flex="1.5",
                        ),
                        rx.vstack(
                            rx.text("Mes/Año Alq.", font_size="0.8em", font_weight="bold"),
                            rx.input(
                                type="month",
                                value=BienesAlquilerState.mes_anio,
                                on_change=BienesAlquilerState.set_mes_anio,
                                width="100%",
                            ),
                            spacing="1", flex="1.5",
                        ),
                        rx.vstack(
                            rx.text("Importe", font_size="0.8em", font_weight="bold"),
                            rx.input(
                                type="number",
                                value=BienesAlquilerState.precio_mensual,
                                on_change=BienesAlquilerState.set_precio_mensual,
                                width="100%",
                                placeholder="$ 0.00",
                            ),
                            spacing="1", flex="1.2",
                        ),
                        spacing="4", width="100%",
                    ),

                    # FILA 2
                    rx.hstack(
                        rx.vstack(
                            rx.text("Descripción / Dirección", font_size="0.8em", font_weight="bold"),
                            rx.input(
                                value=BienesAlquilerState.direccion,
                                on_change=BienesAlquilerState.set_direccion,
                                placeholder="Ej: Av. Santa Fe 1234",
                                width="100%",
                            ),
                            spacing="1", flex="6",
                        ),
                        rx.vstack(
                            rx.text("Acción", font_size="0.8em", font_weight="bold", color="transparent"),
                            rx.button(
                                rx.cond(
                                    BienesAlquilerState.modo_edicion,
                                    rx.hstack(rx.icon("refresh-cw", size=18), "Actualizar"),
                                    rx.hstack(rx.icon("plus", size=18), "Guardar"),
                                ),
                                type="submit",
                                width="100%",
                                color_scheme="indigo",
                                cursor="pointer",
                                size="3",
                            ),
                            spacing="1", flex="1.5",
                        ),
                        spacing="4", width="100%", align_items="flex-end",
                    ),
                    spacing="5",
                ),
                on_submit=BienesAlquilerState.submit_form,
            ),
            width="100%",
            max_width="1200px",
            padding="2em",
            # Estilo Glassmorphism para la tarjeta
            background_color="rgba(255, 255, 255, 0.95)",
            box_shadow="0 10px 30px rgba(0,0,0,0.2)",
            border_radius="15px",
        ),
        width="100%",
        padding_y="2em",
    )

def total_bienes() -> rx.Component:
    return rx.box( # Cambiamos vstack por box para el fondo total
        rx.vstack(
            # Botón Volver estilizado
            rx.link(
                rx.button(rx.icon("arrow-left"), "Volver al Menú", variant="ghost", color="white"),
                href="/",
                align_self="flex-start",
                margin_left="5vw",
                margin_top="2em",
            ),
            
            formulario(),

            # Contenedor de la tabla
            rx.card(
                rx.vstack(
                    rx.heading("Historial de Pagos y Bienes", size="4", margin_bottom="1em"),
                    rx.box(
                        tabla_pagos(),
                        overflow_x="auto",
                        width="100%",
                    ),
                ),
                width="90vw",
                max_width="1400px",
                padding="1.5em",
                background_color="rgba(255, 255, 255, 0.98)",
                margin_bottom="4em",
            ),
            
            align="center",
            spacing="4",
        ),
        # Aplicamos el mismo fondo que en el Index
        background="linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
        min_height="100vh",
        width="100%",
        on_mount=[
            BienesAlquilerState.get_bienes,
            BienesAlquilerState.get_inquilinos,
        ],
    )
    
