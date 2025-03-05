import streamlit as st
import hashlib
import pandas as pd
import os

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

# Streamlit App
st.title("🔐 Generador persistente de Passwords")

clave_usuario = st.text_input("Introduce tu clave alfanumérica:", 
                              type="password")

if st.button("Generar password"):
    if clave_usuario:
        resultado = generar_password(clave_usuario)
        guardar_registro(clave_usuario, resultado)
        st.success(f"Tu password generado es: **{resultado}**")
    else:
        st.warning("Por favor ingresa una clave válida.")

# Check if the 'registros.csv' file exists and display its content
if os.path.exists('registros.csv'):
    try:
        df_registros = pd.read_csv('registros.csv')
        with st.expander("Ver registros guardados"):
            st.dataframe(df_registros)
    except pd.errors.EmptyDataError:
        st.error("El archivo de registros está vacío o corrupto.")
