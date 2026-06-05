"""
Módulo para la gestión de habitaciones del inventario.
"""
import requests
import streamlit as st

# Asegúrate de que esta URL coincida con la de tu servidor FastAPI
API_URL = "http://localhost:8000/rooms"

st.set_page_config(
    page_title="Gestión de Habitaciones", page_icon="🛏️", layout="wide"
)
st.title("🛏️ Control de Habitaciones")

tab_listar, tab_crear, tab_acciones = st.tabs(
    ["📋 Inventario", "➕ Agregar Nueva", "⚙️ Modificar / Eliminar"]
)


def get_rooms(params: dict | None = None):
    """Obtiene la lista de habitaciones desde la API."""
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


with tab_listar:
    st.subheader("Habitaciones del Sistema")
    solo_disp = st.checkbox("🔍 Mostrar solo disponibles")

    rooms = get_rooms({"disponibles_only": solo_disp})
    if rooms is not None:
        if rooms:
            st.dataframe(rooms, use_container_width=True, hide_index=True)
        else:
            st.info("No hay habitaciones disponibles.")
    else:
        st.error("Error conectando con el backend.")

with tab_crear:
    with st.form("form_crear_room", clear_on_submit=True):
        numero = st.text_input("Número de Habitación:")
        tipo = st.selectbox("Tipo:", ["Sencilla", "Doble", "Suite"])
        precio = st.number_input("Precio ($):", min_value=1.0, value=20.0)

        caracteristicas_input = st.text_input(
            "Características (separadas por coma):",
            help="Ejemplo: TV, Wi-Fi, Aire Acondicionado",
        )

        if st.form_submit_button("Guardar"):
            if caracteristicas_input:
                lista_caracteristicas = [
                    c.strip() for c in caracteristicas_input.split(",")
                ]
            else:
                lista_caracteristicas = []

            payload = {
                "numero": numero,
                "tipo": tipo,
                "precio": precio,
                "caracteristicas": lista_caracteristicas,
            }

            try:
                r = requests.post(API_URL, json=payload, timeout=10)
                if r.status_code == 201:
                    st.success(f"Habitación {numero} creada con éxito.")
                else:
                    st.error(f"Error: {r.json().get('detail')}")
            except Exception as e:
                st.error(f"Fallo de conexión: {e}")

with tab_acciones:
    rooms = get_rooms()
    if rooms:
        opciones = {f"{r['numero']} ({r['tipo']})": r for r in rooms}
        sel = st.selectbox("Seleccionar para gestionar:", opciones.keys())
        r_sel = opciones[sel]

        if st.button("🚨 Eliminar", type="primary"):
            try:
                url_del = f"{API_URL}/{r_sel['id']}"
                requests.delete(url_del, timeout=10)
                st.rerun()
            except Exception:
                st.error("Error al eliminar.")
    else:
        st.info("No hay datos disponibles.")