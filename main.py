import streamlit as st

# Everything is accessible via the st.secrets dict:

st.title("Resultados")

st.write("DB username:", st.secrets["db_username"])


