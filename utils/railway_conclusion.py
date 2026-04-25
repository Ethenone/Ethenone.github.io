# -*- coding: GBK -*-
from cmath import nan
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import datetime
import sys
import json
from pypinyin import lazy_pinyin,load_phrases_dict

database = sys.argv[1]
output = sys.argv[2]

print("reading travel history")
data = pd.read_excel(f'{database}/火车乘坐记录.xlsx', sheet_name = '乘坐列表')
data_air = pd.read_excel(f'{database}//飞机乘坐记录.xlsx', sheet_name = 0)
data_f = pd.read_excel(f'{database}/境外铁路乘坐记录.xlsx', sheet_name = '乘坐列表')
data_f = data_f.fillna('NaN')


airportdata = pd.read_csv(f'{database}//airports_data.csv',encoding='gb18030')
#airportdata.head()
airportgeo = {}
for i in range(len(airportdata)):
    airportgeo[airportdata['iata'][i]]=[airportdata['lat'][i],airportdata['lon'][i]]
#print(airportgeo)


statdata = pd.read_csv(f'{database}//stations_data.csv',encoding='gbk')
statgeo = {}
stat_affiliation = {}
for i,row in statdata.iterrows():
    lat = row['纬度']
    lng = row['经度']
    loc = [lat,lng]
#     loc = correct(loc)
    statgeo[row['车站']]=loc
    stat_affiliation[row['车站']]={'lat':lat,'lng':lng,
                                 'bureau':row['路局'],
                                 'city':row['市'],
                                 'province':row['省']}
stats = {}
charts = {}

statdataf = pd.read_excel(f'{database}//境外铁路乘坐记录.xlsx',sheet_name='车站位置')

statgeof = {}
for i in range(len(statdataf)):
    lat = statdataf['lat'][i]
    lng = statdataf['lon'][i]
    loc = [lat,lng]
#     loc = correct(loc)
    statgeof[statdataf['车站'][i]]=loc


#总乘坐次数
stats['total_trips'] = data.shape[0]

#总乘坐时间
total_time = sum(data['时长.1'])
hour,minute = divmod(total_time,60)
stats['total_time'] = [int(hour),int(minute)]

#乘坐时间最长和最短的车
timemax = data.loc[data['时长.1'].idxmax()]
hour,minute = divmod(timemax['时长.1'],60)

stats['longest_trip'] = {'train':timemax['车次'],
                        'from':timemax['上车站'],
                        'to':timemax['下车站'],
                        'duration':f'{int(hour)}h{int(minute)}min'}

timemin = data.loc[data['时长.1'].idxmin()]
hour,minute = divmod(timemin['时长.1'],60)

stats['shortest_trip'] = {'train':timemin['车次'],
                        'from':timemin['上车站'],
                        'to':timemin['下车站'],
                        'duration':f'{int(hour)}h{int(minute)}min'}


#30分钟短途车
under30 = (data[data['时长.1']<30].shape[0])
stats['short_trips'] = under30


#跨天车
night = data[data['跨天']>=1].shape[0]
stats['overnight_trips'] = night

charts['durations'] = [round(x) for x in data['时长.1']]
charts['distances'] = [x for x in data['里程']]

#总乘坐里程
total_dis = sum(data['里程'])
stats['total_distance'] = total_dis

#最远和最近的旅程
dismax = data.loc[data['里程'].idxmax()]
dis = dismax['里程']

stats['farest_trip'] = {'train':dismax['车次'],
                        'from':dismax['上车站'],
                        'to':dismax['下车站'],
                        'distance':f'{dis}km'}

dismin = data.loc[data['里程'].idxmin()]
dis = dismin['里程']

stats['nearest_trip'] = {'train':dismin['车次'],
                        'from':dismin['上车站'],
                        'to':dismin['下车站'],
                        'distance':f'{dis}km'}

#最快和最慢的旅程
ratemax = data.loc[data['速度'].idxmax()]
rate = int(ratemax['速度'])
stats['fastest_trip'] = {'train':ratemax['车次'],
                        'from':ratemax['上车站'],
                        'to':ratemax['下车站'],
                        'rate':f'{rate}km/h'}

ratemin = data.loc[data['速度'].idxmin()]
rate = int(ratemin['速度'])
stats['slowest_trip'] = {'train':ratemin['车次'],
                        'from':ratemin['上车站'],
                        'to':ratemin['下车站'],
                        'rate':f'{rate}km/h'}


#出发时间
earliestdep = data.loc[data['上车时间'].idxmin()]
charts['earliestdep'] = {
    'time':earliestdep['上车时间'].strftime('%H:%M'),
    'train':earliestdep['车次'],
    'from':earliestdep['上车站'],
    'to':earliestdep['下车站']
}
latestdep = data.loc[data['上车时间'].idxmax()]
charts['latestdep'] = {
    'time':latestdep['上车时间'].strftime('%H:%M'),
    'train':latestdep['车次'],
    'from':latestdep['上车站'],
    'to':latestdep['下车站']
}


charts['depart_hours'] = list(filter(lambda i: i is not None,[i.hour if type(i) is not float else None for i in data['上车时间']]))

#到达时间
earliestarr = data.loc[data['下车时间'].idxmin()]
charts['earliestarr'] = {
    'time':earliestarr['下车时间'].strftime('%H:%M'),
    'train':earliestarr['车次'],
    'from':earliestarr['上车站'],
    'to':earliestarr['下车站']
}
latestarr = data.loc[data['下车时间'].idxmax()]
charts['latestarr'] = {
    'time':latestarr['下车时间'].strftime('%H:%M'),
    'train':latestarr['车次'],
    'from':latestarr['上车站'],
    'to':latestarr['下车站']
}


