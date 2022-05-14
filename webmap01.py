from cv2 import circle
import folium
import pandas
 
data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
 
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
 
def color_producer(elevation):
    if(0<=elevation<1500):
        return "red"
    elif(1500<=elevation<2500):
        return "green"
    elif(elevation>=2500):
        return "blue"

map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name = "Volcanoes")

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = color_producer(el))))

fgp = folium.FeatureGroup(name = "Population")
fgp.add_child(folium.GeoJson(data = open("world.json", "r", encoding = "utf-8-sig").read(), 
style_function = lambda x: {'fillColor': 'yellow' if x['properties']['POP2005'] < 10000000 else 'green' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'})) 

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("WorldMap.html")