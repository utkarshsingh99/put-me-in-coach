"""The terra API page."""
from webapp.templates import template
from pydantic import BaseModel
from fastapi import Request
import reflex as rx
import os, json
from zoneinfo import ZoneInfo
from terra.base_client import Terra
from datetime import datetime, timedelta

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

timestamps = []
t = datetime.now(tz=ZoneInfo("America/Los_Angeles")) - timedelta(minutes=30)
for i in range(12):
    timestamps.append(datetime.strftime(t, '%H:%M'))
    t = t + timedelta(minutes=5)

print(timestamps)

def prep_chart_data():
    json_file_path =  os.getcwd() + '/assets/activity_data.json'
    with open(json_file_path, 'r') as json_file:
        data_dict = json.load(json_file)

# # Your nested JSON data
# nested_json = {
#     "all_data": [
#         {
#             "data": [
#                 {
#                     "active_durations_data": {"activity_seconds": 123}
#                 },
#                 # Add more entries as needed
#             ]
#         },
#         # Add more entries as needed
#     ]
# }

    # Extracting the relevant information and creating the desired format
    result = []
    tsind = 0

    for entry in data_dict.get("all_data", []):
        for data_entry in entry.get("data", []):
            active_durations_data = data_entry.get("active_durations_data", {})
            activity_seconds = active_durations_data.get("activity_seconds", None)

            if activity_seconds is not None:
                result.append({"timestamp": timestamps[tsind], "activity_seconds": activity_seconds})
                tsind += 1

    # Print the result
    return result



@template(route="/terra", title="Wearable data integrations")
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
            
    result = prep_chart_data()     
    return rx.chakra.vstack(
        rx.chakra.heading("Wearable Data Integrations", font_size="3em"),
        rx.chakra.text("Load in activity data from your favorite wearables!"),
        # rx.button("Connect with Terra to Garmin", on_click=terraLogin, width="25em"),
        rx.recharts.area_chart(
            rx.recharts.area(
                data_key="activity_seconds", stroke="#8884d8", fill="#8884d8"
            ),
            rx.recharts.x_axis(data_key="timestamp"),
            rx.recharts.y_axis(),
            data=result,
        )
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
