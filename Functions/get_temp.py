import datetime, requests, json
from pythainlp.number import *
from urllib3 import PoolManager
#ในส่วนของการ ดึงข้อมูลจาก API
cond_data = {'Clear':"ท้องฟ้าแจ่มใส",
    'Partly Cloudy':'มีเมฆบางส่วน',
    'Cloudy':'มีเมฆเป็นส่วนมาก',
    'Overcast':'มีเมฆมาก',
    'Light rain':"ฝนตกเล็กน้อย",
    'Moderate rain':"ฝนปานกลาง",
    'Heavy rain':"ฝนตกหนัก",
    'Thunderstorm':"ฝนฟ้าคะนอง",
    'Very cold':"อากาศหนาวจัด",
    'Cold':"อากาศหนาว",
    'Cool':"อากาศเย็น",
    'Very hot':"อากาศร้อนจัด"}
day_data = ['วันจันทร์','วันอังคาร','วันพุธ','วันพฤหัสบดี','วันศุกร์','วันเสาร์','วันอาทิตย์']
month_data = {'01':'มกราคม',
              '02':'กุมภาพันธ์',
              '03':'มีนาคม',
              '04':'เมษายน',
              '05':'พฤษภาคม',
              '06':'มิถุนายน', 
              '07':'กรกฎาคม',
              '08':'สิงหาคม',
              '09':'กันยายน',
              '10':'ตุลาคม',
              '11':'พฤศจิกายน',
              '12':'ธันวาคม'}
def get_weather():
    d = {'api_key': '3966a3490632cabf',
         'state_code': 'TH',
         'personal_weather_station': 'Ubon_Ratchathani'}
    pm = PoolManager()
    r = pm.request('GET', 'http://api.wunderground.com/api/' +
                   d['api_key'] + '/conditions/q/' + d['state_code'] +
                   '/' + d['personal_weather_station'] + '.json')
    return r
def get_temp():
    temp = str(json.loads(get_weather().data.decode('utf-8'))['current_observation']['temp_c']).split('.')[0]
    temp = numtowords(float(temp)).replace('บาทถ้วน','')
    return "อุณหภมูิอยู่ที่ "+ temp + "องศาเซลเซียส"
def get_cond():
    return cond_data[json.loads(get_weather().data.decode('utf-8'))['current_observation']['weather']]
def get_time():
    now = datetime.datetime.now()
    time = str(now.time()).split(':')
    return numtowords(float(time[0])).replace('บาทถ้วน','') + "นาฬิกา " + numtowords(float(time[1])).replace('บาทถ้วน','') + "นาที"
def get_date():
    now = datetime.datetime.now()
    date = str(now.date())
    return date
def get_day():
    now = datetime.datetime.now()
    date = str(now.date())
    return day_data[now.weekday()]
def get_month():
    date = get_date().split('-')
    return month_data[date[1]]
def get_year():
    date = get_date().split('-')
    
    return numtowords(float(date[0])).replace('บาทถ้วน','')
def res():
    res = {'date':'วันนี้'+get_day()+' ที่'+numtowords(float(get_date().split('-')[2])).replace('บาทถ้วน','')+' '+get_month()+' ปี'+get_year(),
       'month':get_month(), 
       'year':get_year(), 
       'time':get_time(), 
       'weather':get_temp()+' สภาพอากาศ'+get_cond()}
    return res