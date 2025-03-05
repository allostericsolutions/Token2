import streamlit as st
import hashlib
import pandas as pd
import os
import re

# =========================================================================
# 1. Configurar el título de la barra lateral y la sección "ChronoShift"
# =========================================================================
st.sidebar.title("ChronoShift")

# =========================================================================
# 2. Función que genera un password consistente a partir de la clave
# =========================================================================
def generar_password(clave):
    hash_object = hashlib.sha256(clave.encode())  
    hex_dig = hash_object.hexdigest()
    return hex_dig[:5].upper()  # Devolvemos los primeros 5 caracteres en mayúscula

# =========================================================================
# 3. Función de guardado de registros en CSV
# =========================================================================
def guardar_registro(clave_original, password):
    archivo = 'registros.csv'
    existe_archivo = os.path.isfile(archivo)
    df_nuevo = pd.DataFrame({'ClaveOriginal': [clave_original], 
                             'PasswordGenerado': [password]})
    if not existe_archivo:
        df_nuevo.to_csv(archivo, index=False)
    else:
        df_nuevo.to_csv(archivo, mode='a', header=False, index=False)

# =========================================================================
# 4. Validación de la clave (6 números seguidos de 1 letra)
# =========================================================================
def es_clave_valida(clave):
    # Asegura 6 dígitos seguidos por una sola letra (mayúscula o minúscula)
    patron = r'^\d{6}[A-Za-z]$'
    return bool(re.match(patron, clave))

# =========================================================================
# 5. Interfaz Principal
# =========================================================================
st.title("🔐 Generador persistente de Passwords")

# Campo para que el usuario ingrese la clave
clave_usuario = st.text_input(
    "Introduce una clave (6 números seguidos de una letra):", 
    type="password"
)

# Botón para generar el password
if st.button("Generar password"):
    if clave_usuario and es_clave_valida(clave_usuario):
        resultado = generar_password(clave_usuario)
        guardar_registro(clave_usuario, resultado)
        
        st.success("Tu password generado es:")
        # Texto "click & copy" sin botón adicional
        st.markdown(
            f"""
            <p 
              style="cursor: pointer; color: blue; text-decoration: underline; font-size: large;" 
              onclick="navigator.clipboard.writeText('{resultado}').then(() => alert('¡Password copiado al portapapeles!')).catch(err => console.error(err));">
              {resultado}
            </p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("La clave debe ser 6 dígitos y 1 letra. Ejemplo: 123456A")

# =========================================================================
# 6. Sección Protegida en la Barra Lateral (Visualización de registros)
# =========================================================================
# Control de acceso
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

# Campo de contraseña para acceder a la sección "ChronoShift"
clave_chronoshift = st.sidebar.text_input("Introduce la contraseña para ChronoShift:", type="password")

def autenticar_clave(contraseña):
    contraseña_correcta = "tu_contraseña_segura"  # Cámbiala por la que desees
    return contraseña == contraseña_correcta

if st.sidebar.button("Acceder"):
    if autenticar_clave(clave_chronoshift):
        st.sidebar.success("Acceso concedido.")
        st.session_state.access_granted = True
    else:
        st.sidebar.error("Contraseña incorrecta.")

# Si tiene acceso y el CSV existe, se despliega el contenido
if st.session_state.access_granted and os.path.exists('registros.csv'):
    with st.sidebar.expander("ChronoShift"):
        try:
            df_registros = pd.read_csv('registros.csv')
            st.dataframe(df_registros)
        except pd.errors.EmptyDataError:
            st.sidebar.error("El archivo de registros está vacío o corrupto.")
