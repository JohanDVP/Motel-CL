import streamlit as st
import requests

API_URL = "http://localhost:8000/users"

st.set_page_config(page_title="Gestión de Usuarios", page_icon="👥", layout="wide")
st.title("👥 Control de Clientes / Usuarios")

# Función auxiliar para manejar respuestas de forma segura
def safe_request(method, url, json_payload=None):
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=json_payload)
        elif method == "PUT":
            response = requests.put(url, json=json_payload)
        elif method == "DELETE":
            response = requests.delete(url)
        
        # Intentar parsear JSON solo si es necesario
        if response.status_code in [200, 201]:
            return response, response.json()
        else:
            # Si hay error, intentar capturar el detalle o devolver el texto plano
            try:
                error_msg = response.json().get('detail', str(response.status_code))
            except:
                error_msg = response.text
            return response, error_msg
    except Exception as e:
        return None, str(e)

tab_listar, tab_crear, tab_acciones = st.tabs(["📋 Lista de Clientes", "➕ Registrar Nuevo", "⚙️ Modificar / Eliminar"])

with tab_listar:
    st.subheader("Clientes Registrados")
    resp, data = safe_request("GET", API_URL)
    if resp is not None and resp.status_code == 200:
        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.info("No hay usuarios registrados.")
    else:
        st.error(f"Error al obtener usuarios: {data}")

with tab_crear:
    st.subheader("Formulario de Registro")
    with st.form("form_crear"):
        name = st.text_input("Nombre Completo:")
        edad = st.number_input("Edad:", 18, 120, 18)
        sexo = st.selectbox("Sexo:", ["M", "F", "Otro"])
        telefono = st.text_input("Teléfono:")
        email = st.text_input("Email:")
        if st.form_submit_button("Guardar"):
            payload = {"name": name, "edad": edad, "sexo": sexo, "telefono": telefono, "email": email}
            resp, msg = safe_request("POST", API_URL, payload)
            if resp and resp.status_code == 201:
                st.success("¡Registrado con éxito!")
            else:
                st.error(f"Error: {msg}")

with tab_acciones:
    st.subheader("Gestión de Registros")
    resp, data = safe_request("GET", API_URL)
    if resp is not None and resp.status_code == 200 and data:
        opciones = {f"{u['name']} (ID: {u['id_user']})": u for u in data}
        sel = st.selectbox("Selecciona cliente:", opciones.keys())
        u = opciones[sel]
        
        c1, c2 = st.columns(2)
        with c1:
            with st.form("edit_form"):
                n_name = st.text_input("Nombre", u['name'])
                if st.form_submit_button("Actualizar"):
                    resp, msg = safe_request("PUT", f"{API_URL}/{u['id_user']}", {"name": n_name, "edad": u['edad'], "sexo": u['sexo'], "telefono": u['telefono'], "email": u['email']})
                    if resp and resp.status_code == 200: st.success("Actualizado")
                    else: st.error(f"Error: {msg}")
        with c2:
            if st.button("Eliminar", type="primary"):
                resp, msg = safe_request("DELETE", f"{API_URL}/{u['id_user']}")
                if resp and resp.status_code == 200: 
                    st.success("Eliminado")
                    st.rerun()
                else: st.error(f"Error: {msg}")