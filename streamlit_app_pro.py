
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import time

def obtener_buses_por_ruta(ruta_objetivo):
    url = "https://rest.busradar.conterra.de/prod/fahrzeuge"
    response = requests.get(url)
    response.raise_for_status()
    datos = response.json()
    return [
        bus for bus in datos["features"]
        if bus["properties"].get("linienid") == ruta_objetivo
    ]

st.set_page_config(page_title="🚍 Bus Tracker PRO", layout="wide")
st.title("🚍 Bus Tracker PRO — Animación en vivo de buses por ruta")

ruta = st.text_input("🔢 Ingresa número de ruta:", value="11")
actualizar = st.checkbox("🔄 Actualizar automáticamente cada 10 segundos", value=True)

if st.button("📍 Mostrar mapa") or actualizar:
    marcador_estado = st.empty()

    while True:
        buses = obtener_buses_por_ruta(ruta)
        mapa = folium.Map(location=[51.96, 7.63], zoom_start=13)

        if buses:
            for bus in buses:
                props = bus["properties"]
                coords = bus["geometry"]["coordinates"]
                lat, lon = coords[1], coords[0]
                delay = props.get("delay", 0)
                folium.Marker(
                    location=[lat, lon],
                    popup=f"🚌 Línea {props['line']}<br>ID: {props['linienid']}<br>Delay: {delay}s",
                    tooltip="Click para detalles"
                ).add_to(mapa)
            marcador_estado.success(f"{len(buses)} vehículos encontrados.")
        else:
            marcador_estado.warning("No hay buses activos en esta ruta.")

        st_folium(mapa, width=1000, height=600)

        if not actualizar:
            break
        time.sleep(10)
        st.rerun()
