"""
Streamlit page for User management.
"""

import requests
import streamlit as st

API_URL = "http://localhost:8000/users"

st.set_page_config(
    page_title="Gestión de Usuarios", page_icon="👥", layout="wide"
)
st.title("👥 Control de Clientes / Usuarios")


def safe_request(method: str, url: str, json_payload: dict | None = None):
    """Auxiliary function to handle API requests safely."""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=json_payload, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=json_payload, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        else:
            return None, "Método no soportado"

        if response.status_code in [200, 201, 204]:
            return response, response.json() if response.content else None
        
        # Intentar capturar el detalle de error
        try:
            error_msg = response.json().get("detail", str(response.status_code))
        except ValueError:
            error_msg = response.text
        return response, error_msg

    except requests.exceptions.RequestException as e:
        return None, str(e)


tab_listar, tab_crear, tab_acciones = st.tabs(
    ["📋 Lista de Clientes", "➕ Registrar Nuevo", "⚙️ Modificar / Eliminar"]
)

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
            payload = {
                "name": name,
                "edad": edad,
                "sexo": sexo,
                "telefono": telefono,
                "email": email,
            }
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
                n_name = st.text_input("Nombre", u["name"])
                if st.form_submit_button("Actualizar"):
                    payload = {
                        "name": n_name,
                        "edad": u["edad"],
                        "sexo": u["sexo"],
                        "telefono": u["telefono"],
                        "email": u["email"],
                    }
                    resp, msg = safe_request(
                        "PUT", f"{API_URL}/{u['id_user']}", payload
                    )
                    if resp and resp.status_code == 200:
                        st.success("Actualizado")
                    else:
                        st.error(f"Error: {msg}")
        with c2:
            if st.button("Eliminar", type="primary"):
                resp, msg = safe_request("DELETE", f"{API_URL}/{u['id_user']}")
                if resp and resp.status_code in [200, 204]:
                    st.success("Eliminado")
                    st.rerun()
                else:
                    st.error(f"Error: {msg}")