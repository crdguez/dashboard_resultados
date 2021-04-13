# dashboard_resultados

### Lanzando un contendor docker con Streamlit y la aplicacion *main.py*

He creado un fichero *main.py* con el código de *streamlit*. Si no tengo el docker creado, lo creo con el siguiente comando:

```
docker run -it -p 8502:8502 --name resultados -v $PWD:/app crdguez/streamlit main.py
```