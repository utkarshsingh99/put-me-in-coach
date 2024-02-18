"""The terra API page."""
from webapp.templates import template
from pydantic import BaseModel
from fastapi import Request
import reflex as rx
from terra.base_client import Terra

API_KEY = "2pUWWW77QFq8ASsxcvt-CPGZA-_mf5z6"
DEV_ID = "coachme-testing-WfYIm4Ft6Z"
SECRET = "somesecret"
terraobj = Terra(API_KEY,DEV_ID, SECRET)

def terraLogin():
    """Login to Terra."""
    auth_resp = terraobj.generate_authentication_url(
        resource="GARMIN",
        auth_success_redirect_url="https://d07f-68-65-169-178.ngrok-free.app/terra", 
        auth_failure_redirect_url="https://d07f-68-65-169-178.ngrok-free.app"
    ).get_parsed_response()
    print(auth_resp)
    return rx.redirect(auth_resp.auth_url)


def prep_chart_data():
    import os
    # print(os.getcwd() + '/assets/activity_data.json')
    f = open(os.getcwd() + '/assets/activity_data.json')
    i = 0

@template(route="/terra", title="Get data from fitness apps")
def terra() -> rx.Component:
    """The terra page.

    Returns:
        The UI for the terra page.
    """
    # class TerraLoginState(rx.State):
    #     """The app state."""
    #     #yield
    #     auth_resp = terraobj.generate_authentication_url(
    #         	resource="GARMIN",auth_success_redirect_url="/terra"
    #         ).get_parsed_response()
    #     rx.redirect(auth_resp.auth_url)

    #     def terraLogin(self):
    #         """Login to Terra."""
            
    prep_chart_data()     
    return rx.chakra.vstack(
        rx.chakra.heading("Wearable Data Integrations", font_size="3em"),
        rx.chakra.text("Load in activity data from your favorite wearables!"),
        rx.button("Connect with Terra to Garmin", on_click=terraLogin, width="25em"),
        rx.chakra.text(
            "You can edit this page in ",
            rx.chakra.code("{your_app}/pages/terra.py"),
        ),
    )

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
