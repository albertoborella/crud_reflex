import reflex as rx
from app.states.InquilinoState import InquilinoState


def inquilinos():
    return rx.container(
        rx.heading("Agregar Inquilino", size="7", font_family="Arial",padding="15px"),
        
        # FORMULARIO
        rx.vstack(
            rx.input(
                #items=InquilinoState.inquilinos_opciones,
                #items=InquilinoState.inquilinos,
                placeholder="Ingrese un inquilino",
                value=InquilinoState.razon_social,
                on_change=InquilinoState.set_razon_social,
                width="100%",
            ),
            rx.input(
                placeholder="Domicilio",
                value=InquilinoState.domicilio,
                on_change=InquilinoState.set_domicilio,
                width="100%",
            ),
            rx.input(
                placeholder="Celular",
                value=InquilinoState.celular,
                on_change=InquilinoState.set_celular,
                width="100%",
            ),
            rx.select(
                ["Monotributo", "Responsable Inscripto", "Exento"],
                    value = InquilinoState.condicion_iva,
                    on_change = InquilinoState.set_value_condicion_iva,
                    placeholder="Condición IVA",
                    width="100%",
                ),
                
            rx.input(
                placeholder="CUIT",
                value=InquilinoState.cuit,
                on_change=InquilinoState.set_cuit,
                width="100%",
            ),
            
            ),

            rx.button(
                rx.cond(
                    InquilinoState.inquilino_id,
                    "Actualizar",
                    "Crear Nuevo Inquilino",
                ),
                on_click=rx.cond(
                    InquilinoState.inquilino_id,
                    InquilinoState.actualizar_inquilino,
                    InquilinoState.nuevo_inquilino,
                ),
            is_disabled=InquilinoState.razon_social == "",
            width="100%",
            margin_top="15px" 
            ),
            rx.divider(margin_top="10px"),

        #TABLA
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Razón Social", align="left"),
                    rx.table.column_header_cell("Tel. celular", align="right"),
                    rx.table.column_header_cell("CUIT", align="right"),
                    rx.table.column_header_cell("Condición", align="right"),
                    rx.table.column_header_cell("Acciones", align="right"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    InquilinoState.inquilinos,
                    lambda i: rx.table.row(
                        rx.table.cell(i.razon_social, font_size="14px", align="left"),
                        rx.table.cell(i.celular, font_size="14px", align='right'),
                        rx.table.cell(i.cuit, font_size="14px", align="right"),
                        rx.table.cell(i.condicion_iva, font_size="14px", align="right"),
                        rx.table.cell(
                            rx.hstack(
                                rx.icon(
                            "pencil",
                            on_click=lambda: InquilinoState.editar_inquilino(i.id),
                            size=16,
                            cursor="pointer",
                                ),
                                rx.icon(
                                    "trash",
                                    color="red",
                                    on_click=lambda: InquilinoState.eliminar_inquilino(i.id),
                                    size=16,
                                    cursor="pointer",
                                ),
                                justify="end",
                                spacing="2",
                            ),
                            align="right"
                        ),
                    ),
                ),
            ),
            width="100%"
        ),
    )
    
    
    
