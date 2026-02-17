import reflex as rx
from app.states.InquilinoState import InquilinoState

def inquilinos() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Cabecera con Botón Volver
            rx.hstack(
                rx.link(
                    rx.button(rx.icon("arrow-left"), "Menú", variant="ghost", color="white"),
                    href="/",
                ),
                rx.spacer(),
                rx.heading("Gestión de Inquilinos", size="8", color="white", font_family="Montserrat"),
                rx.spacer(),
                width="95vw",
                max_width="1200px",
                padding_top="2em",
                align="center",
            ),

            # FORMULARIO EN TARJETA (Glassmorphism)
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("user-plus", color="var(--blue-9)"),
                            rx.text("Datos del Inquilino", size="5", weight="bold", font_family="Montserrat"),
                            spacing="2",
                            margin_bottom="1em",
                        ),
                        # Grid de Inputs para mejor uso del espacio
                        rx.grid(
                            rx.vstack(
                                rx.text("Nombre / Razón Social", size="1", weight="bold"),
                                rx.input(
                                    placeholder="Ej: Juan Pérez o Empresa S.A.",
                                    value=InquilinoState.razon_social,
                                    on_change=InquilinoState.set_razon_social,
                                    width="100%",
                                ),
                                align_items="start", width="100%",
                            ),
                            rx.vstack(
                                rx.text("CUIT / Cuil", size="1", weight="bold"),
                                rx.input(
                                    placeholder="00-00000000-0",
                                    value=InquilinoState.cuit,
                                    on_change=InquilinoState.set_cuit,
                                    width="100%",
                                ),
                                align_items="start", width="100%",
                            ),
                            rx.vstack(
                                rx.text("Celular", size="1", weight="bold"),
                                rx.input(
                                    placeholder="+54 9...",
                                    value=InquilinoState.celular,
                                    on_change=InquilinoState.set_celular,
                                    width="100%",
                                ),
                                align_items="start", width="100%",
                            ),
                            rx.vstack(
                                rx.text("Condición IVA", size="1", weight="bold"),
                                rx.select(
                                    ["Monotributo", "Responsable Inscripto", "Exento"],
                                    value=InquilinoState.condicion_iva,
                                    on_change=InquilinoState.set_value_condicion_iva,
                                    placeholder="Seleccionar...",
                                    width="100%",
                                ),
                                align_items="start", width="100%",
                            ),
                            rx.vstack(
                                rx.text("Domicilio Particular", size="1", weight="bold"),
                                rx.input(
                                    placeholder="Calle, Número, Localidad",
                                    value=InquilinoState.domicilio,
                                    on_change=InquilinoState.set_domicilio,
                                    width="100%",
                                ),
                                align_items="start", width="100%",
                            ),
                            # El botón ocupa el espacio restante
                            rx.vstack(
                                rx.text("Confirmar", size="1", color="transparent"),
                                rx.button(
                                    rx.cond(
                                        InquilinoState.inquilino_id,
                                        rx.hstack(rx.icon("save"), "Actualizar"),
                                        rx.hstack(rx.icon("circle-plus"), "Crear Inquilino"),
                                    ),
                                    on_click=rx.cond(
                                        InquilinoState.inquilino_id,
                                        InquilinoState.actualizar_inquilino,
                                        InquilinoState.nuevo_inquilino,
                                    ),
                                    is_disabled=InquilinoState.razon_social == "",
                                    width="100%",
                                    color_scheme="indigo",
                                    size="3",
                                    cursor="pointer",
                                ),
                                width="100%",
                            ),
                            columns="3",
                            spacing="4",
                            width="100%",
                        ),
                    ),
                    width="95vw",
                    max_width="1200px",
                    padding="2em",
                    background_color="rgba(255, 255, 255, 0.95)",
                    border_radius="15px",
                    box_shadow="0 10px 25px rgba(0,0,0,0.1)",
                ),
            ),

            # TABLA DE RESULTADOS
            rx.card(
                rx.vstack(
                    rx.heading("Listado de Inquilinos", size="5", margin_bottom="1em", font_family="Montserrat"),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Razón Social"),
                                rx.table.column_header_cell("Celular"),
                                rx.table.column_header_cell("CUIT"),
                                rx.table.column_header_cell("Condición"),
                                rx.table.column_header_cell("Acciones", align="center"),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                InquilinoState.inquilinos,
                                lambda i: rx.table.row(
                                    rx.table.cell(i.razon_social, font_weight="medium"),
                                    rx.table.cell(i.celular),
                                    rx.table.cell(i.cuit),
                                    rx.table.cell(
                                        rx.badge(i.condicion_iva, variant="outline", color_scheme="gray")
                                    ),
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("pencil", size=16),
                                                variant="ghost",
                                                on_click=lambda: InquilinoState.editar_inquilino(i.id),
                                                cursor="pointer",
                                            ),
                                            rx.button(
                                                rx.icon("trash-2", size=16),
                                                variant="ghost",
                                                color_scheme="red",
                                                on_click=lambda: InquilinoState.eliminar_inquilino(i.id),
                                                cursor="pointer",
                                            ),
                                            justify="center",
                                        ),
                                    ),
                                    vertical_align="middle",
                                ),
                            ),
                        ),
                        width="100%",
                        variant="surface",
                    ),
                ),
                width="95vw",
                max_width="1200px",
                padding="2em",
                background_color="rgba(255, 255, 255, 0.98)",
                margin_bottom="4em",
            ),
            spacing="7",
            align="center",
        ),
        background="linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
        min_height="100vh",
        width="100%",
    )

    
    
    
