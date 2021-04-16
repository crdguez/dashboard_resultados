import streamlit as st
import requests
import requests
import pandas as pd
from io import StringIO

key = ''
if key == st.secrets["USUARIO"] :
  url='https://gitlab.com/api/v4/projects/16754108/repository/files/importado1.csv/raw'
  #url='https://gitlab.com/api/v4/projects/8982377/repository/files/importado1.csv/raw?ref=master&private_token='+st.secrets["TOKEN"]
  st.write(url)
  df = pd.read_csv(StringIO(requests.get(url).text))

  # Everything is accessible via the st.secrets dict:

  st.title("Resultados")

  st.write("Usuario:", st.secrets["USUARIO"])
  st.dataframe(df)
  
else :
  st.write('Para acceder a los datos tienes que introducir una clave de acceso')

key = st.text_input('clave de acceso:')  
