from __future__ import annotations
import streamlit as st
#import pandas as pd
import folium as fo
from streamlit_folium import st_folium
import requests
from typing import Dict, List
# Nastavení stránky
#st.set_page_config(layout="wide")
import threading
import json
import datetime

def query_gen(query: Dict[str, List[str]]) -> str:
    """Generates a URL with query parameters for a backend API.

        This function constructs a URL, appending query parameters based on the
        provided dictionary. For each key, it uses the first element of its
        corresponding list as the parameter's value if the list is not empty.

        Args:
            query: A dictionary mapping query parameter names (str) to lists of strings.
                   Only the first element of each list will be used.

        Returns:
            A string representing the complete URL with the generated query parameters.
    """
    base = "http://backend:8000/query?"

    addon_list = []
    for key, value in query.items():
        if len(value) == 0:
            continue
        a = key + "="
        a += ",".join(value)
        addon_list.append(a)
    addon = "&".join(addon_list)

    return base + addon

def color_uroven_func(level: str) -> str:
    match level:
        case "SUCHO":
            return "orange"
        case "NELZE":
            return "gray"
        case "VYPNUTO":
            return "black"
        case "EXTREM":
            return "red"
        case "NORMAL":
            return "green"
        case _:
            return "black"

def nazev_uroven_func(nazev_urovne: str) -> str:
    match nazev_urovne:
        case "SUCHO":
            return "Suchá"
        case "NELZE":
            return "Neznámá"
        case "EXTREM":
            return "Extrémní"
        case "NORMAL":
            return "Normální"
        case _:
            return "Vypnuto"

def format_date_time(date_time_str: str) -> str:
    months = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"]
    if date_time_str == "0":
        return "Neznámý čas"

    date_time_str = str(date_time_str)
    format_str = "%Y-%m-%d %H:%M:%S"
    dt = datetime.datetime.strptime(date_time_str, format_str).strftime("%d.%m.%Y %H:%M")

    day_time_parts = dt.split(" ")
    day, time = day_time_parts[0], day_time_parts[1]
    day_parts = day.split(".")
    day, month, year = day_parts[0], day_parts[1], day_parts[2]
    return f"{day}. {months[int(month) - 1]} {year} v {time}"

query_targets = ["Obec", "uroven", "Tok"]

if "keywords_loaded" not in st.session_state:
    # Filtrovací slova
    filter_query = "http://backend:8000/query" #if "query" not in st.session_state else st.session_state["query"]
    print("Requesting there.")
    filter_prething = requests.get(filter_query).json()
    filter_done = { keyword:{thing[keyword] for thing in filter_prething} for keyword in query_targets }
    #st.write(filter_done)

    # Vepsání filtrovacích slov do perzistentního stavu
    for key, item in filter_done.items():
        st.session_state[key] = list(item)

    st.session_state["keywords_loaded"] = True

# Filtrovací cíle
query_query = {query_p:[] for query_p in query_targets}

st.header("Živá mapa povodňových čidel")

# Query picks
param_labels = {"uroven": "Stav", "Obec": "Obec", "Tok": "Tok"}
import streamlit as st
import pandas as pd

# získávání možností pro filtrování
query_cols = st.columns(len(query_targets))
for index, param in enumerate(query_targets):
    with query_cols[index]:
        query_query[param] = st.multiselect(
            label=param_labels.get(param, param),  # Zobrazitelný název
            options=st.session_state[param]
        )
# Získání bodů do mapy
point_getter = query_gen(query_query)
st.write(point_getter)


points = None
def get_points():
    global points
    print("Fetching here.")
    points = requests.get(point_getter).json()
    #st.write(points)
    threading.Timer(60, get_points).start()  # Update every 5 minutes
get_points()

for key, val in query_query.items():
    print(f"{key}: {val}")

ustecky_kraj_bounds = {'north': 50.95,'south': 50.15,'east': 14.65,'west': 12.85}
center_lat = (ustecky_kraj_bounds['north'] + ustecky_kraj_bounds['south']) / 2
center_lon = (ustecky_kraj_bounds['east'] + ustecky_kraj_bounds['west']) / 2

usti = fo.Map(
        location=[center_lat, center_lon],
        zoom_start=9,
        min_zoom=9,
        max_zoom=15,
        scrollWheelZoom=False,
        dragging=True,
        max_bounds=True,
        min_lat=ustecky_kraj_bounds['south'] - 0.15,  # Malý buffer
        max_lat=ustecky_kraj_bounds['north'] + 0.15,
        min_lon=ustecky_kraj_bounds['west'] - 0.15,
        max_lon=ustecky_kraj_bounds['east'] + 0.15
)

if "map_loaded" not in st.session_state:
    #geojson_data = requests.get("http://backend:8000/geojson").json()
    st.session_state["map_loaded"] = requests.get("http://backend:8000/geojson").json()

ustecky_boundaries = next((f for f in st.session_state["map_loaded"]["features"] if "Ústecký kraj" in f["name"]), None)
# Střed kraje
if ustecky_boundaries:
    fo.GeoJson(
        ustecky_boundaries,
        name="Ústecký kraj",
        style_function=lambda x: {
            'fillColor': '#84b1ff',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.3
        },
        tooltip=ustecky_boundaries["name"]
    ).add_to(usti)
else:
    st.error("Ústecký kraj nebyl nalezen.")

for point in points:
    # Popup obsah pro Folium marker
    popup_info = f'''
    <div style="font-family: Arial, sans-serif;">
        <strong style="color:{color_uroven_func(point["uroven"])}">{point["Obec"]}</strong><br>
        <div style="margin: 8px 0;">
            <strong>Stav:</strong> {nazev_uroven_func(point["uroven"])}<br>
            <strong>Adresa:</strong> {point["Adresa"]}<br>
            <strong>Tok:</strong> {point["Tok"]}<br>
            <strong>Hladina:</strong> {point["Hladina"]} m<br>
            <strong>Aktualizováno:</strong> {format_date_time(str(point["Posledni_mereni"]))}
        </div>
    </div>
    '''
    fo.Marker(
        location=[point["Wgs84Lat"], point["Wgs84Lon"]],
        popup=fo.Popup(popup_info, max_width=300),
        icon=fo.Icon(color=color_uroven_func(point["uroven"]))
    ).add_to(usti)

st_folium(usti, use_container_width=True)
