"""The settings page."""

from webapp.templates import template

import reflex as rx


@template(route="/settings", title="Learning Materials")
def settings() -> rx.Component:
    """The settings page.

    Returns:
        The UI for the settings page.
    """
    return rx.chakra.vstack(
        rx.chakra.heading("Learning Materials", font_size="3em"),
        rx.grid(
            rx.foreach(
                rx.Var.range(12),
                # lambda i: rx.card(f"Card {i + 1}", height="10vh"),
                lambda i: rx.html("""
                    <iframe width="420" height="315"
                        src="https://www.youtube.com/embed/pq4DdAqX3yg">
                    </iframe>
                """)
            ),
            columns="3",
            spacing="4",
            width="100%",
        )
    )
