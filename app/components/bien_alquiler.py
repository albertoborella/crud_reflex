import reflex as rx
from app.states.BienesAlquilerState import BienesAlquilerState

def total_bienes_card(total_bienes: int) -> rx.Component:
    return rx.box(
        rx.text(f"Registros de cobros de alquileres - ({total_bienes})", color='green', font_size="25px", font_weight="bold"),

        margin_top="20px",
        margin_bottom="4px",
        padding="6px",
        height="50px",
        border="1px solid #ccc",
        border_radius="8px",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
        text_align="center",
        justify="center",
        max_width="600px",
        width="90%",
        bg="white",
    ),
    
