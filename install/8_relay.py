import megaioind as m
import relay8 as r

name = 'example'

bord_id = 0
AO_id   = 1
DI_id   = 4

door_ids = {
"main"  : {
"open" : [7,2],
"close" : [5,4]
},
"small" : {
"open" : [8,1],
"close" : [3,6]
}
}

tun_doors = ['small0','small1']

wind_dir_dict = {
0  : "N",
45 : "NE",
90 : "E",
135: "SE",
180: "S",
225: "SW",
270: "W",
315: "NW",
360: "N"
}


def calc_doors(type):
    # for open state - type = main or small
    st = '00000000'
    other = 'small' if type == 'main' else 'main'
    on = door_ids[type]['open']
    other_on = door_ids[other]['close']
    off = door_ids[type]['close']
    other_off = door_ids[other]['open']
    on_relays = on + other_on
    off_relays = off + other_off
    for i in on_relays:
        st = st[:(i-1)] +'1'+ st[i:]
    for i in off_relays:
        st = st[:(i-1)] +'0'+ st[i:]
    return int(st[::-1],2)

def calc_doors_close():
    st = '00000000'
    on = door_ids['main']['close']
    other_on = door_ids['small']['close']
    off = door_ids['main']['open']
    other_off = door_ids['small']['open']
    on_relays = on + other_on
    off_relays = off + other_off
    for i in on_relays:
        st = st[:(i-1)] +'1'+ st[i:]
    for i in off_relays:
        st = st[:(i-1)] +'0'+ st[i:]
    return int(st[::-1],2)

def calc_tun_doors():
    st = '00000000'
    on_relays = door_ids['main']['close'] + door_ids['small']['close']
    for i in on_relays:
        st = st[:(i-1)] +'1'+ st[i:]
    tun_op_relays = []
    tun_cl_relays = []
    for i in tun_doors:
        tun_op_relays.append(door_ids[i[0:-1]]['open'][int(i[-1])])
        tun_cl_relays.append(door_ids[i[0:-1]]['close'][int(i[-1])])
    for i in tun_op_relays:
        st = st[:(i-1)] +'1'+ st[i:]
    for i in tun_cl_relays:
        st = st[:(i-1)] +'0'+ st[i:]
    return int(st[::-1],2)

def calc_door(dnum,state):
    return door_ids[dnum[0:-1]][state][int(dnum[-1])]

def open_door(dnum):
    r.set(bord_id,calc_door(dnum,'close'),0)
    time.sleep(0.1)
    r.set(bord_id,calc_door(dnum,'open'),1)

def close_door(dnum):
    r.set(bord_id,calc_door(dnum,'open'),0)
    time.sleep(0.1)
    r.set(bord_id,calc_door(dnum,'close'),1)

def set_door_relays(num):
    if num == 0:
        num = calc_doors_close()
    r.set_all(bord_id,num)

def relay_state():
    st = '{0:08b}'.format(r.get_all(bord_id))
    rt = {}
    ind = 8
    for i in st:
        rt[index_find(ind)] = i
        ind = ind - 1
    return rt

def is_tunnel():
    return m.getOptoCh(bord_id,DI_id)

def set_press(press):
    if int(m.getUOut(bord_id,AO_id)) == press:
        return
    m.setUOut(bord_id,AO_id,press)

def index_find(i):
    for v in door_ids:
        for va in door_ids[v]:
            for val in door_ids[v][va]:
                if i == val:
                    return v+va+str(door_ids[v][va].index(val))
