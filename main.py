import streamlit as st
import requests
import pandas as pd
import gitlab

from io import StringIO

import intro
import analisis
import analumno

PAGES = {
    "Introducción": intro,
    "Resultados generales": analisis,
    "Resultados por alumno": analumno,

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

    gl = gitlab.Gitlab('https://gitlab.com', private_token=st.secrets["TOKEN"])
    p=gl.projects.get(8982377)
    # st.write(p.repository_tree('datos_actas'))
    df = pd.DataFrame(p.repository_tree('datos_actas'))
    # st.write(list(df['name']))

    col1, col2, col3 = st.sidebar.beta_columns([1.5,1.5,1])
    with col1 :
        # curso = st.sidebar.selectbox('Curso', list(df['name'].sort_values(ascending=False)))
        curso = st.selectbox('Curso', list(df['name'].sort_values(ascending=False)))
    with col2 :
        df2 = pd.DataFrame(p.repository_tree('datos_actas/'+curso))
        clase = st.selectbox('Grupo', list(df2['name']))
    with col3 :
        df3 = pd.DataFrame(p.repository_tree('datos_actas/'+curso+'/'+clase))
        lista_evaluaciones = list(reversed(range(1,len(list(df3['name']))+1)))
        eval = st.selectbox('Evaluación', lista_evaluaciones)

    # st.write(curso)
    # st.write(clase)
    # st.write(eval)

    # lista_evaluaciones = ['1','2']

    # eval = int(st.sidebar.selectbox('Seleccione evaluación:',lista_evaluaciones, index=len(lista_evaluaciones)-1))
    # eval = int(st.sidebar.selectbox('Seleccione evaluación:',lista_evaluaciones, index=len(lista_evaluaciones)-1))

    OPCIONES =  {
        'curso': curso,
        'clase': clase,
        'eval': eval
    }
    # st.sidebar.header('Navegación')
    selection = st.sidebar.radio("Navegar a:", list(PAGES.keys()),index=0)
    if selection == list(PAGES.keys())[1] :
        # Aquí le pasaré la función
        # tipo = st.sidebar.radio("Tipo de función:", list(FUNCIONES.keys()),index=1)
        analisis.app(OPCIONES)
    if selection == list(PAGES.keys())[2] :
        analumno.app(OPCIONES)
    if selection == list(PAGES.keys())[0] :
        # Aquí le pasaré la función
        intro.app()

else :
    intro.app()

st.sidebar.header('Autor')
st.sidebar.info('* Aplicación desarrollada por **Carlos Rodríguez** \
    \n * El [código fuente](https://github.com/crdguez/dashboard_resultados) se publica con **licencia libre**')
