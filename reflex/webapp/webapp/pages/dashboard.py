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

result = '0'
with open('/Users/utkarshsingh/Desktop/Projects/put-me-in-coach/ml_results.txt') as f:
    result = f.read()
    print(result)

result_dict = {
    '0': 'Good shot!',
    '1': 'Good form!',
    '2': 'Forearm was too flat, you need to make sure your forearm has an approximate 90-degree perpendicular direction to your big arm',
    '3': "Push shot. Your release point is rght in front of your chest, and you're releasing the ball from pushing. \
    Suggestions: you should 1). move up your release point form your chest to your head; 2). use your wrist to spin the ball instead of pushing forward.",
    '4': 'Bad weightlifting, too forward',
        '5': 'Bad weightlifting, too backward',
            '6': 'Bad weightlifting, too outward',
}

@template(route="/dashboard", title="Visualize your form")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.chakra.vstack(
        rx.chakra.heading("Form Analysis", font_size="3em"),
        rx.chakra.text("Based on our wearable sleeve, here's how your form compares to the pros!"),
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
        ),
        rx.badge("Machine Learning based feedback"),
        rx.text(result_dict[result])
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
