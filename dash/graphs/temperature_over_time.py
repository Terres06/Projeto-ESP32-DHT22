from dash import dcc, html
import plotly.express as px


def render_temperature_over_time(sensor_readings):
	if not isinstance(sensor_readings, list):
		return html.Div("Unable to load temperature chart data")

	temperatures = []
	timestamps = []

	for reading in sensor_readings:
		temperature = reading.get("temperature")
		timestamp = reading.get("timestamp")

		if temperature is None or timestamp is None:
			continue

		temperatures.append(temperature)
		timestamps.append(timestamp)

	if not temperatures:
		return html.Div("No temperature data available for chart")

	figure = px.line(
		x=timestamps,
		y=temperatures,
		labels={"x": "Time", "y": "Temperature (°C)"},
		title="Temperature Over Time",
	)

	return dcc.Graph(figure=figure)