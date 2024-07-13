from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Tabs, TabPanel

from data_processing import *
from plot_creation import *
from widgets import *
from update_function import *
from welcome_page import create_welcome_page

# Load and process data
monthly_ridership_data, route_shapes = load_and_process_ridership_data()
ridership_statistics = {
    'Origin Stations': monthly_ridership_data['Origin Station'].unique(),
    'Destination Stations': monthly_ridership_data['Destination Station'].unique(),
    'Trip Count Range': [monthly_ridership_data['trip_count'].min(), monthly_ridership_data['trip_count'].max()]
}

# Initial filtering
filtered_ridership_data, filtered_station_data = filter_ridership_data(monthly_ridership_data, 2011, 5, 7)

# Datetime info
hourly_departure_data = process_daily_ridership_data(2011, 1, 1)

# Create data sources
heatmap_data_source = ColumnDataSource(filtered_ridership_data.drop(columns=['origin', 'destination']))
station_data_source = ColumnDataSource(data={
    'x': filtered_station_data['x'],
    'y': filtered_station_data['y'],
    'Station': filtered_station_data['Station'],
    'trip_count_origin': filtered_station_data['trip_count_o'],
    'trip_count_destination': filtered_station_data['trip_count_d'],
    'total_count': filtered_station_data['total_count']
})
histogram_data_source = ColumnDataSource(hourly_departure_data)

# Create plots
heatmap = create_ridership_heatmap(ridership_statistics, heatmap_data_source)
map_plot = create_route_map(route_shapes, station_data_source, [filtered_station_data['total_count'].min(), filtered_station_data['total_count'].max()])
histogram = create_departure_histogram(histogram_data_source)

# Create widgets
year_input, month_input, hour_slider = create_month_summary_widgets()
date_picker, date_hour_slider, filter_button = create_specific_date_widgets()

# Create update functions
update_ridership_data = create_ridership_update_function(monthly_ridership_data, heatmap_data_source, station_data_source, year_input, month_input, hour_slider)
update_histogram_data = create_histogram_update_function(date_picker, histogram_data_source, process_daily_ridership_data)

# Add the update callbacks
year_input.on_change("value", update_ridership_data)
month_input.on_change("value", update_ridership_data)
hour_slider.on_change("value", update_ridership_data)
filter_button.on_click(update_histogram_data)

# Create layout of monthly information
monthly_data_layout = column(row(year_input, month_input), hour_slider, row(heatmap, map_plot))

# Create welcome page
welcome_layout = create_welcome_page()

# Create datetime info page
date_specific_layout = column(row(date_picker, filter_button), column(histogram, date_hour_slider))

# Create tabs
welcome_tab = TabPanel(child=welcome_layout, title="Welcome")
monthly_data_tab = TabPanel(child=monthly_data_layout, title="Monthly Ridership Information")
date_specific_tab = TabPanel(child=date_specific_layout, title="Date-Specific Information")

# Create tab layout
visualization_tabs = Tabs(tabs=[welcome_tab, monthly_data_tab, date_specific_tab])

# Add tabs to the document
curdoc().add_root(visualization_tabs)
curdoc().title = "Ridership Visualization"


