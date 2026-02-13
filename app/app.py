import reflex as rx
from app.models import BienAlquilado
from app.pages.total_bienes import total_bienes
from app.pages.inquilinos import inquilinos
from app.states.InquilinoState import InquilinoState
from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            #justify="center",
            min_height="85vh",
        ),
    )



app = rx.App()
app.add_page(index)
app.add_page(total_bienes, route="/bienes")
app.add_page(inquilinos, route="/inquilinos", on_load=InquilinoState.get_inquilinos)
