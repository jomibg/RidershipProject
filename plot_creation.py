from bokeh.models import (ColumnDataSource, ColorBar, BasicTicker, Legend,
                          LegendItem, HoverTool, NumeralTickFormatter)
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
import xyzservices.providers as xyz


def create_ridership_heatmap(ridership_info, heatmap_source):
    hm = figure(x_range=ridership_info['Origin Stations'],
                y_range=ridership_info['Destination Stations'],
                title="Trip Count Heatmap",
                tools="hover",
                tooltips=[("Trip count", "@trip_count")],
                toolbar_location=None)

    mapper = linear_cmap(field_name='trip_count', palette=Viridis256,
                         low=ridership_info['Trip Count Range'][0],
                         high=ridership_info['Trip Count Range'][1])

    hm.xaxis.major_label_orientation = 1.0
    hm.rect(x="Origin Station", y="Destination Station", width=1, height=1, source=heatmap_source,
            line_color=None, fill_color=mapper)

    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0, 0),
                         ticker=BasicTicker(desired_num_ticks=10))
    hm.add_layout(color_bar, 'right')

    return hm


def create_route_map(shape_routes, stops_source, color_range):
    m = figure(x_axis_type="mercator", y_axis_type="mercator", title="Routes Map", width=800, height=600,
               tools=("wheel_zoom", "pan"),
               toolbar_location="below",
               active_drag="pan")

    route_renderers = []
    for i, route in shape_routes.iterrows():
        source = ColumnDataSource(data=dict(
            x=[route['x']],
            y=[route['y']],
            route_short_name=[route['route_short_name']],
            route_color=[route['route_color']]
        ))
        renderer = m.multi_line(xs='x', ys='y', source=source, line_color='route_color', line_width=5, line_alpha=0.6)
        route_renderers.append(renderer)

    m.x_range.range_padding = 0.1
    m.y_range.range_padding = 0.1

    mapper = linear_cmap(field_name='total_count', palette=Viridis256,
                         low=color_range[0],
                         high=color_range[1])
    stop_renderer = m.scatter(x='x',
                              y='y',
                              source=stops_source,
                              fill_color=mapper,
                              line_color="white",
                              size=10,
                              fill_alpha=0.8)
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0, 0),
                         ticker=BasicTicker(desired_num_ticks=10))
    m.add_layout(color_bar, 'right')

    stop_hover = HoverTool(renderers=[stop_renderer])
    stop_hover.tooltips = [("Stop Name", "@Station"), ("Departures", "@trip_count_o"), ("Arrivals", "@trip_count_d")]
    m.add_tools(stop_hover)

    legend_items = []
    for renderer, route_name in zip(route_renderers, shape_routes['route_short_name']):
        legend_item = LegendItem(label=f"Route {route_name}", renderers=[renderer])
        legend_items.append(legend_item)

    legend = Legend(items=legend_items, click_policy="hide")
    m.add_layout(legend, 'right')
    m.legend.click_policy = "hide"

    m.add_tile(xyz.CartoDB.DarkMatter)

    return m

def create_departure_histogram(hour_departures):
    hist = figure(x_range=(0, 24), title='Trip departures distribution',width=800, height=600   )
    hist.vbar(x='Hour', top='Trip Count', source=hour_departures, width=0.8)
    hist.yaxis.formatter = NumeralTickFormatter(format='0,0')
    hist.ygrid.grid_line_color = None
    hist.xgrid.grid_line_color = None

    return hist