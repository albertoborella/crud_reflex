import reflex as rx
from app.models import BienAlquilado
from app.pages.gestion_contratos import gestion_contratos_page
from app.pages.total_bienes import total_bienes
from app.pages.inquilinos import inquilinos
from app.states.ContratoState import ContratoState
from app.states.InquilinoState import InquilinoState
from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Título con sombra para que resalte sobre el fondo
            rx.heading(
                "Gestión de Alquiler de Inmuebles", 
                font_family="Montserrat",
                size="8", 
                margin_bottom="1.5em",
                color="white",
                text_shadow="2px 2px 4px rgba(0,0,0,0.3)"
            ),
            rx.hstack(
                rx.link(
                    rx.card(
                        rx.vstack(
                            rx.icon("layers", size=30), # Iconos opcionales para más estilo
                            rx.heading("Cobranzas", size="4"),
                            align="center",
                        ),
                        padding="2em",
                        _hover={"transform": "scale(1.05)", "transition": "0.2s"},
                    ),
                    href="/bienes",
                ),
                rx.link(
                    rx.card(
                        rx.vstack(
                            rx.icon("file-text", size=30),
                            rx.heading("Contratos", size="4"),
                            align="center",
                        ),
                        padding="2em",
                        _hover={"transform": "scale(1.05)", "transition": "0.2s"},
                    ),
                    href="/contratos",
                ),
                rx.link(
                    rx.card(
                        rx.vstack(
                            rx.icon("users", size=30),
                            rx.heading("Inquilinos", size="4"),
                            align="center",
                        ),
                        padding="2em",
                        _hover={"transform": "scale(1.05)", "transition": "0.2s"},
                    ),
                    href="/inquilinos",
                ),
                spacing="6",
                justify="center",
            ),
            align="center",
        ),
        width="100%",
        height="100vh",
        # FONDO PROFESIONAL: Un degradado entre azul oscuro y petróleo
        background="linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
    )


    



app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com",
    ],
)
app.add_page(index)
app.add_page(total_bienes, route="/bienes")
app.add_page(inquilinos, route="/inquilinos", on_load=InquilinoState.get_inquilinos)
app.add_page(gestion_contratos_page, route="/contratos", on_load=ContratoState.cargar_datos)
