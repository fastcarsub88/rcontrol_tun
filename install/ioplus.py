import libioplus as m

name = 'example'

bord_id = 0
AO_id   = 1
DI_id   = 4

door_ids = {
"main"  : [1,3],
"small" : [2,4]
}

tun_doors = ['main0','small1']

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

def calc_door(dnum):
    return door_ids[dnum[0:-1]][int(dnum[-1])]

def calc_doors(type):
    str = '0000'
    for i in door_ids[type]:
        str = str[:(i-1)] +'1'+ str[i:]
    return int(str[::-1],2)

def calc_tun_doors():
    str = '0000'
    for i in tun_doors:
        index = door_ids[i[0:-1]][int(i[-1])]
        str = str[:(index-1)] +'1'+ str[index:]
    return int(str[::-1],2)

def open_door(dnum):
    m.setRelayCh(bord_id,calc_door(dnum),1)

def close_door(dnum):
    m.setRelayCh(bord_id,calc_door(dnum),0)

def set_door_relays(num):
    m.setRelays(bord_id,num)

def is_tunnel():
    return m.getOptoCh(bord_id,DI_id)

def set_press(press):
    m.setDacV(bord_id,AO_id,press)

def index_find(i):
    for v in door_ids:
        for va in door_ids[v]:
            if i == va:
                return v+str(door_ids[v].index(va))

def relay_state():
    '{0:04b}'.format(m.getRelays(bord_id))
    rt = {}
    ind = 4
    for i in st:
        rt[index_find(ind)] = i
        ind = ind - 1
    return json.dumps(rt)
