import reflex as rx

config = rx.Config(
    app_name="app",
    db_url="sqlite:///alquileres.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)

