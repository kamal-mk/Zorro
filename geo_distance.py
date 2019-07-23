from math import sin, cos, sqrt, atan2, radians
import json
import string
import collections


#calculate distance
def calc_distance(city1,city2):
    cities={}
    rad_earth=6373.0 #radius of the earth in km
   

    with open("citylist.json",encoding='utf-8', errors='ignore') as json_data:
        data = json.load(json_data, strict=False)
    for p in data:
        temp_city=(p['cityLabel']).lower()
        temp_country=p['countryLabel']
        temp_gps=p['gps']
        #print(temp_gps)
        temp_gps=(temp_gps[6:-1]).split()
        if len(temp_gps)==2:
            lng=temp_gps[0]
            lat=temp_gps[1]
        #print(temp_gps)
        tlat=radians(float(lat))
        tlon=radians(float(lng))
        #print(tlat,tlon)
        cities[temp_city]={'country':temp_country,'lat':tlat,'lon':tlon}
    #print("Loaded",len(cities),"cities")
    city1=cities[city1]
    city2=cities[city2]

    dlon=city1['lat']-city2['lat']
    dlat=city1['lon']-city2['lon']
    
    a = sin(dlat / 2)**2 + cos(city1['lat']) * cos(city2['lat']) * sin(dlon / 2)**2
    #a=abs(a)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance=round(rad_earth*c)
    #print("User location is approximately",distance,"km away.")
    return distance

