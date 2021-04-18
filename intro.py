# intro.py
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

def app() :
    st.spinner("Un poco de paciencia ...")
    st.title('Análisis de Resultados')
    col11, col12 = st.beta_columns([1,1])

    with col12 :
    # image = Image.open('img/parabolas_red.jpg')
    # st.image(image, caption='Photo by Ricardo Gomez Angel', use_column_width=True)
        image = Image.open('img_intro.png')
        st.image(image, caption='', use_column_width=True)
    with col11:
        st.write('Aplicación para consultar **estadísticas** a  \
        partir de los resultados de la evaluación.   ',\
        '  \n Para poder acceder a los contenidos es necesario introducir **clave de acceso** ya que \
        se accede a **datos confidenciales**.')
        st.warning(':arrow_left: :key: Introduce la **clave de acceso** en el menú de la izquierda para acceder a las **opciones**')

        st.subheader('Sobre el proyecto')
        st.markdown('- Autor: *Carlos Rodríguez*  \n -   :exclamation: [Repositorio *Github*](https://github.com/crdguez/dashboard_resultados)' )
        st.subheader('Licencia')
        st.write('Tanto el código como la aplicación se publican con **licencia libre**. \
          \n * En caso de uso, se agradece la atribución :+1: \
            \n * Así mismo, se agradecen sugerencias y contribuciones \
            a través de *pull requests* en el repositorio')
