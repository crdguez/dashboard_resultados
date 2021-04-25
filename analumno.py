from libreria_funciones import *


def app(OPCIONES) :



    # lista_evaluaciones = ['1','2','3']
    # lista_evaluaciones = ['1','2']
    # eval = int(st.sidebar.selectbox('Selecciona evaluación:',lista_evaluaciones, index=len(lista_evaluaciones)-1))
    curso=OPCIONES['curso']
    clase=OPCIONES['clase']
    eval=OPCIONES['eval']
    st.title('Resultados por alumno en la '+str(eval)+'ª evaluación')
    st.markdown('---')

    # url='https://gitlab.com/api/v4/projects/16754108/repository/files/importado1.csv/raw'
    # url='https://gitlab.com/api/v4/projects/8982377/repository/files/importado1.csv/raw?ref=master&private_token='+st.secrets["TOKEN"]
    # urls=['https://gitlab.com/api/v4/projects/8982377/repository/files/importado'+str(i+1)+'.csv/raw?ref=master&private_token='+st.secrets["TOKEN"] for i in range(eval)]
    urls=[r'https://gitlab.com/api/v4/projects/8982377/repository/files/datos_actas%2F'+curso+r'%2F'+clase+r'%2Fimportado'+str(i+1)+'.csv/raw?ref=master&private_token='+st.secrets["TOKEN"] for i in range(eval)]
    # st.subheader('Actilla')
    ultima_evaluacion = len(urls)

    datos_act, datos_act_estilada = actilla(urls)
    #Seleccionamos alumno
    al = st.selectbox('Alumno:',list(datos_act['Alumno'].unique()))
    # st.header("Resultados de "+al+" en la "+str(eval)+"ª evaluación")

    analisis_alumno(datos_act,al,eval)

    #st.dataframe(datos_brutos(urls))

    # st.dataframe(datos_act_estilada)
    #
    #
    # st.subheader('Resumen de resultados')
    #
    # df = datos_act.groupby(['Eval'])[['Alumno','Nota','Suspenso']].aggregate({'Alumno':'nunique','Nota':'mean','Suspenso':'sum'}).rename(columns={'Alumno':'N_al', 'Nota':'Media', 'Suspenso':'N_susp'})
    # df['Susp_alu']=(df['N_susp']/df['N_al']).round(2)
    # df['Media']=df['Media'].round(2)
    # df2 = df.rename(columns={'N_al':'número de alumnos', 'Media':'nota media', 'N_susp':'número de suspensos','Susp_alu':'número de suspensos por alumno'}).iloc[:,1:]
    #
    # st.info(analisis_df(df2,txt_intro="A nivel de grupo, se tienen los siguientes datos: \n ", modo=2)[0])
    #
    #
    # fig = plt.figure(figsize=(22,15))
    # fig.suptitle('Estadísticas {}ª Evaluación'.format(ultima_evaluacion), fontsize=20)
    # gs = gridspec.GridSpec(nrows=2, ncols=2, height_ratios=[2, 1])
    #
    # ax0 = fig.add_subplot(gs[1, :])
    # df=datos_act.groupby(['Alumno','Eval'])[['Nota']].mean().round(2).rename(columns={'Nota':'Media'}).unstack()
    # df.columns = df.columns.get_level_values(1)
    # g3=df.plot.bar(title='Nota media por alumno',ax=ax0, xlabel="", fontsize=18)
    # g3.legend(loc='lower right')
    # for p in g3.patches:
    #     g3.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    #
    # ax1 = fig.add_subplot(gs[0, 0])
    # df = datos_act[datos_act.Eval==ultima_evaluacion].groupby('Alumno').mean().Nota
    # ranges = [0,3,4,5,6,7,9,10]
    # df2 = df.groupby(pd.cut(df, ranges, right=False)).count()
    # df2.name = 'Alumnos'
    # g1=df2[df2 > 0].plot(kind='pie', title = 'Alumnos y Nota media',autopct='%1.1f%%', legend = True, table=True, ax=ax1, ylabel="", fontsize=24)
    # # , fontsize=24
    # ax2 = fig.add_subplot(gs[0, 1])
    # df = datos_act[datos_act.Eval==ultima_evaluacion].groupby('Alumno').sum().Suspenso
    # ranges = [0,1,2,3,5,10]
    # df2 = df.groupby(pd.cut(df, ranges, right=False)).count()
    # df2.index=['0 susp.','1 susp.','2 susp.','3 ó 4 susp.','> 4 susp.']
    # df2.name = 'Alumnos'
    # g4=df2[df2 > 0].plot(kind='pie', title = 'Alumnos y suspensos',autopct='%1.1f%%', table=True, ax=ax2, ylabel="", fontsize=24)
    #
    # st.pyplot(fig)
    #
    #
    # # st.write("Usuario:", st.secrets["USUARIO"])
