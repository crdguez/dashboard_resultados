import streamlit as st

st.title("Hola, aquí irá la aplicación ...")
st.write("Nos vemos pronto")


st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

# And the root-level secrets are also accessible as environment variables:

import os
st.write(
	"Has environment variables been set:",
	os.environ["db_username"] == st.secrets["db_username"])
