"""
Main entry point for the Streamlit Frontend application.
"""

import streamlit as st

st.set_page_config(page_title="Motelandro Dashboard", page_icon="🏨", layout="wide")

st.title("🏨 Bienvenido a Motelandro Management System")
st.markdown("---")

st.info("""
    Utiliza el menú lateral de la izquierda para gestionar el motel:
    * **👥 1 Usuarios:** Registro y consulta de clientes en la nube.
    * **🛏️ 2 Habitaciones:** Ver estado e inventario en tiempo real.
    * **📅 3 Reservas:** Crear reservaciones y calcular totales automáticos.
""")

st.sidebar.success("Selecciona una sección arriba.")
