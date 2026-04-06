from dash import Dash, html
from cards.average_temperature import render_average_temperature
from cards.most_readings_device import render_most_readings_device
from graphs.temperature_over_time import render_temperature_over_time
import requests

app = Dash(__name__)

#get data from API
avg_response = requests.get("http://localhost:8000/average-reading")
avg_data = avg_response.json()

most_response = requests.get("http://localhost:8000/most-readings-device")
most_read_data = most_response.json()

sensor_response = requests.get("http://localhost:8000/sensor-readings")
sensor_readings = sensor_response.json()

app.layout = html.Div(
    children=[
        html.Div("DHT22 Sensor Dashboard"),
        html.Div(
            children=[
                html.Div(
                    render_temperature_over_time(sensor_readings),
                    style={"flexGrow": 3}
                ),
                html.Div(
                    children=[
                        render_average_temperature(avg_data["average_temperature"]),
                        render_most_readings_device(most_read_data["most_read_device_id"], most_read_data["readings_count"])
                    ],
                    style={"flexGrow": 1}
                )
            ],
            style={"display": "flex"}
        )
    ]
)


if __name__ == "__main__":
    app.run(debug=True)