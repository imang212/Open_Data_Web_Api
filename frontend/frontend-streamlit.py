from __future__ import annotations

import streamlit as st
#import json
#import pandas as pd
import folium as fo
from streamlit_folium import st_folium
import requests
from typing import Dict, List
# Nastavení stránky
#st.set_page_config(layout="wide")
import threading

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
            raise ValueError("Unexpected level")

def nazev_uroven_func(nazev_urovne: str) -> str:
    list_nazvu = ["SUCHO", "NELZE", "VYPNUTO", "EXTREM", "NORMAL"]
    list_prekladu = ["Suchá", "Neznámá", "Neměřená", "Extrémní", "Normální"]
    return list_prekladu[list_nazvu.index(nazev_urovne)]

query_targets = ["Obec", "uroven", "Tok"]

# Filtrovací slova
filter_query = "http://backend:8000/query" #if "query" not in st.session_state else st.session_state["query"]
filter_prething = requests.get(filter_query).json()
filter_done = { keyword:{thing[keyword] for thing in filter_prething} for keyword in query_targets }
#st.write(filter_done)

# Vepsání filtrovacích slov do perzistentního stavu
for key, item in filter_done.items():
    st.session_state[key] = list(item)

# Filtrovací cíle
query_query = {query_p:[] for query_p in query_targets}

st.header("Živá mapa povodňových čidel")

# Query picks
query_cols = st.columns(len(query_targets))
for index, param in enumerate(query_targets):
    print(index, param)
    with query_cols[index]:
        query_query[param] = st.multiselect(label=param, options=st.session_state[param])

# Získání bodů do mapy
point_getter = query_gen(query_query)
#st.write(point_getter)

points = None
def get_points():
    global points
    points = requests.get(point_getter).json()
    #st.write(points)
    threading.Timer(30, get_points).start()  # Update every 5 minutes
get_points()

for key, val in query_query.items():
    print(f"{key}: {val}")

ustecky_kraj_bounds = {'north': 50.95,'south': 50.15,'east': 14.65,'west': 12.85}
# Střed kraje
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
        min_lat=ustecky_kraj_bounds['south'] - 0.05,  # Malý buffer
        max_lat=ustecky_kraj_bounds['north'] + 0.05,
        min_lon=ustecky_kraj_bounds['west'] - 0.05,
        max_lon=ustecky_kraj_bounds['east'] + 0.05
)

for point in points:
    # Popup obsah pro Folium marker
    popup_info = f'''
    <div style="font-family: Arial, sans-serif;">
        <strong style="color:{color_uroven_func(point["uroven"])}">{point["Obec"]}</strong><br>
        <div style="margin: 8px 0;">
            <strong>Stav:</strong> {nazev_uroven_func(point["uroven"])}<br>
            <strong>Adresa:</strong> {point["Adresa"]}<br>
            <strong>Tok:</strong> {point["Tok"]}
        </div>
    </div>
    '''
    fo.Marker(
        location=[point["Wgs84Lat"], point["Wgs84Lon"]],
        popup=fo.Popup(popup_info, max_width=300),
        icon=fo.Icon(color=color_uroven_func(point["uroven"]))
    ).add_to(usti)

st_folium(usti, use_container_width=True)
