import streamlit as st
import requests

API_RESERVAS = "http://localhost:8000/reservas"
API_USERS = "http://localhost:8000/users"
API_ROOMS = "http://localhost:8000/rooms"

st.set_page_config(page_title="Gestión de Reservas", page_icon="📅", layout="wide")
st.title("📅 Panel de Reservaciones")

tab_historial, tab_nueva, tab_gestion = st.tabs([
    "📋 Historial de Reservas", 
    "⚡ Crear Nueva Reserva", 
    "🚫 Cancelar / Finalizar"
])

# TAB 1: HISTORIAL DE RESERVAS
with tab_historial:
    st.subheader("Registro General de Ocupación")
    if st.button("🔄 Actualizar Historial"):
        st.rerun()
        
    try:
        response = requests.get(API_RESERVAS)
        if response.status_code == 200:
            reservas = response.json()
            if reservas:
                st.dataframe(reservas, use_container_width=True, hide_index=True)
            else:
                st.info("No se registran transacciones de hospedaje.")
    except requests.exceptions.ConnectionError:
        st.error("Error: Backend desconectado.")

# TAB 2: CREAR RESERVACIÓN
with tab_nueva:
    st.subheader("Apertura de Ticket de Hospedaje")
    
    try:
        res_users = requests.get(API_USERS).json()
        res_rooms = requests.get(API_ROOMS, params={"disponibles_only": True}).json()
        
        if not res_users:
            st.warning("⚠️ No puedes crear reservas sin clientes registrados en el sistema.")
        elif not res_rooms:
            st.info("🛏️ Todas las habitaciones se encuentran ocupadas en este momento.")
        else:
            # CORRECCIÓN AQUÍ: Cambiado u['nombre'] por u['name'] para coincidir con el backend
            dict_users = {f"{u['name']} (ID: {u['id_user']})": u['id_user'] for u in res_users}
            dict_rooms = {f"Hab. {r['numero']} - {r['tipo']} (${r['precio']}/hr)": r for r in res_rooms}
            
            with st.form("form_nueva_reserva"):
                client_sel = st.selectbox("Seleccione el Cliente:", dict_users.keys())
                room_sel = st.selectbox("Seleccione Habitación Libre:", dict_rooms.keys())
                horas = st.number_input("Duración del hospedaje (Horas):", min_value=1, max_value=24, value=2)
                
                room_obj = dict_rooms[room_sel]
                total_estimado = room_obj['precio'] * horas
                st.info(f"💰 **Total a abonar en caja:** ${total_estimado:.2f}")
                
                if st.form_submit_button("⚡ Confirmar Entrada e Iniciar Reserva"):
                    payload = {
                        "id_usuario": dict_users[client_sel],
                        "id_room": room_obj['id'],
                        "horas": horas
                    }
                    rep = requests.post(API_RESERVAS, json=payload)
                    if rep.status_code == 201:
                        st.success("¡Reserva procesada y habitación bloqueada con éxito!")
                        st.rerun()
                    else:
                        st.error(f"Fallo en la operación: {rep.json().get('detail')}")
    except Exception:
        st.error("Conectando con dependencias del backend...")

# TAB 3: ACCIONES Y CANCELACIÓN
with tab_gestion:
    st.subheader("Gestión de Ciclo de Vida (Check-out / Cancelación)")
    
    try:
        res_all = requests.get(API_RESERVAS).json()
        activas = [r for r in res_all if r["estado"] == "activa"]
        
        if activas:
            dict_act = {f"Reserva #{ra['id']} - Habitación ID: {ra['id_room']} (Total: ${ra['total']})": ra for ra in activas}
            sel_res = st.selectbox("Seleccione la reserva activa:", dict_act.keys())
            reserva_obj = dict_act[sel_res]
            
            col_cancel, col_purge = st.columns(2)
            
            with col_cancel:
                st.markdown("### 🚪 Salida Anticipada / Cancelación")
                st.write("Esta acción liberará la habitación y cambiará el estado a 'cancelada'.")
                if st.button("🚫 Cancelar / Checkout Seguro", type="secondary"):
                    rep_can = requests.post(f"{API_RESERVAS}/{reserva_obj['id']}/cancelar")
                    if rep_can.status_code == 200:
                        st.success("Habitación liberada correctamente.")
                        st.rerun()
                    else:
                        st.error("No se pudo cambiar el estado.")
                        
            with col_purge:
                st.markdown("### 🚨 Depuración")
                st.write("Borra físicamente la reserva de la auditoría. Si estaba activa, desbloquea la habitación.")
                if st.button("🗑️ Eliminar del Historial", type="primary"):
                    rep_del = requests.delete(f"{API_RESERVAS}/{reserva_obj['id']}")
                    if rep_del.status_code == 204:
                        st.success("Registro eliminado del historial.")
                        st.rerun()
                    else:
                        st.error("Error al remover el registro.")
        else:
            st.info("No hay reservas activas que requieran gestión en este momento.")
    except Exception:
        st.error("Error al procesar el panel de gestión.")