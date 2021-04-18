import streamlit as st
import requests
import pandas as pd
from io import StringIO

import intro
import analisis

PAGES = {
    "Introducción": intro,
    "Resultados generales": analisis,

}

st.set_page_config(
    page_title='Análisis de Resultados',
    page_icon="🧊",
    layout='wide')
st.sidebar.title('IES Pedro Cerrada')

st.sidebar.header('Acceso')

key = st.sidebar.text_input('Introduce clave de acceso:', type="password")
if key == st.secrets["PASS"] :
    st.sidebar.header('Opciones')
    selection = st.sidebar.radio("Selecciona:", list(PAGES.keys()),index=0)

    if selection == list(PAGES.keys())[1] :
        # Aquí le pasaré la función
        # tipo = st.sidebar.radio("Tipo de función:", list(FUNCIONES.keys()),index=1)

        analisis.app()
    if selection == list(PAGES.keys())[0] :
        # Aquí le pasaré la función
        intro.app()

else :
    intro.app()

st.sidebar.header('Autor')
st.sidebar.info('* Aplicación desarrollada por **Carlos Rodríguez** \
    \n * El [código fuente](https://github.com/crdguez/dashboard_resultados) se publica con **licencia libre**')
