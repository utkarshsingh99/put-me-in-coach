"""The terra API page."""
from webapp.templates import template
from pydantic import BaseModel
from fastapi import Request
import reflex as rx

@template(route="/terra", title="Get data from Fitness Apps")
def terra() -> rx.Component:
    """The terra page.

    Returns:
        The UI for the terra page.
    """
    return rx.chakra.vstack(
        rx.chakra.heading("Fitness App", font_size="3em"),
        rx.chakra.text("Look at data sourced from other fitness apps of the user"),
        rx.chakra.text(
            "You can edit this page in ",
            rx.chakra.code("{your_app}/pages/terra.py"),
        ),
    )


# class Item(BaseModel):
#     daily: dict
#     body: dict | None = None

data = []

async def api_test(req: Request):
    data.append(await req.json())
    print(len(data))
    return "OK"

# @template(route="/terrawebhook", title="TerraAPI")
# def terrawebhook() -> rx.Component:
#     return rx.chakra.hstack(
#         rx.text('Thank you')
#     )