charts['arrive_hours'] = list(filter(lambda i: i is not None,[i.hour if type(i) is not float else None for i in data['下车时间']]))



# 上下车时间散点图数据

charts['rides'] = [{"on":row['上车时间'].strftime('%H:%M'),
                    "off":row['下车时间'].strftime('%H:%M'),
                    "duration":int(row['时长.1']),
                    "distance":int(row['里程']),
                    "train":row['车次'],
                    "from":row['上车站'],
                    "to":row['下车站']} for i,row in data.iterrows()]


#城市统计
special_places = {
    '六安': [['lù'], ['ān']],
    '重庆': [['chóng'], ['qìng']],
    '厦门': [['xià'], ['mén']]
}

# 加载自定义拼音
for word, pinyin_list in special_places.items():
    load_phrases_dict({word: pinyin_list})


citycount = {}
def city_cal(city,country,direction,lat,lng):
    if city == "NaN":
        return

    if city == "Xianggang":
        city = "Hong Kong"

    if city not in citycount.keys():
        citycount[city] = {'on':0,'off':0,'total':0,
                           'lat':lat,'lng':lng,'country':country}
    citycount[city][direction] += 1
    citycount[city]['total'] += 1


for i,row in data.iterrows():

    city_cal(''.join(lazy_pinyin(row['上车城市'])).capitalize(),"China","on",statgeo[row['上车站']][0],statgeo[row['上车站']][1])
    city_cal(''.join(lazy_pinyin(row['下车城市'])).capitalize(),"China","off",statgeo[row['下车站']][0],statgeo[row['下车站']][1])

for i,row in data_air.iterrows():
    city_cal(row['起飞城市EN'],row['起飞国家'],'on',airportgeo[row['start']][0],airportgeo[row['start']][1])
    city_cal(row['降落城市EN'],row['降落国家'],'off',airportgeo[row['depart']][0],airportgeo[row['depart']][1])

for i,row in data_f.iterrows():
    city_cal(row['上车城市（英语）'],row['上车国家'],'on',statgeof[row['上车站']][0],statgeof[row['上车站']][1])
    city_cal(row['下车城市（英语）'],row['下车国家'],'off',statgeof[row['下车站']][0],statgeof[row['下车站']][1])
    
charts['citycount'] = citycount;    

#车站统计

stationcount = {}

northernmost = {"name":'nan',"lat":-90,"lng":0} #车站名，纬度，经度
southernmost = {"name":'nan',"lat":90,"lng":0} #车站名，纬度，经度
easternmost = {"name":'nan',"lat":0,"lng":-180} #车站名，纬度，经度
westernmost = {"name":'nan',"lat":0,"lng":180} #车站名，纬度，经度
r_city = {}
r_prov = {}

def station_cal(station,direction,moststation = False):
    if station == 'NaN':
        return
    if station not in stationcount.keys():
        affiliation = stat_affiliation[station]
        stationcount[station] = {'on':0,'off':0,'total':0} | affiliation
        city = affiliation['city']
        if city not in r_city.keys():
            r_city[city] = {'on':0,'off':0,'total':0} | affiliation 
            del r_city[city]['city'],r_city[city]['bureau']
        prov = affiliation['province']
        if prov not in r_prov.keys():
            r_prov[prov] = {'on':0,'off':0,'total':0} | affiliation
            del r_prov[prov]['province'],r_prov[prov]['city'],r_prov[prov]['bureau']
            

        
        if moststation:
            lat = statgeo[station][0]
            lng = statgeo[station][1]
            global northernmost,southernmost,easternmost,westernmost
            if lat > northernmost['lat']:
                northernmost = {'name':station,'lat':lat,'lng':lng}
            if lat < southernmost['lat']:
                southernmost = {'name':station,'lat':lat,'lng':lng}
            if lng > easternmost['lng']:
                easternmost = {'name':station,'lat':lat,'lng':lng}
            if lng < westernmost['lng']:
                westernmost = {'name':station,'lat':lat,'lng':lng}

    station_info = stationcount[station]
    for d in [station_info,r_city[station_info['city']],r_prov[station_info['province']]]:
        d[direction] += 1
        d['total'] += 1




for i,row in data.iterrows():
    station_cal(row['上车站'],'on',True)
    station_cal(row['下车站'],'off',True)
        
top_city, top_city_count = max(r_city.items(), key=lambda x: x[1]["total"])
top_prov, top_prov_count = max(r_prov.items(), key=lambda x: x[1]["total"])
top_stat, top_stat_count = max(stationcount.items(), key=lambda x: x[1]["total"])

charts['stationcount'] = stationcount
stats['northernmost'] = northernmost
stats['southernmost'] = southernmost
stats['easternmost'] = easternmost
stats['westernmost'] = westernmost
stats['railway_city_top'] = [top_city, top_city_count['total']]
stats['railway_prov_top'] = [top_prov, top_prov_count['total']]
stats['railway_stat_top'] = [top_stat, top_stat_count['total']]
stats['railway_station_count'] = len(stationcount)
stats['railway_city_count'] = len(r_city)
stats['railway_prov_count'] = len(r_prov)

with open(f'{output}/stats.json', 'w',encoding='utf-8') as f:
    json.dump(stats, f,ensure_ascii=False)
    
with open(f'{output}/charts.json', 'w',encoding='utf-8') as f:
    json.dump(charts, f,ensure_ascii=False)




