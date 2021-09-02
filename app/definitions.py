import megaioind as m
bord_id = 0
AO_id   = 1

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
    return int(str[::-1])

def calc_tun_doors():
    str = '0000'
    for i in tun_doors:
        index = door_ids[i[0:-1]][int(i[-1])]
        str = str[:(index-1)] +'1'+ str[index:]
    return int(str[::-1])

def open_door(dnum):
    m.setRelay(bord_id,calc_door(dnum),1)

def close_door(dnum):
    m.setRelay(bord_id,calc_door(dnum),0)

def set_door_relays(num):
    m.setRelays(bord_id,num)

def relay_state():
    return '{0:04b}'.format(m.getRelays(bord_id))

def is_tunnel():
    return m.getOptoCh(bord_id,1)

def set_press(press):
    if int(m.getUOut(bord_id,AO_id)) == press:
        return
    m.setUOut(bord_id,AO_id,press)
