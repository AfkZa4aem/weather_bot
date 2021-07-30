import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = os.environ.get("ACC_TWILIO_SID")
auth_token = os.environ.get("AUTH_TWILIO_TOKEN")

api_key = os.environ.get("OWM_API_KEY")
OMW_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
parameters = {
    "lat": 55.755825,
    "lon": 37.617298,
    "units": "metric",
    "exclude": "current,daily,minutely",
    "appid": api_key,
    "lang": "ru",
}

response = requests.get(url=OMW_endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

twelve_hours = weather_data["hourly"][:12]

cond_list = [cond_id["weather"][0]["id"] for cond_id in twelve_hours]

will_it_rain = False

for code in cond_list:
    if code < 700:
        will_it_rain = True

if will_it_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https": os.environ["https_proxy"]}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Bring an umbrella ☔",
        from_='Phone_number',
        to="Phone_number"
    )

print(message.status)

