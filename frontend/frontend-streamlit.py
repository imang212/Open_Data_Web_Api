import streamlit as st
#import json
#import pandas as pd
import folium as fo
from streamlit_folium import st_folium

# Nastavení stránky
#st.set_page_config(layout="wide")

# Filtrovací cíle
query_targets = ["Obec", "Stav"]
query_query = {query_p:[] for query_p in query_targets} 
st.write("Fine")

st.header("Živá mapa povodňových čidel")
st.divider()

picks = {
        "Obec":["Kundovice", "Pičín", "Prdelákov"],
        "Stav":["Dobrý", "Špatný", "Velmi špatný"]
}
st.write("Fine")

# Query picks
query_cols = st.columns(len(query_targets))
for index, param in enumerate(query_targets):
    print(index, param)
    with query_cols[index]:
        query_query[param] = st.multiselect(label=param, options=picks[param])
        

if st.button("Send it!"):
    st.write("Sent")

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

st_folium(usti, use_container_width=True)
