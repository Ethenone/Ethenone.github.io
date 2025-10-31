# -*- coding: GBK -*-
import json
import pandas as pd
import folium
import sys

database = sys.argv[1]
output = sys.argv[2]
print("reading airports data")
airportdata = pd.read_csv(f'{database}//airports_data.csv',encoding='gb18030')
#airportdata.head()
airportgeo = {}
for i in range(len(airportdata)):
    airportgeo[airportdata['iata'][i]]=[airportdata['lat'][i],airportdata['lon'][i]]
#print(airportgeo)


print("reading flight travel record")
data = pd.read_excel(f'{database}//�ɻ�������¼.xlsx', sheet_name = 0)
#data.head()

print("reading station data")
statdata = pd.read_csv(f'{database}//stations_data.csv',encoding='gbk')
#statdata.head()
statgeo = {}
for i in range(len(statdata)):
    lat = statdata['γ��'][i]
    lng = statdata['����'][i]
    loc = [lat,lng]
#     loc = correct(loc)
    statgeo[statdata['��վ'][i]]=loc
#print(statgeo)    

print("reading train travel record")
data2 = pd.read_excel(f'{database}//�𳵳�����¼.xlsx', sheet_name = 0)
#data2.head()


print("drawing map")
m = folium.Map(location=airportgeo['SHA'],
               zoom_start=5,
               control_scale=True,
               control=False,
               tiles=None
              )

folium.TileLayer(tiles='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                 attr="&copy; <a href='https://stadiamaps.com/' target='_blank'>Stadia Maps</a> &copy; <a href='https://openmaptiles.org/' target='_blank'>OpenMapTiles</a> &copy; <a href='https://www.openstreetmap.org/copyright' target='_blank'>OpenStreetMap</a>&copy; <a href='https://stamen.com/' target='_blank'>Stamen Design</a>",
                 min_zoom=0,
                 max_zoom=19,
                 control=True,
                 show=True,
                 overlay=False,
                 name='transportation'
                ).add_to(m)

group_air = folium.FeatureGroup(name='air')
for i in range(len(data)):
    start = airportgeo[data['start'][i]]
    end = airportgeo[data['depart'][i]]
    if start[1] < 0:
        start[1] += 360
    if end[1] < 0:
        end[1] += 360
    # �������򾭶Ȼ���
    folium.PolyLine(
        locations = [start,end],
        color='red',
        weight=3,
        opacity=0.3
    ).add_to(group_air)
    
    
    folium.Circle(
        location=start,
        radius=9000,   # Բ�İ뾶
        popup=folium.Popup(data['���'][i],max_width=10),
        color='red', #'#FF1493',
        fill=True,
        fill_color='#FFD700'
    ).add_to(group_air)
    
    folium.Circle(
        location=end,
        radius=9000,   # Բ�İ뾶
        popup=folium.Popup(data['����'][i],max_width=10),
        color='red', #'#FF1493',
        fill=True,
        fill_color='#FFD700'
    ).add_to(group_air)

group_air.add_to(m)

group_train = folium.FeatureGroup(name='train')
for i in range(len(data2)):
    folium.PolyLine(
        locations = [
            statgeo[data2['�ϳ�վ'][i]],statgeo[data2['�³�վ'][i]]
        ],
        color='blue',
        weight=3,
        opacity=0.3
    ).add_to(group_train)
    folium.Circle(
        location=statgeo[data2['�ϳ�վ'][i]],
        radius=9000,   # Բ�İ뾶
        popup=folium.Popup(data2['�ϳ�վ'][i],max_width=10),
        color='blue', #'#FF1493',
        fill=True,
        fill_color='#FFD700'
    ).add_to(group_train)
    folium.Circle(
        location=statgeo[data2['�³�վ'][i]],
        radius=9000,   # Բ�İ뾶
        popup=folium.Popup(data2['�³�վ'][i],max_width=10),
        color='blue', #'#FF1493',
        fill=True,
        fill_color='#FFD700'
    ).add_to(group_train)

group_train.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)
m.save(f'{output}//map_line.html')