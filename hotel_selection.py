# %%
import pandas as pd
import numpy as np
import folium
import math
from math import pi
from folium.plugins import HeatMap
import sys
from GPSPhoto import gpsphoto

# %%
def get_coordinate(filename):
    return gpsphoto.getGPSData(filename)

# %%
# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def deg2rad(deg):
    return deg*(math.pi/180)
def distance(lat1, lon1, lat2, lon2):
    p = pi / 180
    a = 0.5-np.cos((lat2 - lat1) * p)/2 + np.cos(lat1 * p) * np.cos(lat2 * p) * (1 - np.cos((lon2 - lon1) * p)) / 2
    result = 12742*np.arcsin(np.sqrt(a))*1000
   
    return result

# %%
# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)



# %%
def get_desire_amenity(df,category):
    for i in range(len(df.index)):
        df = df[df['amenity'] == category]
    return df
  
def position_inrange(lat1,lon1,category):
        lat2 = category[1]       
        lon2 = category[2]
        d = distance(lat1, lon1, lat2, lon2)
        if d < 500:
            return True
def position_amen_inrange(lat,lon,amen):
        lat2 = amen[0]       
        lon2 = amen[1]
        d = distance(lat, lon, lat2, lon2)
        if d < 500:
            return True

# %%
def get_similar(df):
    df['amenity'] = df['amenity'].replace(['parking_entrance'], 'parking')
    df['amenity'] = df['amenity'].replace(['pub'], 'bar')
    df['amenity'] = df['amenity'].replace(['childcare'], 'kindergarten')
    df['amenity'] = df['amenity'].replace(['nightclub'], 'bar')
    df['amenity'] = df['amenity'].replace(['gambling'], 'casino')
    df['amenity'] = df['amenity'].replace(['atm;bank'], 'bank')
    df['amenity'] = df['amenity'].replace(['motorcycle_parking'], 'parking')
    df['amenity'] = df['amenity'].replace(['drinking_water'], 'fountain')
    df['amenity'] = df['amenity'].replace(['doctors'], 'hospital')
    df['amenity'] = df['amenity'].replace(['storage'], 'storage_rental')
    df['amenity'] = df['amenity'].replace(['internet_cafe'], 'cafe')
    df['amenity'] = df['amenity'].replace(['chiropractor'], 'hospital')
    df['amenity'] = df['amenity'].replace(['post_depot'], 'post_office')
    df['amenity'] = df['amenity'].replace(['Pharmacy'], 'pharmacy')
    df['amenity'] = df['amenity'].replace(['ferry_terminal'], 'bus_station')
    df['amenity'] = df['amenity'].replace(['car_rental'], 'traffic')
    df['amenity'] = df['amenity'].replace(['car_sharing'], 'traffic')
    df['amenity'] = df['amenity'].replace(['bicycle_rental'], 'traffic')
    df['amenity'] = df['amenity'].replace(['taxi'], 'traffic')
    df['amenity'] = df['amenity'].replace(['boat_rental'], 'traffic')
    df['amenity'] = df['amenity'].replace(['food_court'], 'restaurant')
    df['amenity'] = df['amenity'].replace(['motorcycle_rental'], 'traffic')
    return df

# %%
def split_on_map(data,van_map):
    food_lst = ['cafe','restaurant', 'fast_food','traffic']
    trans_lst = ['parking','bus_station','traffic']
    enter_lst = ['pub', 'cinema','bar']
    shop_lst = ['atm', 'bank','marketplace']
    for index, row in data.iterrows():
        if row['amenity'] in food_lst:
            folium.Circle(
                radius=6,
                location=[row['lat'], row['lon']],
                color='red',
            ).add_to(van_map)
        if row['amenity'] in trans_lst:
            folium.Circle(
                radius=6,
                location=[row['lat'], row['lon']],
                color='yellow',
            ).add_to(van_map)
        if row['amenity'] in enter_lst:
            folium.Circle(
                radius=6,
                location=[row['lat'], row['lon']],
                color='blue',
            ).add_to(van_map)
        if row['amenity'] in shop_lst:
            folium.Circle(
                radius=6,
                location=[row['lat'], row['lon']],
                color='green',
            ).add_to(van_map)
            

