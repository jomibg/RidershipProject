from bokeh.models import TextInput, Slider, DatePicker, Button


def create_month_summary_widgets():
    year_input = TextInput(title="Year", value="2011")
    month_input = TextInput(title="Month", value="5")
    hour_slider = Slider(start=0, end=23, value=7, step=1, title="Hour")

    return year_input, month_input, hour_slider


def create_specific_date_widgets():
    date_picker = DatePicker(
        title="Select date",
        value="2011-01-01",
        min_date="2011-01-01",
        max_date="2023-05-23",
    )
    hour_slider = Slider(start=0, end=23, value=7, step=1, title="Hour")
    button = Button(label="Display", button_type="success")

    return date_picker, hour_slider, button
