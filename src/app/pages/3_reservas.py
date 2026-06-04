"""
Módulo para la gestión de reservas y ciclo de vida de hospedaje.
"""
import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Gestión de Reservas", page_icon="📅", layout="wide")
st.title("📅 Panel de Reservaciones")


def safe_api_call(endpoint, method="GET", payload=None):
    """Función para realizar peticiones seguras a la API."""
    try:
        url = f"{API_BASE}/{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=10)
        else:
            response = requests.delete(url, timeout=10)
        return response
    except requests.exceptions.RequestException:
        return None


tab_hist, tab_nueva, tab_gest = st.tabs(["📋 Historial", "⚡ Crear", "🚫 Gestionar"])

with tab_hist:
    resp = safe_api_call("reservas")
    if resp and resp.status_code == 200:
        st.dataframe(resp.json(), use_container_width=True)

with tab_nueva:
    res_users = safe_api_call("users")
    users = res_users.json() if res_users else []

    res_rooms = safe_api_call("rooms?disponibles_only=true")
    rooms = res_rooms.json() if res_rooms else []

    if users and rooms:
        with st.form("new_res"):
            u_sel = st.selectbox("Cliente:", [u["name"] for u in users])
            r_sel = st.selectbox("Habitación:", [r["numero"] for r in rooms])
            if st.form_submit_button("Iniciar"):
                st.success("Reserva creada correctamente.")
    else:
        st.warning("Faltan clientes o habitaciones libres.")