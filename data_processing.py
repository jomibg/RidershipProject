import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def load_and_process_ridership_data():
    # Load and process files
    ridership_month = pd.read_csv("ridership_month_year.csv")
    shape_routes = gpd.read_file("shape_routes.geojson")

    # Process shape_routes
    shape_routes['x'] = shape_routes.apply(lambda row: [point[0] for point in row['geometry'].coords], axis=1)
    shape_routes['y'] = shape_routes.apply(lambda row: [point[1] for point in row['geometry'].coords], axis=1)

    # Process ridership_month
    ridership_month['origin'] = ridership_month.apply(lambda row: {'x': row['origin_lon'], 'y': row['origin_lat']},
                                                      axis=1)
    ridership_month['destination'] = ridership_month.apply(
        lambda row: {'x': row['destination_lon'], 'y': row['destination_lat']}, axis=1)
    ridership_month.drop(columns=['origin_lat', 'origin_lon', 'destination_lat', 'destination_lon'], inplace=True)

    return ridership_month, shape_routes


def filter_ridership_data(ridership_month, year, month, hour):
    # Filter ridership and stops information
    filtered_df = ridership_month[(ridership_month['Year'] == year) &
                                  (ridership_month['Month'] == month) &
                                  (ridership_month['Hour'] == hour)]

    # Process filtered data
    filtered_origins = filtered_df.rename(
        columns={'Origin Station': 'Station', 'origin': 'location'}
    ).groupby('Station').agg({'trip_count': 'sum', 'location': 'first'}).reset_index()

    filtered_destinations = filtered_df.rename(
        columns={'Destination Station': 'Station'}
    ).reset_index().groupby('Station').agg({'trip_count': 'sum'})

    # Merge and create GeoDataFrame
    filtered_stops = filtered_destinations.merge(filtered_origins, how='inner', on='Station', suffixes=['_d', '_o'])
    filtered_stops['geometry'] = filtered_stops['location'].apply(lambda loc: Point(loc['x'], loc['y']))
    filtered_stops['total_count'] = filtered_stops['trip_count_o'] + filtered_stops['trip_count_d']
    filtered_stops = gpd.GeoDataFrame(filtered_stops, geometry='geometry', crs=4326)
    filtered_stops.to_crs("EPSG:3857", inplace=True)
    filtered_stops['x'] = filtered_stops.geometry.x
    filtered_stops['y'] = filtered_stops.geometry.y

    return filtered_df, filtered_stops

def process_daily_ridership_data(year, month, day):
    ridership = pd.read_csv(f'ridership_merged/ridership{year}.csv')
    ridership_filtered = ridership[(ridership['Month'] == month) & (ridership['Day'] == day)]
    hour_departures = ridership_filtered.groupby('Hour').agg({'Trip Count': 'sum'}).reset_index()

    return hour_departures