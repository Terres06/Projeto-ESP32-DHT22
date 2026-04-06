from dash import html 

def render_most_readings_device(most_read_device_id, readings_count):
    return html.Div(
        children=[
            html.H3("Device with Most Readings"),
            html.P(f"Device ID: {most_read_device_id}"),
            html.P(f"Readings Count: {readings_count}")
        ],
        style={
            "border": "1px solid #ccc",
            "borderRadius": "8px",
            "padding": "16px",
        }
    )