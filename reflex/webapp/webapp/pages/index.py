"""The home page of the app."""

from webapp import styles
from webapp.templates import template

import reflex as rx


@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return rx.chakra.vstack(
        rx.chakra.heading("Put me in, coach!", font_size="3em"),
        rx.chakra.text("Identify problems with your athletic form"),
        rx.chakra.text(
            "From your free throw shot to your overhead press, make sure that you are performing sport and athletic movements the right way. Track your workout history, watch tutorials, and get live AI-generated personal training to coach you on how you're moving.",
            # rx.chakra.code("{your_app}/pages/dashboard.py"),
        ),
    )
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
