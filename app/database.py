import reflex as rx
from rxconfig import config

def get_session():
    return rx.session(config)
