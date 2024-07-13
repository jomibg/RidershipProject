from bokeh.models import ColumnDataSource
from data_processing import filter_ridership_data
from datetime import datetime as dt
def create_ridership_update_function(ridership_month, heatmap_source, stops_source, year_input, month_input, hour_slider):
    def update(attr, old, new):
        selected_year = int(year_input.value)
        selected_month = int(month_input.value)
        selected_hour = hour_slider.value

        filtered_df, filtered_stops = filter_ridership_data(ridership_month, selected_year, selected_month, selected_hour)

        heatmap_source.data.update(ColumnDataSource.from_df(filtered_df.drop(columns=['origin', 'destination'])))

        stops_source.data.update({
            'x': filtered_stops['x'],
            'y': filtered_stops['y'],
            'Station': filtered_stops['Station'],
            'trip_count_o': filtered_stops['trip_count_o'],
            'trip_count_d': filtered_stops['trip_count_d'],
            'total_count': filtered_stops['total_count']
        })

    return update

def create_histogram_update_function(date_picker, hist_source, read_function):
    def update(event):
        selected_date = dt.strptime(date_picker.value, '%Y-%m-%d')
        selected_year = selected_date.year
        selected_month = selected_date.month
        selected_day = selected_date.day
        new_data = read_function(selected_year, selected_month, selected_day)
        hist_source.data.update(ColumnDataSource.from_df(new_data))

    return update
