
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

def obtener_buses_por_ruta(ruta_objetivo):
    url = "https://rest.busradar.conterra.de/prod/fahrzeuge"
    response = requests.get(url)
    response.raise_for_status()
    datos = response.json()

    return [
        bus for bus in datos["features"]
        if bus["properties"].get("line") == ruta_objetivo
    ]

st.title("🚌 Seguimiento en vivo de autobuses por ruta")
ruta = st.text_input("Ingresa número de ruta (ej. 11):", value="11")

if st.button("Mostrar mapa"):
    buses = obtener_buses_por_ruta(ruta)

    if buses:
        mapa = folium.Map(location=[51.96, 7.63], zoom_start=13)

        for bus in buses:
            props = bus["properties"]
            coords = bus["geometry"]["coordinates"]
            lat, lon = coords[1], coords[0]
            folium.Marker(
                location=[lat, lon],
                popup=f"Línea {props['line']} - ID {props['id']}",
                tooltip=f"Delay: {props.get('delay', 0)}s"
            ).add_to(mapa)

        st_folium(mapa, width=700, height=500)
    else:
        st.warning("No se encontraron buses activos para esa ruta.")
