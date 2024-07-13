from bokeh.models import Div
from bokeh.layouts import column


def create_welcome_page():
    welcome_text = Div(text="""
        <h1>Welcome to the Ridership Visualization</h1>
        <p>This application visualizes ridership data. Use the navigation bar above to switch between views.</p>
        <p>Click on 'Main Visualization' to see the average day in month/year view.</p>
    """, width=800)

    return column(welcome_text)
