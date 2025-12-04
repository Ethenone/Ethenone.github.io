# -*- coding: GBK -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import datetime
import sys
import json

database = sys.argv[1]
output = sys.argv[2]

print("reading travel history")
data = pd.read_excel(f'{database}/火车乘坐记录.xlsx', sheet_name = '乘坐列表')
#data = data.fillna(0)
#statdata.head()
stats = {}
charts = {}


#总乘坐次数
stats['total_trips'] = data.shape[0]

#总乘坐时间
total_time = sum(data['时长.1'])
hour,minute = divmod(total_time,60)
stats['total_time'] = f'{int(hour)}h{int(minute)}min'

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


#出发时间
earliestdep = data.loc[data['上车时间'][26:].idxmin()]
charts['earliestdep'] = {
    'time':earliestdep['上车时间'].strftime('%H:%M'),
    'train':earliestdep['车次'],
    'from':earliestdep['上车站'],
    'to':earliestdep['下车站']
}
latestdep = data.loc[data['上车时间'][26:].idxmax()]
charts['latestdep'] = {
    'time':latestdep['上车时间'].strftime('%H:%M'),
    'train':latestdep['车次'],
    'from':latestdep['上车站'],
    'to':latestdep['下车站']
}


charts['depart_hours'] = list(filter(lambda i: i is not None,[i.hour if type(i) is not float else None for i in data['上车时间']]))

#到达时间
earliestarr = data.loc[data['下车时间'][26:].idxmin()]
charts['earliestarr'] = {
    'time':earliestarr['下车时间'].strftime('%H:%M'),
    'train':earliestarr['车次'],
    'from':earliestarr['上车站'],
    'to':earliestarr['下车站']
}
latestarr = data.loc[data['下车时间'][26:].idxmax()]
charts['latestarr'] = {
    'time':latestarr['下车时间'].strftime('%H:%M'),
    'train':latestarr['车次'],
    'from':latestarr['上车站'],
    'to':latestarr['下车站']
}


charts['arrive_hours'] = list(filter(lambda i: i is not None,[i.hour if type(i) is not float else None for i in data['下车时间']]))


with open(f'{output}/stats.json', 'w',encoding='utf-8') as f:
    json.dump(stats, f,ensure_ascii=False)
    
with open(f'{output}/charts.json', 'w',encoding='utf-8') as f:
    json.dump(charts, f,ensure_ascii=False)