import reflex as rx
import os
from dotenv import load_dotenv

# Esto asegura que busque el .env en la misma carpeta donde está este script
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

db_url = os.getenv("DATABASE_URL")

# Verificación rápida (solo para debug, después podés borrar el print)
if not db_url:
    print("⚠️ Error: No se pudo cargar DATABASE_URL del archivo .env")

config = rx.Config(
    app_name="app",
    db_url=db_url,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)


