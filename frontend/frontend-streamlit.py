from requests.api import request
import streamlit as st
import json
import pandas as pd
import folium as fo
from streamlit_folium import st_folium
import requests
from typing import Dict, List
# Nastavení stránky
#st.set_page_config(layout="wide")

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
    base = "http://backend:8000/query"

    addon = ""
    for key, val in query.items():
        if len(val) > 0:
            to_add = val[0]
            if len(addon) > 0:
                addon += "&"
            addon += f"{key}={to_add}"

    if len(addon) > 0:
        addon = "?" + addon

    return base + addon

def color_func(level: str) -> str:
    match level:
        case "SUCHO":
            return "yellow"
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

query_targets = ["Obec", "uroven", "Tok"]

# Filtrovací slova
filter_prething = requests.get("http://backend:8000/query").json()
filter_done = { keyword:{thing[keyword] for thing in filter_prething} for keyword in query_targets }
st.write(filter_done)

# Vepsání filtrovacích slov do perzistentního stavu
for key, item in filter_done.items():
    st.session_state[key] = list(item)

# Filtrovací cíle
query_query = {query_p:[] for query_p in query_targets}
st.write("Fine")

st.header("Živá mapa povodňových čidel")
st.divider()

st.write("Fine")

# Query picks
query_cols = st.columns(len(query_targets))
for index, param in enumerate(query_targets):
    print(index, param)
    with query_cols[index]:
        query_query[param] = st.multiselect(label=param, options=st.session_state[param])


# Získání bodů do mapy
point_getter = query_gen(query_query)
st.write(point_getter)
points = requests.get(point_getter).json()
st.write(points)

for key, val in query_query.items():
    print(f"{key}: {val}")

max_lat, min_lat = 75, 33
max_long, min_long = 65, -31

usti = fo.Map(
        [50, 13],
        zoom_start=5,
        max_bounds=True,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_long,
        max_lon=max_long
)

for point in points:
    fo.Marker(
        location=[point["Wgs84Lat"],point["Wgs84Lon"]],
        icon=fo.Icon(color=color_func(point["uroven"]))
    ).add_to(usti)

st_folium(usti, use_container_width=True)
