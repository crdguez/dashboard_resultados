import streamlit as st
import requests
import requests
from io import StringIO

url='https://gitlab.com/api/v4/projects/16754108/repository/files/importado1.csv/raw'
df = pd.read_csv(StringIO(requests.get(url).text))

# Everything is accessible via the st.secrets dict:

st.title("Resultados")

st.write("Usuario:", st.secrets["USUARIO"])
st.dataframe(df)


