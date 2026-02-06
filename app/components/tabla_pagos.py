import reflex as rx
from app.states.BienesAlquilerState import BienesAlquilerState


def tabla_pagos():

    def fila_bien(bien):
        return rx.table.row(
            rx.table.row_header_cell(
                rx.moment(bien.mes_anio, format="MM/YYYY")
            ),
            rx.table.cell(bien.nombre),
            rx.table.cell(bien.direccion),
            rx.table.cell(f"$ {bien.precio_mensual:,.2f}"),
            rx.table.cell(
                rx.cond(
                    bien.fecha_pago_mensual,
                    rx.moment(bien.fecha_pago_mensual, format="DD/MM/YYYY"),
                    "Sin fecha de pago"
                )
            ),
            rx.table.cell(
                rx.cond(
                    bien.observaciones != "",
                    bien.observaciones,
                    "Sin observaciones"
                )
            ),
            rx.table.cell(
                rx.hstack(
                    rx.icon(
                        "pencil",
                        cursor="pointer",
                        color="blue",
                        size=15,
                        on_click=BienesAlquilerState.cargar_registro(bien.id),
                    ),
                    rx.icon(
                        "trash",
                        cursor="pointer",
                        color="red",
                        size=15,
                        on_click=BienesAlquilerState.delete_registro(bien.id),
                    ),
                    spacing="3",
                    justify="center",
                )

                # rx.button(
                #     rx.cond(
                #         BienesAlquilerState.modo_edicion,
                #         "Actualizar",
                #         "Guardar"
                #     ),
                #     type="submit"
                # )
            )
        )

    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Mes y Año"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Dirección"),
                rx.table.column_header_cell("Precio Mensual"),
                rx.table.column_header_cell("Fecha Pago Mensual"),
                rx.table.column_header_cell("Observaciones"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(
                BienesAlquilerState.bienes, fila_bien
            )
        ),
        width="100%"
    )
        
        
        
    