# %%
def main(input_directory, output_directory):
    coordinate=get_coordinate(input_directory)
    lat=coordinate['Latitude']
    lon=coordinate['Longitude']
    
    raw_data_amen = pd.read_json('amenities-vancouver.json.gz', lines=True)
    hotel = pd.read_csv("listings.csv", encoding="utf-8",sep =',')
    addition_amen = pd.read_csv('additional_amenities.csv', encoding="utf-8",sep =',')
    van_map = folium.Map(location=[lat, lon], zoom_start=12)
    # cleaning amenities' data
    raw_data_amen = raw_data_amen[raw_data_amen['name'].notna()]
    raw_data_amen = raw_data_amen.drop(['timestamp','tags'], axis=1).reset_index(drop= True)
    cleaned_data_amen = get_similar(raw_data_amen)
    filter_amen = ['arts_centre','restaurant','bar','casino', 'cinema', 'clock',
        'museum','park','university','beach','theatre','lake', 'shopping_centre'
        ,'conference_centre','parking','cafe','fast_food','parking','bus_station','traffic']
    cleaned_data_amen = cleaned_data_amen[cleaned_data_amen['amenity'].isin(filter_amen) == True]
    addition_amen = addition_amen[addition_amen['amenity'].isin(filter_amen) == True]
    all_amen = pd.concat([cleaned_data_amen,addition_amen]).reset_index(drop = True)
    all_amen = all_amen.drop_duplicates()
    temp = []
    for amen in all_amen.itertuples(index=False):
        if position_amen_inrange(lat,lon,amen) == True:
            temp.append(amen)
    all_amen = pd.DataFrame(temp) 
    split_on_map(all_amen,van_map)
         
    # cleanig hotel's data
    # choose the relative new information
    hotel['last_review'] = pd.to_datetime(hotel['last_review'], errors='coerce')
    hotel = hotel[(hotel['reviews_per_month']>1)]
    cleaned_data_hotel = hotel.drop_duplicates()
    cleaned_data_hotel = cleaned_data_hotel.drop(['id', 'host_id','host_name','neighbourhood_group','neighbourhood'
                     ,'room_type','price','minimum_nights','number_of_reviews','last_review'
                     ,'reviews_per_month','calculated_host_listings_count','availability_365'
                     ], axis = 1)
    cleaned_data_hotel = cleaned_data_hotel.reset_index(drop=True)
    temp1 = []
    for item in cleaned_data_hotel.itertuples(index=False):
        if position_inrange(lat,lon,item) == True:
            temp1.append(item)
    cleaned_data_hotel = pd.DataFrame(temp1)
            
    # Show density graph of the amenities in Vancouver
    incidents = folium.map.FeatureGroup()
    # https://stackoverflow.com/questions/69816726/how-to-use-python-folium-marker-save-custom-information
    folium.Marker(
    location=[lat, lon],
    popup="My postion",
    icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(van_map)  
    incidents = folium.map.FeatureGroup()
    latitudes = list(cleaned_data_hotel.latitude)
    longitudes = list(cleaned_data_hotel.longitude)
    labels = list(cleaned_data_hotel.name)
    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng], popup=label).add_to(van_map)
    van_map.add_child(incidents)
    
    cleaned_data_hotel = cleaned_data_hotel.drop(['latitude','longitude'], axis = 1)
    
    van_map.save(outfile= "amenity_near_hotel.html")
    cleaned_data_hotel.to_csv(output_directory)
    

# %%
if __name__=='__main__':
    input_directory = sys.argv[1]
    output_directory = 'hotel_list'
    main(input_directory,output_directory)


