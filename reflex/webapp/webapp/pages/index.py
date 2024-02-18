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
        rx.chakra.text("Identify problems with your basketball skills"),
        rx.chakra.text(
            "Some more things about this project...",
            # rx.chakra.code("{your_app}/pages/dashboard.py"),
        ),
    )
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
