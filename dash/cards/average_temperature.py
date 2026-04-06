from dash import html

def render_average_temperature(average_temperature):
    formatted_temperature = "N/A"
    if average_temperature is not None:
        formatted_temperature = f"{average_temperature:.2f}".replace(".", ",")

    return html.Div(
        children=[
            html.H3("Average Temperature (30 days)"),
            html.P(f"{formatted_temperature}°C")
        ],
        style={
            "border": "1px solid #ccc",
            "borderRadius": "8px",
            "padding": "16px",
        }
    )