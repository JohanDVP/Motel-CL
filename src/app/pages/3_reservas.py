"""
Streamlit interface for creating and managing room reservations.
"""

import streamlit as st
import requests

st.set_page_config(page_title="Control de Reservas", page_icon="📅", layout="wide")

BASE_URL = "http://127.0.0.1:8000"

st.title("📅 Panel de Control de Reservaciones")
st.markdown("---")

col_crear, col_monitor = st.columns([1, 2])

with col_crear:
    st.header("🔑 Agendar Habitación")
    
    with st.form("form_nueva_reserva", clear_on_submit=True):
        id_usuario = st.number_input("ID del Cliente (Numérico):", min_value=1, step=1)
        id_habitacion = st.number_input("Número de Habitación:", min_value=1, step=1)
        horas = st.slider("Horas de Hospedaje:", min_value=1, max_value=24, value=4)
        
        botón_reserva = st.form_submit_with_button("Confirmar Reserva")
        
        if botón_reserva:
            # Payload alineado con ReservaCreate (Pydantic)
            payload = {
                "id_user": id_usuario,
                "id_room": id_habitacion,
                "horas": horas
            }
            
            try:
                respuesta = requests.post(f"{BASE_URL}/reservas/", json=payload)
                if respuesta.status_code == 201:
                    st.success("¡Reserva procesada y guardada en la nube con éxito!")
                    st.rerun()
                else:
                    error_msg = respuesta.json().get("detail", "Error en reglas de negocio.")
                    st.error(f"Falla al reservar: {error_msg}")
            except requests.exceptions.ConnectionError:
                st.error("Error crítico: El backend de FastAPI no responde.")

with col_monitor:
    st.header("📋 Historial Operativo")
    
    try:
        res = requests.get(f"{BASE_URL}/reservas/")
        if res.status_code == 200:
            reservas = res.json()
            if not reservas:
                st.info("No se registran transacciones activas en este momento.")
            else:
                tabla_res = []
                for r in reservas:
                    tabla_res.append({
                        "Reserva ID": r["id_reserva"],
                        "Cliente ID": r["id_user"],
                        "Habitación": r["id_room"],
                        "Horas": r["horas"],
                        "Total Facturado": f"${r['total']:.2f}"
                    })
                st.dataframe(tabla_res, use_container_width=True, hide_index=True)
        else:
            st.error("Error al leer el historial de reservas.")
    except requests.exceptions.ConnectionError:
        st.warning("Verifica la conexión del backend en el puerto 8000.")