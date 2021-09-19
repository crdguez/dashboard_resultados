# dashboard_resultados

Aplicación hecha en streamlit para visualizar estadísticas de las evaluaciones de mis diferentes cursos y grupos a partir de los datos de Sigad. a
En /.strreamlit/secrets.toml está el pass para poder ver los datos. Este fichero solo está en local. En la aplicación desplegada en el servicio de Streamlit hay que ir a la configuración de la apliación.

Los ficheros que lee la aplicación se encuentran en mi repositorio privado [https://gitlab.com/crdguez/actas_evaluacion](https://gitlab.com/crdguez/actas_evaluacion)

### Lanzando un contendor docker con Streamlit y la aplicacion *main.py*

He creado un fichero *main.py* con el código de *streamlit*. Si no tengo el docker creado, lo creo con el siguiente comando:

```
docker run -it -p 8502:8502 --name resultados -v $PWD:/app crdguez/streamlit main.py

```

Una vez creado podemos lanzarlo yendo desde un terminal:


```
docker start resultados

```

Y en un navegador: [http://localhost:8501/](http://localhost:8501/) .
