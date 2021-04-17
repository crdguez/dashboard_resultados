import streamlit as st
import requests
import pandas as pd
from io import StringIO

import intro
import analisis

PAGES = {
    "Introducción": intro,
    "Análisis": analisis,

}

st.set_page_config(
    page_title='Análisis de Resultados',
    page_icon="🧊",
    layout='wide')
st.sidebar.title('IES Pedro Cerrada')
key = st.sidebar.text_input('clave de acceso:', type="password")
if key == st.secrets["PASS"] :
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

# key = st.text_input('clave de acceso:')
#
# if key == st.secrets["USUARIO"] :
#   url='https://gitlab.com/api/v4/projects/16754108/repository/files/importado1.csv/raw'
#   #url='https://gitlab.com/api/v4/projects/8982377/repository/files/importado1.csv/raw?ref=master&private_token='+st.secrets["TOKEN"]
#   st.write(url)
#   df = pd.read_csv(StringIO(requests.get(url).text))
#
#   eval=1
#   pre_actilla = pd.read_csv(StringIO(requests.get(url).text), index_col=False, encoding='utf-8')
#   pre_actilla = pre_actilla.drop([col for col in pre_actilla if col.startswith('Unna')], axis=1)
#   pre_actilla = pre_actilla.drop("Nº MNS", axis = 1)
#   pre_actilla = pd.melt(pre_actilla, id_vars=["Nº","Apellidos, Nombre"], var_name="Asignatura", value_name="Nota")
#   pre_actilla = pre_actilla[pre_actilla['Nota'].notna()]
#   pre_actilla = pre_actilla.copy()
#   pre_actilla['Eval'] = eval
#   pre_actilla.Asignatura=pre_actilla.Asignatura.str.replace('\n', ' ')
#   actilla_final = pre_actilla
#   actilla_final = actilla_final.rename(columns={'Apellidos, Nombre':'Alumno'})
#   actilla_final = actilla_final[['Alumno','Asignatura','Eval','Nota']]
#   actilla_final['Suspenso']=0
#
#   # Everything is accessible via the st.secrets dict:
#
#   st.title("Resultados")
#
#   st.write("Usuario:", st.secrets["USUARIO"])
#   st.dataframe(df)
#   st.dataframe(actilla_final)
#
# else :
#   st.write('Para acceder a los datos tienes que introducir una clave de acceso correcta')
