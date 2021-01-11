import folium
import pandas

data = pandas.read_csv("data/US_volcanoes.txt")  # Pandas DataFrame
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])


def color_producer(elevation):
    if elevation < 1500:
        return 'green'
    elif 1500 <= elevation <= 3000:
        return 'orange'
    else:
        return 'red'


basemap = folium.Map(location=[37.02, -24.61], zoom_start=3, tiles="Stamen Terrain")

# Volcanoes Layer
fgv = folium.FeatureGroup("US_Volcanoes")

for lt, ln, name, el in zip(lat, lon, name, elev):
    fgv.add_child(folium.CircleMarker(location=(lt, ln), radius=6, popup=name+"\n"+str(el)+" m",
                                      fill_color=color_producer(el), color='grey', fill_opacity=0.7))

# World Population Layer
fgp = folium.FeatureGroup("Population_2005")
choropleth = folium.GeoJson(data=open('data/world.json', 'r', encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor':
                                                       'green' if x['properties']['POP2005'] < 10000000
                                                       else
                                                       'orange' if 10000000 <= x['properties']['POP2005'] <= 20000000
                                                       else
                                                       'red'})
choropleth.add_child(folium.GeoJsonTooltip(fields=['NAME','POP2005'], aliases=['Country','Population'], localize=True))
fgp.add_child(choropleth)

basemap.add_child(fgv)
basemap.add_child(fgp)
basemap.add_child(folium.LayerControl())

basemap.save("Map.html")
