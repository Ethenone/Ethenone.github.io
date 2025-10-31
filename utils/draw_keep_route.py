# -*- coding: UTF-8 -*-
import json
import pandas as pd
import folium
import polyline
from folium import plugins
import datetime
import sys

database = sys.argv[1]
output = sys.argv[2]

print("reading activities data")
with open(f'{database}//activities.json','r') as file:
    data = json.load(file)

def transfer(loc):
    iloc = []
    for i in loc:
        iloc.append([i[0],i[1]])
    return iloc

m = folium.Map(location=[31.016832, 121.431093],
               zoom_start=5,
               control_scale=True,
               control=False,
               tiles=None
              )
print("drawing map")
folium.TileLayer(tiles='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                 attr="&copy; <a href='https://stadiamaps.com/' target='_blank'>Stadia Maps</a> &copy; <a href='https://openmaptiles.org/' target='_blank'>OpenMapTiles</a> &copy; <a href='https://www.openstreetmap.org/copyright' target='_blank'>OpenStreetMap</a>&copy; <a href='https://stamen.com/' target='_blank'>Stamen Design</a>",
                 min_zoom=0,
                 max_zoom=19,
                 control=True,
                 show=True,
                 overlay=False,
                 name='ss'
                ).add_to(m)
from collections import defaultdict
citysum = defaultdict(int)
for i in data:
    if not i['summary_polyline']:
        continue
    citystr = i['location_country'].replace("\'","\"").replace("None","\"None\"")
    #print(citystr)
    j = json.loads(citystr)
    citysum[j['city']] += i['distance']
    date = i['start_date_local']
    dt = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    if dt.year>2023:
        color = 'red'
    else:
        color = 'blue'
    pl = polyline.decode(i['summary_polyline'])
    folium.PolyLine(
        locations = transfer(pl),
        color = color,
        weight=3,
        opacity=0.5
    ).add_to(m)
print(citysum)

from folium import Element
map_var = m.get_name()
citylist = [
    ["北京市","Beijing",39.9042,116.4074,11],
    ["上海市","Shanghai",31.0100,121.4737,10],
    ["佛山市","Foshan",22.8919,112.8690,11],
    ["广州市","Guangzhou",23.07973,113.23455,12],
    ["杭州市","Hangzhou",30.23073,120.14920,12],
    ["肇庆市","Zhaoqing",23.08489,112.50192,13],
    ["江门市","Jiangmeng",22.82926,112.86808,13],
    ["阳江市","Yangjiang",21.567433,111.837264,13],
    ["长沙市","Changsha",28.200786,113.000833,13],
    ["武汉市","Wuhan",30.544631,114.302479,12],
    ["厦门市","Xiameng",24.528288,118.183274,12],
    ["宁波市","Ningbo",29.780472,121.629362,14],
    ["舟山市","Zhoushan", 29.904443,122.407543,12],
    ["嘉兴市","Jiaxing",30.533073,120.685239,15],
    ["芜湖市","Wuhu",31.337129,118.35807,15],
    ["金华市","Jinhua", 29.213957,119.47529,14],
    ["温州市","Wenzhou",27.972729,120.914697,11],
    ["太原市","Taiyuan",37.809694,112.568537,12],
    ["昆明市","Kunming",24.859032,102.771717,13],
    ["大理白族自治州","Dali",25.789693,100.14789,12],
    ["南昌市","Nanchang",28.657547,115.8540042,12],
    ["上饶市","Shangrao",28.6882821,117.7981305,14],
    ["景德镇市","Jingdezhen",29.2712774,117.1727822,13],
    ["晋中市","Jinzhong",37.6866796,112.7383414,14],
    ["六安市","Luan",31.883699,116.521854,11],
    ["合肥市","Hefei",31.8031187,117.2550177,13],
    ["信阳市","Xinyang",32.1319046,115.0410674,13],
    ["青岛市","Qingdao",36.0759435,120.4085225,13],
    ["香港","Hong Kong",22.302711,114.177216,13]
]

selectlist = """"""
locationlist = """initial: [0,0,1]"""
for name,en,lat,lon,zoom in citylist:
    selectlist = selectlist + f"""
    <option value="{en}">{name}:{round(citysum[name]/1000,2)}km</option>"""
    
    locationlist = locationlist + f""",
    {en}:[{lat},{lon},{zoom}]"""
    
custom_html = f"""
<style>
    #city-select {{
        position: absolute;
        top: 10px;
        left: 50px;
        z-index: 1000;
        padding: 6px;
        font-size: 16px;
        background: white;
        border-radius: 5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }}
</style>

<select id="city-select">
    <option value="">🌍 我曾在这些城市留下痕迹</option>
    {selectlist}  
</select>

<script>
    const cityCenters = {{
        {locationlist}
    }};

    const select = document.getElementById('city-select');

    select.addEventListener('change', function () {{
        const val = this.value;
        if (val && cityCenters[val]) {{
            const [lat, lon, zoom] = cityCenters[val];
            {map_var}.setView([lat, lon], zoom);  // 使用 folium 真实地图变量名
        }}
    }});
</script>
"""
m.get_root().html.add_child(Element(custom_html))
m.save(f'{output}//map_with_polyline_cityselect.html')