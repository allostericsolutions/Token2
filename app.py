import streamlit as st
import hashlib
import pandas as pd
import os
import re

# --------------------------------------------------------------------
# Inyectamos CSS para ajustar el ancho de st.code() y
# colocar una imagen de fondo en la barra lateral
# --------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Barra lateral con imagen de fondo */
    [data-testid="stSidebar"] {
        background-image: url("https://storage.googleapis.com/allostericsolutionsr/Allosteric_Solutions.png");
        background-repeat: no-repeat;
        background-position: center;
        background-size: 80% auto;
    }

    /* Ajusta el ancho de los bloques de código */
    div[data-testid="stCodeBlock"] pre {
        width: 10rem !important;       /* Ajusta a tu gusto (~160px) */
        max-width: 10rem !important;   /* Evita que se expanda más */
        white-space: pre-wrap;         
        word-wrap: break-word;         
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------------------------
# Ajustes de la app
# --------------------------------------------------------------------
st.sidebar.title("ChronoShift")
st.title("🔐 Generador persistente de Passwords")

def generar_password(clave):
    hash_object = hashlib.sha256(clave.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:5].upper()

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

def es_clave_valida(clave):
    return bool(re.match(r'^\d{6}[A-Za-z]$', clave))

# --------------------------------------------------------------------
# Interfaz principal para generar el password
# --------------------------------------------------------------------
clave_usuario = st.text_input(
    "Introduce una clave (6 números seguidos de 1 letra):",
    type="password"
)

if st.button("Generar password"):
    if clave_usuario and es_clave_valida(clave_usuario):
        resultado = generar_password(clave_usuario)
        guardar_registro(clave_usuario, resultado)
        st.success("Tu password generado es:")
        st.code(resultado, language="bash")
    else:
        st.warning("La clave debe ser 6 dígitos seguidos de 1 letra, ej: 123456A.")

# --------------------------------------------------------------------
# Sección protegida en la barra lateral para ver los registros
# --------------------------------------------------------------------
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

def autenticar_clave(contraseña):
    contraseña_correcta = "francisco14%"  # Cámbiala por la que desees
    return contraseña == contraseña_correcta

clave_chronoshift = st.sidebar.text_input(
    "ChronoShift:",
    type="password"
)

if st.sidebar.button("Acceder"):
    if autenticar_clave(clave_chronoshift):
        st.sidebar.success("Acceso concedido.")
        st.session_state.access_granted = True
    else:
        st.sidebar.error("🛑 Buen intento, aquí no, es allá ➡")

if st.session_state.access_granted and os.path.exists('registros.csv'):
    with st.sidebar.expander("ChronoShift Admi"):
        try:
            df_registros = pd.read_csv('registros.csv')
            st.dataframe(df_registros)
        except pd.errors.EmptyDataError:
            st.sidebar.error("El archivo de registros está vacío o corrupto.")

        if st.button("Borrar registros"):
            if os.path.exists('registros.csv'):
                os.remove('registros.csv')
                st.success("Se han borrado todos los registros.")
                st.experimental_rerun()
            else:
                st.warning("No existe ningún archivo de registros.")
