"""
Módulo para la gestión de reservas.
"""
import requests
import streamlit as st

# URL de tu servidor FastAPI
API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Gestión de Reservas", page_icon="📅", layout="wide")
st.title("📅 Panel de Reservaciones")

def safe_api_call(endpoint, method="GET", payload=None):
    """Función para realizar peticiones seguras a la API."""
    try:
        clean_endpoint = endpoint.lstrip('/')
        url = f"{API_BASE}/{clean_endpoint}"
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
    resp = safe_api_call("reservas/")
    if resp and resp.status_code == 200:
        # CORRECCIÓN: 'width' ahora es 'stretch'
        st.dataframe(resp.json(), width='stretch') 
    else:
        st.info("No hay reservas para mostrar.")

with tab_nueva:
    res_users = safe_api_call("users")
    users = res_users.json() if res_users and res_users.status_code == 200 else []

    res_rooms = safe_api_call("rooms?disponibles_only=true")
    rooms = res_rooms.json() if res_rooms and res_rooms.status_code == 200 else []

    if users and rooms:
        with st.form("new_res"):
            u_sel = st.selectbox("Cliente:", [u.get("name", "Desconocido") for u in users])
            r_sel = st.selectbox("Habitación:", [r.get("numero", "N/A") for r in rooms])
            horas = st.number_input("Horas de estadía:", min_value=1, step=1, value=1)
            
            if st.form_submit_button("Iniciar"):
                user_match = next((u for u in users if u.get("name") == u_sel), None)
                room_match = next((r for r in rooms if r.get("numero") == r_sel), None)
                
                if user_match and room_match:
                    # CORRECCIÓN DE CAMPOS: Usamos 'id_user' y 'id' según tus datos
                    uid = user_match.get("id_user") or user_match.get("id")
                    rid = room_match.get("id")
                    
                    if uid and rid:
                        payload = {"id_usuario": uid, "id_room": rid, "horas": horas}
                        resp = safe_api_call("reservas/", method="POST", payload=payload)
                        
                        if resp and resp.status_code in [200, 201]:
                            st.success("Reserva creada correctamente.")
                            st.rerun() 
                        else:
                            st.error(f"Error del servidor: {resp.text if resp else 'Sin respuesta'}")
                    else:
                        st.error("No se pudo obtener el ID necesario.")
                else:
                    st.error("Error al buscar el cliente o la habitación.")
    else:
        st.warning("Cargando datos o no hay recursos disponibles...")