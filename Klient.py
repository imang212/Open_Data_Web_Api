import streamlit as st
import requests

st.title("Streamlit Frontend")

if st.button("Načíst data z FastAPI"):
    res = requests.get("http://localhost:8000/query")
    st.json(res.json())
