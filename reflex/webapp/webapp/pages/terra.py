"""The terra API page."""
from webapp.templates import template
from pydantic import BaseModel
from fastapi import Request
import reflex as rx

@template(route="/terra", title="Import other wearables")
def terra() -> rx.Component:
    """The terra page.

    Returns:
        The UI for the terra page.
    """
    class State(rx.State):
    """The app state."""
        yield
        auth_resp = terra.generate_authentication_url(
            	resource="GARMIN",auth_success_redirect_url="/terra"
            ).get_parsed_response()
        rx.redirect(auth_resp['auth_url'])

        def terraLogin(self):
            """Login to Terra."""
            
                
    return rx.chakra.vstack(
        rx.chakra.heading("Wearable Data Integrations", font_size="3em"),
        rx.chakra.text("Load in activity data from your favorite wearables!"),
        rx.button("Connect with Terra to Garmin", on_click=State.terraLogin, width="25em"),
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
