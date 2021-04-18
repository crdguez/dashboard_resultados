import streamlit as st
import pandas as pd
from io import StringIO
import requests

def app() :

    st.title('Ánalisis de resultados (en construcción)')
    # url='https://gitlab.com/api/v4/projects/16754108/repository/files/importado1.csv/raw'
    url='https://gitlab.com/api/v4/projects/8982377/repository/files/importado1.csv/raw?ref=master&private_token='+st.secrets["TOKEN"]
    # st.write(url)
    df = pd.read_csv(StringIO(requests.get(url).text))
    eval=1
    pre_actilla = pd.read_csv(StringIO(requests.get(url).text), index_col=False, encoding='utf-8')
    pre_actilla = pre_actilla.drop([col for col in pre_actilla if col.startswith('Unna')], axis=1)
    pre_actilla = pre_actilla.drop("Nº MNS", axis = 1)
    pre_actilla = pd.melt(pre_actilla, id_vars=["Nº","Apellidos, Nombre"], var_name="Asignatura", value_name="Nota")
    pre_actilla = pre_actilla[pre_actilla['Nota'].notna()]
    pre_actilla = pre_actilla.copy()
    pre_actilla['Eval'] = eval
    pre_actilla.Asignatura=pre_actilla.Asignatura.str.replace('\n', ' ')
    actilla_final = pre_actilla
    actilla_final = actilla_final.rename(columns={'Apellidos, Nombre':'Alumno'})
    actilla_final = actilla_final[['Alumno','Asignatura','Eval','Nota']]
    actilla_final['Suspenso']=0

    # Everything is accessible via the st.secrets dict:

    st.title("Resultados")

    st.write("Usuario:", st.secrets["USUARIO"])
    st.dataframe(df)
    st.dataframe(actilla_final)
