import reflex as rx
from app.states.ContratoState import ContratoState

def tabla_contratos() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Contratos Registrados", size="5", margin_bottom="1em", font_family="Montserrat"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Inquilino"),
                        rx.table.column_header_cell("Propiedad / Dirección"),
                        rx.table.column_header_cell("Inicio"),
                        rx.table.column_header_cell("Fin"),
                        rx.table.column_header_cell("Estado"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(ContratoState.contratos, lambda c: rx.table.row(
                        rx.table.cell(c.inquilino.razon_social, font_weight="medium"),
                        rx.table.cell(c.bien.direccion),
                        rx.table.cell(c.fecha_inicial.to(str)),
                        rx.table.cell(c.fecha_final.to(str)),
                        rx.table.cell(
                            rx.cond(
                                c.contrato_vigente, 
                                rx.badge("Vigente", color_scheme="green", variant="soft", size="2"), 
                                rx.badge("Finalizado", color_scheme="red", variant="soft", size="2")
                            )
                        ),
                        vertical_align="middle",
                    ))
                ),
                width="100%",
                variant="surface", # Estilo más moderno para la tabla
            ),
        ),
        width="95vw",
        max_width="1400px",
        padding="2em",
        background_color="rgba(255, 255, 255, 0.98)",
    )

def gestion_contratos_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Botón Volver y Título
            rx.hstack(
                rx.link(
                    rx.button(rx.icon("arrow-left"), "Menú", variant="ghost", color="white"),
                    href="/",
                ),
                rx.spacer(),
                rx.heading("Gestión de Contratos", size="8", color="white", font_family="Montserrat"),
                rx.spacer(),
                width="95vw",
                max_width="1400px",
                padding_top="2em",
                align="center",
            ),
            
            # Formulario de alta estilizado
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("file-plus", color="var(--blue-9)"),
                            rx.text("Nuevo Contrato", size="5", weight="bold", font_family="Montserrat"),
                            spacing="2",
                            margin_bottom="1em",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Inquilino", size="1", weight="bold"),
                                rx.select(
                                    ContratoState.nombres_inquilinos,
                                    placeholder="Seleccionar Inquilino",
                                    on_change=ContratoState.set_inquilino_id_por_nombre,
                                    width="100%",
                                ),
                                flex="2",
                            ),
                            rx.vstack(
                                rx.text("Propiedad", size="1", weight="bold"),
                                rx.select(
                                    ContratoState.direcciones_bienes_disponibles,
                                    placeholder="Seleccionar Propiedad",
                                    on_change=ContratoState.set_bien_id_por_direccion,
                                    width="100%",
                                ),
                                flex="2",
                            ),
                            rx.vstack(
                                rx.text("Fecha Inicio", size="1", weight="bold"),
                                rx.input(
                                    type="date", 
                                    value=ContratoState.fecha_inicial,
                                    on_change=ContratoState.set_fecha_inicial,
                                    width="100%",
                                ),
                                flex="1.5",
                            ),
                            rx.vstack(
                                rx.text("Vencimiento", size="1", weight="bold"),
                                rx.input(
                                    type="date", 
                                    value=ContratoState.fecha_final,
                                    on_change=ContratoState.set_fecha_final,
                                    width="100%",
                                ),
                                flex="1.5",
                            ),
                            rx.button(
                                rx.hstack(rx.icon("check"), "Registrar"),
                                on_click=ContratoState.guardar_contrato,
                                color_scheme="indigo",
                                size="3",
                                cursor="pointer",
                                margin_top="auto",
                            ),
                            spacing="4",
                            width="100%",
                            align_items="end",
                        ),
                    ),
                    width="95vw",
                    max_width="1400px",
                    padding="2em",
                    background_color="rgba(255, 255, 255, 0.95)",
                    border_radius="15px",
                ),
                width="100%",
            ),
            
            # Tabla de resultados
            tabla_contratos(),
            
            spacing="7",
            padding_bottom="4em",
            align="center",
        ),
        # Fondo consistente con el resto de la app
        background="linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
        min_height="100vh",
        width="100%",
        on_mount=ContratoState.cargar_datos,
    )
