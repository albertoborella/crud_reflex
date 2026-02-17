import reflex as rx

from app.states.ContratoState import ContratoState


def tabla_contratos() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Inquilino"),
                rx.table.column_header_cell("Bien / Dirección"),
                rx.table.column_header_cell("Inicio"),
                rx.table.column_header_cell("Fin"),
                rx.table.column_header_cell("Estado"),
            )
        ),
        rx.table.body(
            rx.foreach(ContratoState.contratos, lambda c: rx.table.row(
                rx.table.cell(c.inquilino.razon_social),
                rx.table.cell(c.bien.direccion),
                rx.table.cell(c.fecha_inicial.to(str)),
                rx.table.cell(c.fecha_final.to(str)),
                rx.table.cell(
                    rx.cond(c.contrato_vigente, 
                        rx.badge("Vigente", color_scheme="green"), 
                        rx.badge("Finalizado", color_scheme="red")
                    )
                ),
            ))
        ),
        width="100%",
    )

def gestion_contratos_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Gestión de Contratos", size="8"),
        
        # Formulario de alta
        rx.card(
            rx.vstack(
                rx.text("Nuevo Contrato", weight="bold"),
                # En gestion_contratos.py dentro del rx.hstack
                rx.hstack(
                    rx.select(
                        ContratoState.nombres_inquilinos,
                        placeholder="Inquilino",
                        on_change=ContratoState.set_inquilino_id_por_nombre
                    ),
                    rx.select(
                        ContratoState.direcciones_bienes_disponibles,
                        placeholder="Propiedad",
                        on_change=ContratoState.set_bien_id_por_direccion
                    ),
                    rx.vstack(
                        rx.text("Inicio", size="1"),
                        rx.input(
                            type="date", 
                            value=ContratoState.fecha_inicial, # Vinculado al state
                            on_change=ContratoState.set_fecha_inicial
                        ),
                    ),
                    rx.vstack(
                        rx.text("Vencimiento", size="1"),
                        rx.input(
                            type="date", 
                            value=ContratoState.fecha_final, # Vinculado al state
                            on_change=ContratoState.set_fecha_final
                        ),
                    ),
                    rx.button(
                        "Registrar Contrato", 
                        on_click=ContratoState.guardar_contrato,
                        margin_top="auto" # Alinea el botón con los inputs
                    ),
                    spacing="4",
                    align_items="end",
                ),

                width="100%",
            ),
            width="100%",
            padding="2em",
        ),
        
        # Tabla de resultados
        tabla_contratos(),
        
        spacing="6",
        padding="2em",
        on_mount=ContratoState.cargar_datos,
    )
