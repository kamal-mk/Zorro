from geotext import GeoText


query="Golden Gate is an amazing place in San Francisco, I don't think anywhere uin London comes close."
places = GeoText(query)
for y in places.cities:
    print(y)