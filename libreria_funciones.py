import streamlit as st
import pandas as pd
from io import StringIO
import requests
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def pre_actilla(url, eval=1):
    fichero = url
    pre_actilla = pd.read_csv(fichero, index_col=False, encoding='utf-8')
    # pre_actilla = pd.read_csv(StringIO(requests.get(url).text), index_col=False, encoding='utf-8')
    pre_actilla = pre_actilla.drop([col for col in pre_actilla if col.startswith('Unna')], axis=1)
    pre_actilla = pre_actilla.drop("Nº MNS", axis = 1)
    pre_actilla = pd.melt(pre_actilla, id_vars=["Nº","Apellidos, Nombre"], var_name="Asignatura", value_name="Nota")
    pre_actilla = pre_actilla[pre_actilla['Nota'].notna()]
    pre_actilla = pre_actilla.copy()
    pre_actilla['Eval'] = eval
    pre_actilla.Asignatura=pre_actilla.Asignatura.str.replace('\n', ' ')
    return pre_actilla

def datos_brutos(urls) :
    datos_brutos = pd.concat([pre_actilla(urls[i], i+1) for i in range(len(urls))])
    datos_brutos = datos_brutos.rename(columns={'Apellidos, Nombre':'Alumno'})
    datos_brutos = datos_brutos[['Alumno','Asignatura','Eval','Nota']]
    datos_brutos['Suspenso']=0
    # Si sale algún no presentado hay que ejecutar lo siguiente
    #datos_brutos = datos_brutos.drop(datos_brutos[datos_brutos.Nota == 'NP'].index)
    datos_brutos.Nota = pd.to_numeric(datos_brutos.Nota)
    datos_brutos.loc[datos_brutos['Nota'] < 5, 'Suspenso'] = 1
    datos_brutos.Nota = datos_brutos.Nota.astype(int)
    return  datos_brutos

def actilla(urls):
    #Se le pasa una lista de ficheros y devuelve: datos_actilla, actilla sin estilo, actilla con estilo

    actilla = datos_brutos(urls)
    actilla = actilla.iloc[actilla['Alumno'].str.normalize('NFKD').argsort()]

    # modificar actilla

    ultima_evaluacion = len(urls)
    df = actilla[actilla.Eval.isin([ultima_evaluacion, ultima_evaluacion -1])]

    df1 = df.set_index(['Alumno','Asignatura','Eval']).Nota.astype(int).unstack('Asignatura').unstack('Eval').sort_values(by='Alumno', key=lambda col: [str(i) for i in col])

    # Normalizamos los datos para que salgan ordenados
    df1 = df1.iloc[df1.index.str.normalize('NFKD').argsort()]

    df2=actilla[actilla.Eval == ultima_evaluacion].groupby(['Alumno','Eval'])[['Nota']].mean().unstack('Eval').sort_values(by='Alumno', key=lambda col: [str(i) for i in col]).rename(columns={'Nota':'NM'})
    df3 = df.groupby(['Asignatura','Eval'])[['Nota']].mean()

    df4 = pd.concat([df1,df3.T.rename(index={'Nota': 'Media'})])

    # #calculamos el número de suspensos por asignatura y porcentaje

    df7=df.groupby(['Asignatura','Eval'])[['Suspenso']].aggregate(['sum','count'])
    df7[('Suspenso','porc')]=df7[('Suspenso','sum')]/df7[('Suspenso','count')]
    df7.columns=df7.columns.get_level_values(1)
    df7.T

    df4 = pd.concat([df4,df7[['sum','porc']].T.rename(index={'sum':'nsusp','porc':'%'})], sort=False)

    df5 = pd.concat([df4,df2], axis=1, sort=False)
    df6 = actilla[actilla.Eval == ultima_evaluacion].groupby(['Alumno','Eval'])[['Suspenso']].sum().unstack('Eval').sort_values(by='Alumno', key=lambda col: [str(i) for i in col]).rename(columns={'Suspenso':'MNS'})
    df5 = pd.concat([df5,df6], axis=1, sort=False)


    # # calculamos la media de las medias de las notas y la suma total de suspensos
    df5.iloc[-3:-2,-2:-1]=df2.mean()[0]
    df5.iloc[-2:-1,-1:]=df6.sum()[0]

    actilla_estilada = df5.style.set_precision(0) \
        .format("{:.0%}",subset=(df5.index[-1:],df5.columns[:-2])) \
        .format("{:.0f}",subset=(df5.index[-2:-1],df5.columns[:-2])) \
        .format("{:.1f}",subset=(df5.index[-3:-2],df5.columns[:-2])) \
        .format("{:.1f}",subset=(df5.index,df5.columns[-2:-1])) \
        .format("{:.0f}",subset=(df5.index,df5.columns[-1:0])) \
        .set_table_styles([{'selector': 'td','props': [('border', '1px solid black'),('text-align', 'center')]}, \
                           {'selector': 'tr','props': [('border', '1px solid black')]}, \
                           {'selector': 'th','props': [('border', '1px solid black'),('text-align', 'center'),('font-size','13px')]}, \
                          ] \
                         ) \
        .applymap(color_negative_red, subset=(df5.index[:-3],df5.columns[:-2])).highlight_null("white") \
        .applymap(color_media, subset=(df5.index[-3:-2],df5.columns)) \
        .applymap(evaluaciones_anteriores, subset=(df5.index[-2:],df5.columns[:])) \
        .applymap(color_media, subset=(df5.index[:-3],['NM'])) \
        .applymap(color_suspensos, subset=(df5.index[:-3],['MNS'])) \
        .applymap(evaluaciones_anteriores, subset=(df5.index,df5.columns[df5.columns.get_level_values(1) != ultima_evaluacion])) \
        .set_na_rep('-')

    return actilla, actilla_estilada


