import requests,threading,json,requests,megaioind as m, relay8 as r,time
from datetime import datetime
from definitions import *

last_weather_check = 0

def open_door(dnum):
    op_relay = door_dict[dnum+"open"]
    cl_relay = door_dict[dnum+"close"]
    r_set(cl_relay[0],cl_relay[1],0)
    time.sleep(0.1)
    r_set(op_relay[0],op_relay[1],1)

def close_door(dnum):
    op_relay = door_dict[dnum+"open"]
    cl_relay = door_dict[dnum+"close"]
    r_set(op_relay[0],op_relay[1],0)
    time.sleep(0.1)
    r_set(cl_relay[0],cl_relay[1],1)

def set_press(press):
    if int(m.getUOut(pres_AO[0],pres_AO[1])) == press:
        return
    m.setUOut(pres_AO[0],pres_AO[1],press)

def r_set(brd,num,state):
    r_stat = '{0:04b}'.format(m.getRelays(0))
    if int(r_stat[4 - num]) == state:
        return
    m.setRelay(brd,num,state)

def get_conditions(data_file):
    w_data = requests.get("https://api.openweathermap.org/data/2.5/weather?zip=65078,us&appid=914fd2c984f8077049df587218d8579d&units=imperial")
    w_dict = json.loads(w_data.text)
    data_file['feels_like'] = w_dict['main']['feels_like']
    data_file['wind_speed'] = w_dict['wind']['speed']
    data_file['sunrise'] = time.strftime("%H:%M",time.localtime(w_dict['sys']['sunrise']))
    data_file['sunset'] = time.strftime("%H:%M",time.localtime(w_dict['sys']['sunset']))
    data_file['rain'] = requests.get("https://rcontrol.hawcreektech.com/dogwood/rain_api?method=get_state").text
    c_wind_dir = (w_dict['wind']['deg'] if 'deg' in w_dict['wind'] else '0')
    for value in wind_dir_dict:
        if value < c_wind_dir:
            continue
        if (value - c_wind_dir) < 23:
            wind_dir_str = wind_dir_dict[value]
        else:
            wind_dir_str = wind_dir_dict[(value-45)]
    data_file['wind_dir'] = wind_dir_str
    with open('data_file.json','w') as f:
         f.write(json.dumps(data_file))

def cnt_time(time,num):
    t = int(time.replace(':',''))
    num = int(num)
    dir = float(num)
    if dir >= 0:
        for i in range(num):
            if int(str(t)[-2:]) == 60:
                t += 41
            else:
                t += 1
    else:
        num = -num
        for i in range(num):
            if int(str(t)[-2:]) == 00:
                t -= 41
            else:
                t -= 1
    return t

while True:
    time.sleep(5)
    cr_tm = int(datetime.now().strftime('%H:%M').replace(":",''))
    with open('data_file.json') as f:
        data_file = json.load(f)
    if (cr_tm - last_weather_check) > 10 or last_weather_check > cr_tm:
        last_weather_check = cr_tm
        get_conditions(data_file)
    if data_file['auto'] == 0:
        continue
    feels_like = data_file['feels_like']
    if data_file['open_method'] == 'time':
        op_tm = int(data_file['open'].replace(':',''))
    else:
        op_tm = cnt_time(data_file['sunrise'],data_file['open'])
    if data_file['close_method'] == 'time':
        cl_tm = int(data_file['close'].replace(':',''))
    else:
        cl_tm = cnt_time(data_file['sunset'],data_file['close'])
    min_temp = data_file['min_temp']
    sm_door_temp = data_file['sm_door_temp']
    fst_close_tm = data_file['fst_close_tm']
    if cr_tm > op_tm and cr_tm < cl_tm:
        if data_file['open_state'] == 'reset':
            data_file['open_state'] = 'main'
            if feels_like < sm_door_temp:
                data_file['open_state'] = 'small'
            if feels_like < min_temp:
                date_file['open_state'] = 'none'
            with open('data_file.json','w') as f:
                f.write(json.dumps(data_file))
        if data_file['state'] == 'close':
            data_file['state'] = 'open'
            with open('data_file.json','w') as f:
                f.write(json.dumps(data_file))
        if data_file['open_state'] == 'none':
            set_press(7)
            close_door("11")
            time.sleep(0.001)
            close_door("12")
            time.sleep(0.001)
        else:
            cr_tm = str(cr_tm)
            cr_tm = (cr_tm[0:2]+":"+cr_tm[2:4])
            if (cnt_time(cr_tm + fst_close_tm) > cl_tm:
                set_press(data_file['min_pres'])
            elif (data_file['rain'] == 'true'):
                set_press(data_file['rain_pres'])
            else:
                set_press(data_file['max_pres'])
            st = data_file['open_state']
            op_dr = ('2' if st == 'small' else '1')
            cl_dr = ('2' if st == 'main' else '1')
            open_door("1"+op_dr)
            time.sleep(0.001)
            close_door("1"+cl_dr)
    else:
        if data_file['state'] == 'open':
            data_file['state'] = 'close'
            data_file['open_state'] = 'reset'
            with open('data_file.json','w') as f:
                f.write(json.dumps(data_file))
        set_press(7)
        close_door("11")
        time.sleep(0.001)
        close_door("12")
        time.sleep(0.001)
