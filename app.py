import streamlit as st
import hashlib
import pandas as pd
import os
import re

# Configurar el nombre de la barra lateral
st.sidebar.title("ChronoShift")

# Función que genera passwords consistentes a partir de una clave
def generar_password(clave):
    hash_object = hashlib.sha256(clave.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:5].upper()

# Función para guardar registros en CSV
def guardar_registro(clave_original, password):
    archivo = 'registros.csv'
    existe_archivo = os.path.isfile(archivo)
    df_nuevo = pd.DataFrame({'ClaveOriginal':[clave_original], 
                             'PasswordGenerado':[password]})
    if not existe_archivo:
        df_nuevo.to_csv(archivo, index=False)
    else:
        df_nuevo.to_csv(archivo, mode='a', header=False, index=False)

# Streamlit App - Main Content
st.title("🔐 Generador persistente de Passwords")

clave_usuario = st.text_input("Introduce una clave (6 números seguidos de una letra):",
                              type="password")

def es_clave_valida(clave):
    return re.match(r"^\d{6}[a-zA-Z]$", clave)

if st.button("Generar password"):
    if clave_usuario and es_clave_valida(clave_usuario):
        resultado = generar_password(clave_usuario)
        guardar_registro(clave_usuario, resultado)
        st.success(f"Tu password generado es: **{resultado}**")
        
        # Agregar un botón para copiar al portapapeles usando JavaScript
        st.markdown(f"""
            <button onclick="navigator.clipboard.writeText('{resultado}'); alert('Password copiado al portapapeles!')">
                Copiar al portapapeles
            </button>
            """, unsafe_allow_html=True)
    else:
        st.warning("Por favor ingresa una clave válida (6 números seguidos de una letra).")

# Sidebar - Protected Section
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

clave_chronoshift = st.sidebar.text_input("Introduce la contraseña para ChronoShift:", type="password")

def autenticar_clave(contraseña):
    contraseña_correcta = "tu_contraseña_segura"
    return contraseña == contraseña_correcta

if st.sidebar.button("Acceder"):
    if autenticar_clave(clave_chronoshift):
        st.sidebar.success("Acceso concedido.")
        st.session_state.access_granted = True
    else:
        st.sidebar.error("Contraseña incorrecta.")

if st.session_state.access_granted and os.path.exists('registros.csv'):
    with st.sidebar.expander("ChronoShift"):
        try:
            df_registros = pd.read_csv('registros.csv')
            st.dataframe(df_registros)
        except pd.errors.EmptyDataError:
            st.sidebar.error("El archivo de registros está vacío o corrupto.")