def analisis_df(df, txt_intro ="Tenemos los siguientes datos: \n " \
                ,txt_mejor="\n * Sube {}:", txt_peor="\n * **Baja** {}:", \
                txt_igual="\n * Se mantiene {}:", solo_diferencias=False, \
                modo=1) :
    # analiza los datos de un dataframe donde en el indice están las evaluaciones y en las columnas los items a analizar
    if max(df.index)  > 1 :
        # ix = list(df.index).index(ultima_evaluacion)
        ix = len(df.index) - 1
        txt = txt_intro
        for c in range(len(df.columns)) :
            if (df.iloc[ix,c] - df.iloc[ix-1,c]) > 0 : txt2 = txt_mejor.format(df[df.columns[c]].name)+" Pasa de {} a {}. ".format(str(df.iloc[ix-1,c]),str(df.iloc[ix,c]))
            elif (df.iloc[ix,c] - df.iloc[ix-1,c]) < 0 : txt2 = txt_peor.format(df[df.columns[c]].name)+" Pasa de {} a {}. ".format(str(df.iloc[ix-1,c]),str(df.iloc[ix,c]))
            elif (solo_diferencias) : txt2=""
            else : txt2 = txt_igual.format(df[df.columns[c]].name)+" {}. ".format(str(df.iloc[ix,c]))
            txt += txt2
    else :
        txt = txt_intro
        if modo ==1 :
            txt += ", ".join(["**{}** es {}".format(df[df.columns[c]].name,str(df.iloc[0,c])) for c in range(len(df.columns))])
        elif modo == 2 :
            txt += " ".join(["\n* **{}**: {}".format(df[df.columns[c]].name,str(df.iloc[0,c])) for c in range(len(df.columns))])+" \n "
        else :
            txt += ", ".join(["**{}**: {}".format(df[df.columns[c]].name,str(df.iloc[0,c])) for c in range(len(df.columns))])+" \n "
    return txt+" \n ", [df[df.columns[i]] for i in range(len(df.columns))]


def analisis_alumno(df,a,eval) :
    #Resumen de resultados
    ultima_evaluacion=eval
    df2 = df[(df.Alumno == a) & (df.Eval <= ultima_evaluacion)].groupby(['Alumno','Eval']).aggregate({'Nota':'mean','Suspenso':'sum'})
    df2.index = df2.index.get_level_values(1)
    df2.Nota = df2.Nota.round(2)
    df2 = df2.rename(columns={'Nota':'Nota media', 'Suspenso':'Número de suspensos'})
    st.subheader(a)
    # st.dataframe(df2)
    st.write(analisis_df(df2, "En la {}ª evaluación: \n ".format(ultima_evaluacion),txt_igual="\n * Mantiene {}")[0])

    #Lista de suspensos
    df2 = df[(df.Alumno==a) & (df.Suspenso==1) & (df.Eval == ultima_evaluacion)][['Asignatura','Eval','Suspenso']]
    if len(df2[['Asignatura']].values) > 0 :
        st.write("Asignaturas suspendidas: "+",".join(list(df2['Asignatura'])))
        # st.dataframe(df2)

    #Análisis de las notas
    df2 = df[(df.Alumno == a) & (df.Eval <= ultima_evaluacion)].iloc[:,1:-1].groupby(['Asignatura','Eval']).min().unstack('Asignatura')
    df2.columns = df2.columns.get_level_values(1)
    st.write('**Calificaciones obtenidas por evaluación:**')
    st.dataframe(df2.style.applymap(color_negative_red).highlight_null("white"))
    # st.write(analisis_df(df2, "Resultados: \n ", "Sube en {}:", "Baja en {}:", "En {}:", solo_diferencias=True)[0])

    g = df2.T.plot.barh(title=a, xlabel ="", width=0.8)
    g.legend(loc='lower left')

    for p in g.patches:
        g.annotate(str(p.get_width()), (p.get_width() , p.get_y()*1.01))
    fig3=g.get_figure()
    st.pyplot(fig3)




# Funciones para estilo

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    if type(val)== str:
        color = 'blue ; background: azure'
    else:
        color = 'red; background: khaki' if (val < 5 or val =="") else 'green; background: lightyellow'
    return 'color: %s ; font-size: 20px ; font-weight: bold' % color

def color_media(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    if type(val)== str:
        color = 'blue ; background: azure'
    else:
        color = 'red; background: gold' if (val < 5 or val =="") else 'black; background: burlywood'
    return 'color: %s ; font-size: 14px ; font-weight: bold'  % color

def color_suspensos(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    if type(val)== str:
        color = 'blue ; background: azure'
    else:
        color = 'red; background: gold' if (val > 0 or val =="") else 'black; background: darkkhaki'

    return 'color: %s ; font-weight: bold ; font-size: 14px' % color

def evaluaciones_anteriores(val):
    if type(val)== str:
        color = 'blue ; background: azure'
    else:
        #color = 'red; background: khaki' if (val < 5 or val =="") else 'green; background: ghostwhite'
        color = 'blue ; background: azure'

    return 'color: %s ; font-size: 16px ; font-weight: bold' % color
