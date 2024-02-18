"""The dashboard page."""
from webapp.templates import template

import os
import reflex as rx
from reflex import html

style={
    '.canvas-style': {
        'width': '50%',
        'color': 'red',
        'background-color': 'red'
    }
}

# config = rx.Config(
#     app_name="reflexwebapp",
#     db_url="mysql://root:fractal@localhost/treehacks",
# )

# class Users(rx.Model, table=True):
#     username: str
#     email: str
#     password: str

# with rx.session() as session:
#     session.add(
#         Users(
#             username="test",
#             email="admin@pynecone.io",
#             password="admin",
#         )
#     )
#     session.commit()


@template(route="/dashboard", title="Visualize your form")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.chakra.vstack(
        rx.chakra.heading("Dashboard", font_size="3em"),
        rx.chakra.text("This will be the place for Spatial Visualization!"),
        # rx.chakra.text(
        #     "You can edit this page in ",
        #     rx.chakra.code("{your_app}/pages/dashboard.py"),
        # ),
        rx.hstack(
            rx.box(
                rx.text('Reference shot'),
                rx.html(
                    "<img src='/scatter.gif' />"),
                ),
            rx.box(
                rx.text('Your shot'),
                rx.html(
                    "<img src='/scatter1.gif' />"
                )
            )
        )
        # rx.box(
        #     # rx.html("<div id=\"canvas\">Hello World</div>"),
        #     rx.text('Hey! Look at me'),
        #     id="canvas_id_123",
        #     width='700px',
        #     height='500px',
        #     backgroundColor="black",
        #     color="red"),
        # rx.script(src="/main.js", custom_attrs={"type": "module"})
    )
