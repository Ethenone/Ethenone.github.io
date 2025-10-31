# -*- coding: GBK -*-
import folium
import geopandas as gpd
import pandas as pd
from folium import Element
import sys

database = sys.argv[1]
output = sys.argv[2]

print("reading geojson data")
data = gpd.read_file(f'{database}\\�й�_��.geojson')
print("reading citycount")
citydata = pd.read_excel(f'{database}\\;����.xlsx',sheet_name=0,index_col = 0)


# ������ͼ
base_map = folium.Map(
    location=[35.0, 105.0],
    tiles='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    attr="&copy; <a href='https://stadiamaps.com/' target='_blank'>Stadia Maps</a> &copy; <a href='https://openmaptiles.org/' target='_blank'>OpenMapTiles</a> &copy; <a href='https://www.openstreetmap.org/copyright' target='_blank'>OpenStreetMap</a>&copy; <a href='https://stamen.com/' target='_blank'>Stamen Design</a>",
    zoom_start=5
)

# �Զ�����ʽ�����������ֶ��޸���ɫ�ȣ�
def style_function(feature):
    name = feature['properties'].get('name', '')
    try:
        citydata.loc[name]
    except:
        return {
            'fillColor': '#dddddd',
            'color': 'gray',
            'weight': 0.5,
            'fillOpacity': 0.2
        }
    if citydata.loc[name,'ס��']==1:
        return {
            'fillColor': '#E57373',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,'�޲�']==1:
        return {
            'fillColor': '#FFF176',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,'����']==1:
        return {
            'fillColor': '#81C784',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,'�ӵ�']==1:
        return {
            'fillColor': '#4FC3F7',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,';��']==1:
        return {
            'fillColor': '#BAA6D0',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    else:
        return {
            'fillColor': '#dddddd',
            'color': 'gray',
            'weight': 0.5,
            'fillOpacity': 0.2
        }

# ��ѡ����� tooltip ��ʾ�ֶΣ���������
tooltip = folium.GeoJsonTooltip(
    fields=['name'],       # �滻Ϊ��� GeoJSON �е��ֶ������� '����'
    aliases=['����:'],      # ��ʾ���ı���
    localize=True
)

# ��� GeoJson ͼ��
folium.GeoJson(
    data,
    name='�ؼ�����',
    style_function=style_function,
    tooltip=tooltip
).add_to(base_map)

# �����ͼ
legend_html = """
<div style="
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    background-color: white;
    padding: 10px;
    border: 2px solid grey;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    font-size:14px;
">
    <b>���з���ͼ��</b><br>
    <i style="background:#E57373; width:10px;height:10px;display:inline-block;"></i> ��ס<br>
    <i style="background:#FFF176; width:10px;height:10px;display:inline-block;"></i> ס��<br>
    <i style="background:#81C784; width:10px;height:10px;display:inline-block;"></i> ����<br>
    <i style="background:#4FC3F7; width:10px;height:10px;display:inline-block;"></i> ����<br>
    <i style="background:#BAA6D0; width:10px;height:10px;display:inline-block;"></i> ;��<br>
    <i style="background:#dddddd; width:10px;height:10px;display:inline-block;"></i> δ;��
</div>
"""

base_map.get_root().html.add_child(Element(legend_html))

# �����ͼ
base_map.save(f"{output}\\map_city.html")

