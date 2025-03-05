import streamlit as st
import hashlib
import pandas as pd
import os
import re

# --------------------------------------------------------------------
# Inyectamos CSS para ajustar el ancho de TODOS los st.code() en la app
# --------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Ajusta el ancho de los bloques de código */
    div[data-testid="stCodeBlock"] pre {
        width: 10rem !important;       /* Ajusta a tu gusto (10rem ~ 160px) */
        max-width: 10rem !important;   /* Evita que se expanda más que 10rem */
        white-space: pre-wrap;         /* Permite el salto de línea si es muy largo */
        word-wrap: break-word;         /* Ajusta la palabra a la línea */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------------------------
# Configurar el nombre de la barra lateral y el título principal
# --------------------------------------------------------------------
st.sidebar.title("ChronoShift")
st.title("🔐 Generador persistente de Passwords")

# --------------------------------------------------------------------
# Función que genera un password consistente a partir de 6 dígitos + 1 letra
# --------------------------------------------------------------------
def generar_password(clave):
    hash_object = hashlib.sha256(clave.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:5].upper()

# --------------------------------------------------------------------
# Función para guardar registros en CSV
# --------------------------------------------------------------------
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

# --------------------------------------------------------------------
# Validación de la clave (6 números + 1 letra)
# --------------------------------------------------------------------
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
        # Generar y mostrar password
        resultado = generar_password(clave_usuario)
        guardar_registro(clave_usuario, resultado)
        
        st.success("Tu password generado es:")
        # Usamos st.code para mostrar el texto con botón de copiado integrado
        st.code(resultado, language="bash")
    else:
        st.warning("La clave debe ser 6 dígitos seguidos de 1 letra, ej: 123456A.")

# --------------------------------------------------------------------
# Sección protegida en la barra lateral para ver los registros
# --------------------------------------------------------------------
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

def autenticar_clave(contraseña):
    # Ajusta "tu_contraseña_segura" por la que prefieras
    contraseña_correcta = "francisco14%"
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
        st.sidebar.error("Buen intento, aquí no es.")

# Solo muestra la sección de registros si hay acceso concedido y si existe registros.csv
if st.session_state.access_granted and os.path.exists('registros.csv'):
    with st.sidebar.expander("ChronoShift"):
        try:
            df_registros = pd.read_csv('registros.csv')
            st.dataframe(df_registros)
        except pd.errors.EmptyDataError:
            st.sidebar.error("El archivo de registros está vacío o corrupto.")
