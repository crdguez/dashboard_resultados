import streamlit as st
import requests
import requests
import pandas as pd
from io import StringIO


key = st.text_input('clave de acceso:') 

if key == st.secrets["USUARIO"] :
  url='https://gitlab.com/api/v4/projects/16754108/repository/files/importado1.csv/raw'
  #url='https://gitlab.com/api/v4/projects/8982377/repository/files/importado1.csv/raw?ref=master&private_token='+st.secrets["TOKEN"]
  st.write(url)
  df = pd.read_csv(StringIO(requests.get(url).text))
  
  pre_actilla = pd.read_csv(StringIO(requests.get(url).text), index_col=False, encoding='utf-8')
  pre_actilla = pre_actilla.drop([col for col in pre_actilla if col.startswith('Unna')], axis=1)
  pre_actilla = pre_actilla.drop("Nº MNS", axis = 1)
  pre_actilla = pd.melt(pre_actilla, id_vars=["Nº","Apellidos, Nombre"], var_name="Asignatura", value_name="Nota")
  pre_actilla = pre_actilla[pre_actilla['Nota'].notna()]
  pre_actilla = pre_actilla.copy()
  pre_actilla['Eval'] = eval
  pre_actilla.Asignatura=pre_actilla.Asignatura.str.replace('\n', ' ')

  # Everything is accessible via the st.secrets dict:

  st.title("Resultados")

  st.write("Usuario:", st.secrets["USUARIO"])
  st.dataframe(df)
  st.dataframe(pre_actilla)
  
else :
  st.write('Para acceder a los datos tienes que introducir una clave de acceso correcta')


