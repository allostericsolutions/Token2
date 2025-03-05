import streamlit as st
import hashlib
import pandas as pd
import os
import re

# ─────────────────────────────────────────────────────────────────────
# 1. Configuración de la barra lateral y título principal
# ─────────────────────────────────────────────────────────────────────
st.sidebar.title("ChronoShift")
st.title("🔐 Generador persistente de Passwords")

# ─────────────────────────────────────────────────────────────────────
# 2. Función que genera un password consistente a partir de 6 dígitos + 1 letra
# ─────────────────────────────────────────────────────────────────────
def generar_password(clave):
    hash_object = hashlib.sha256(clave.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:5].upper()

# ─────────────────────────────────────────────────────────────────────
# 3. Función para guardar registros en un CSV
# ─────────────────────────────────────────────────────────────────────
def guardar_registro(clave_original, password):
    archivo = 'registros.csv'
    existe_archivo = os.path.isfile(archivo)
    df_nuevo = pd.DataFrame({
        'ClaveOriginal': [clave_original], 
        'PasswordGenerado': [password]
    })
    if not existe_archivo:
        df_nuevo.to_csv(archivo, index=False)
    else:
        df_nuevo.to_csv(archivo, mode='a', header=False, index=False)

# ─────────────────────────────────────────────────────────────────────
# 4. Validación de la clave (6 números seguidos de 1 letra)
# ─────────────────────────────────────────────────────────────────────
def es_clave_valida(clave):
    return bool(re.match(r'^\d{6}[A-Za-z]$', clave))

# ─────────────────────────────────────────────────────────────────────
# 5. Interfaz principal: ingreso de la clave y generación del password
# ─────────────────────────────────────────────────────────────────────
clave_usuario = st.text_input("Introduce una clave (6 números seguidos de una letra):",
                              type="password")

if st.button("Generar password"):
    if clave_usuario and es_clave_valida(clave_usuario):
        # Generar y mostrar password
        resultado = generar_password(clave_usuario)
        guardar_registro(clave_usuario, resultado)
        st.success("Tu password generado es:")
        
        # Bloque de código que incluye el icono de copiado (Streamlit 1.28+)
        st.code(resultado, language="bash")

    else:
        st.warning("La clave debe ser 6 dígitos seguidos de 1 letra. Ej: 123456A")

# ─────────────────────────────────────────────────────────────────────
# 6. Sección protegida en la barra lateral para ver registros (ChronoShift)
# ─────────────────────────────────────────────────────────────────────
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

clave_chronoshift = st.sidebar.text_input("Introduce la contraseña para ChronoShift:",
                                          type="password")

def autenticar_clave(contraseña):
    # Cambia "tu_contraseña_segura" por la contraseña que desees
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
