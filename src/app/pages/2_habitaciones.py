import streamlit as st
import requests

API_URL = "http://localhost:8000/rooms"

st.set_page_config(page_title="Gestión de Habitaciones", page_icon="🛏️", layout="wide")
st.title("🛏️ Control de Habitaciones")
st.markdown("Administra el inventario, características y estado de ocupación del motel.")

tab_listar, tab_crear, tab_acciones = st.tabs([
    "📋 Inventario de Habitaciones", 
    "➕ Agregar Nueva Habitación", 
    "⚙️ Modificar / Eliminar"
])

# TAB 1: LISTAR HABITACIONES
with tab_listar:
    st.subheader("Habitaciones del Sistema")
    solo_disponibles = st.checkbox("🔍 Mostrar únicamente habitaciones disponibles")
    
    try:
        params = {"disponibles_only": solo_disponibles}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            habitaciones = response.json()
            if habitaciones:
                st.dataframe(habitaciones, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron habitaciones bajo los criterios seleccionados.")
        else:
            st.error(f"Error de API: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ No se pudo conectar con el Backend.")

# TAB 2: CREAR HABITACIÓN
with tab_crear:
    st.subheader("Registrar Nueva Habitación")
    with st.form("form_crear_room", clear_on_submit=True):
        numero = st.text_input("Número o Nombre de Habitación (Ej: 101, 204):")
        tipo = st.selectbox("Tipo de Habitación:", ["Sencilla", "Doble", "Suite", "Jacuzzi"])
        precio = st.number_input("Precio por Hora ($):", min_value=1.0, step=5.0, value=20.0)
        
        enviado = st.form_submit_button("Guardar Habitación")
        
        if enviado:
            if not numero or precio <= 0:
                st.warning("⚠️ Ingresa un número válido y un precio mayor a 0.")
            else:
                payload = {"numero": numero, "tipo": tipo, "precio": precio, "caracteristicas": []}
                response = requests.post(API_URL, json=payload)
                if response.status_code == 201:
                    st.success(f"🎉 Habitación '{numero}' agregada correctamente.")
                else:
                    st.error(f"Error: {response.json().get('detail')}")

# TAB 3: EDITAR Y ELIMINAR
with tab_acciones:
    st.subheader("Acciones sobre Habitaciones")
    
    try:
        res = requests.get(API_URL)
        if res.status_code == 200 and res.json():
            lista_rooms = res.json()
            opciones = {f"Habitación {r['numero']} ({r['tipo']})": r for r in lista_rooms}
            
            seleccion = st.selectbox("Selecciona la habitación a gestionar:", opciones.keys())
            room_seleccionada = opciones[seleccion]
            
            col_edit, col_del = st.columns(2)
            
            with col_edit:
                st.markdown("### 📝 Editar Especificaciones")
                with st.form("form_edit_room"):
                    n_numero = st.text_input("Número:", value=room_seleccionada["numero"])
                    n_tipo = st.selectbox("Tipo:", ["Sencilla", "Doble", "Suite", "Jacuzzi"], index=["Sencilla", "Doble", "Suite", "Jacuzzi"].index(room_seleccionada["tipo"]))
                    n_precio = st.number_input("Precio ($):", value=float(room_seleccionada["precio"]), min_value=1.0)
                    
                    if st.form_submit_button("💾 Actualizar"):
                        up_payload = {"numero": n_numero, "tipo": n_tipo, "precio": n_precio, "caracteristicas": room_seleccionada.get("caracteristicas", [])}
                        rep = requests.put(f"{API_URL}/{room_seleccionada['id']}", json=up_payload)
                        if rep.status_code == 200:
                            st.success("¡Habitación actualizada!")
                        else:
                            st.error("No se pudo actualizar.")
            
            with col_del:
                st.markdown("### 🗑️ Zona de Peligro")
                st.warning(f"¿Eliminar permanentemente la habitación {room_seleccionada['numero']}?")
                if st.button("🚨 Eliminar Registro", type="primary", key="del_room"):
                    rep_del = requests.delete(f"{API_URL}/{room_seleccionada['id']}")
                    if rep_del.status_code == 204:
                        st.success("Habitación eliminada con éxito.")
                        st.rerun()
                    else:
                        st.error("No se pudo eliminar (puede tener reservas activas asociadas).")
        else:
            st.info("No hay habitaciones en la base de datos.")
    except Exception:
        st.error("Error cargando el panel de edición.")