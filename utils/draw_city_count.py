# -*- coding: GBK -*-
import folium
import geopandas as gpd
import pandas as pd
from folium import Element
import sys

database = sys.argv[1]
output = sys.argv[2]

print("reading geojson data")
data = gpd.read_file(f'{database}\\中国_市.geojson')
print("reading citycount")
citydata = pd.read_excel(f'{database}\\途径市.xlsx',sheet_name=0,index_col = 0)


# 创建底图
base_map = folium.Map(
    location=[35.0, 105.0],
    tiles='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    attr="&copy; <a href='https://stadiamaps.com/' target='_blank'>Stadia Maps</a> &copy; <a href='https://openmaptiles.org/' target='_blank'>OpenMapTiles</a> &copy; <a href='https://www.openstreetmap.org/copyright' target='_blank'>OpenStreetMap</a>&copy; <a href='https://stamen.com/' target='_blank'>Stamen Design</a>",
    zoom_start=5
)

# 自定义样式函数（根据字段修改颜色等）
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
    if citydata.loc[name,'住居']==1:
        return {
            'fillColor': '#E57373',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,'宿泊']==1:
        return {
            'fillColor': '#FFF176',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,'访问']==1:
        return {
            'fillColor': '#81C784',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,'接地']==1:
        return {
            'fillColor': '#4FC3F7',
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0.6
        }
    elif citydata.loc[name,'途径']==1:
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

# 可选：添加 tooltip 显示字段（如县名）
tooltip = folium.GeoJsonTooltip(
    fields=['name'],       # 替换为你的 GeoJSON 中的字段名，如 '县名'
    aliases=['城市:'],      # 显示中文别名
    localize=True
)

# 添加 GeoJson 图层
folium.GeoJson(
    data,
    name='地级区域',
    style_function=style_function,
    tooltip=tooltip
).add_to(base_map)

# 保存地图
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
    <b>城市分类图例</b><br>
    <i style="background:#E57373; width:10px;height:10px;display:inline-block;"></i> 居住<br>
    <i style="background:#FFF176; width:10px;height:10px;display:inline-block;"></i> 住宿<br>
    <i style="background:#81C784; width:10px;height:10px;display:inline-block;"></i> 到访<br>
    <i style="background:#4FC3F7; width:10px;height:10px;display:inline-block;"></i> 换乘<br>
    <i style="background:#BAA6D0; width:10px;height:10px;display:inline-block;"></i> 途径<br>
    <i style="background:#dddddd; width:10px;height:10px;display:inline-block;"></i> 未途径
</div>
"""

base_map.get_root().html.add_child(Element(legend_html))

# 保存地图
base_map.save(f"{output}\\map_city.html")

