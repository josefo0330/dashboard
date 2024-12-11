#-- coding: utf-8 --
import streamlit as st
import pandas as pd
import plotly.express as px  
from pymongo import MongoClient
#personalizacion
def app():
    #Funcion para limpiar cadenas con caracteres inrelevantes
    def dropCaracter (cadena):
        nuevaCadena=cadena.replace('(', '')
        nuevaCadena= nuevaCadena.replace(',','')
        return nuevaCadena
    def conection_mongo (host,port,username,password,db):
        if username and password:
            uri = 'mongodb://%s:%s@%s:%s/%s'%(username,password,host,port,db)
            conn=MongoClient (uri)
        else:
            conn=MongoClient (host,port)
        return conn [db]
    def read_mongo(db,colletion ,host= 'localhost', port= 27017, username=None, password = None, no_id= True):
        db =conection_mongo (host=host,port=port,username=username,password=password,db=db)
        cursor =db[colletion].find({})
        df = pd.DataFrame (list(cursor))

        if no_id:
            del df ['_id']
        return df
    #titulos
    st.title('UNIVERSIDAD DE PANAMA📈')
    st.image("https://th.bing.com/th/id/R.a6fb04281ed45e6ffb651299b5fd99e5?rik=Qscqw8WT%2b0yAbQ&riu=http%3a%2f%2fsites.ieee.org%2fpanama-pes%2ffiles%2f2013%2f06%2funiversidad-de-panama-logo.jpg&ehk=rBaEBLq%2bHN6AoAw2PsR7qvja4FckpBhUgzEFT0qMQkQ%3d&risl=&pid=ImgRaw&r=0", width=100, output_format= "PNG")
    dfE= read_mongo('cruv', 'estudiantes')
    #aux2=[]
    #i=0
    #st.dataframe(dfE) 
    #print(read_mongo('cruv', 'datos'))
    #selector
    with st.sidebar:
        st.title('UNIVERSIDAD DE PANAMA📈')
        year_list = ["FACULTAD","SEXO","TURNO"]
        selected_year = st.selectbox('SELECCIONE LA OPCION', year_list)
        df_selected_year = selected_year
    #----------
    st.subheader('ESTUDIANTES POR '+df_selected_year +'- CRUV')
    col = st.columns((1.5, 4.5, 0.5), gap='medium')
    total=0
    if df_selected_year== 'FACULTAD':
        df_grouped = dfE.groupby(by=['facultad'])['facultad'].count()   # -- GROUP DATAFRAME
        dataF= pd.DataFrame(df_grouped)
        dataF=dataF.rename(columns={'facultad': 'CANTIDAD DE ESTUDIANTES'})
        total = dataF['CANTIDAD DE ESTUDIANTES'].sum()
        with col[0]:
            st.metric(label="TOTAL-ESTUDIANTES", value=total )
        with col[1]:
            st.markdown('FACULTADES')
        #st.dataframe(df_grouped) 
            st.dataframe(dataF) 
            # -- PLOT DATAFRAME
        
        fig = px.bar(
        dataF,
        y='CANTIDAD DE ESTUDIANTES',
        color='CANTIDAD DE ESTUDIANTES',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Estudiantes  by facultades</b>')
        dfE_facult = dfE.groupby(by= ['facultad'])['facultad']
        dataFacult = pd.DataFrame(dfE_facult)
        column1= dataFacult.columns.tolist()
        listAux= dataFacult[column1[0]].tolist()
        for i in range (len(listAux)):
            aux= listAux[i]
            listAux[i]=aux[0]
            #print("dato: ",aux[0])
        st.plotly_chart(fig)
        facultadSelect= st.selectbox('Seleccione la facultad',listAux )
        print(facultadSelect)
        #para mostrar la estadistica de las carrearas de la facultad seleccionada
        dfFacultadSelect= dfE.loc[dfE['facultad'] == facultadSelect]
        dfFacultadGroup= dfFacultadSelect.groupby(by=['carrera'])['carrera'].count()
        dfFacultadSelect= pd.DataFrame(dfFacultadGroup)
        dfFacultadSelect=dfFacultadSelect.rename(columns={'carrera': 'ESTUDIANTES'})
        colCarrera = st.columns((6,10, 12), gap='small')
        with colCarrera[0]:
            st.metric(label="TOTAL-ESTUDIANTES", value=dfFacultadSelect['ESTUDIANTES'].sum() )
        with colCarrera[2]:
            st.dataframe(dfFacultadSelect)
        with colCarrera[1]:
            figCarrera = px.bar(
            dfFacultadSelect,
            y='ESTUDIANTES',
            color='ESTUDIANTES',
            color_continuous_scale=['red', 'yellow', 'green'],
            template='plotly_white',
            title=f'<b>Grafica de estudiantes</b>'
            )
            st.plotly_chart(figCarrera)
        

    else:
        if df_selected_year== 'SEXO':
            dfE_grouped = dfE.groupby(by= ['sexo'])['sexo'].count()
            dataF= pd.DataFrame(dfE_grouped)
            dataF=dataF.rename(columns={'sexo': 'CANTIDAD DE ESTUDIANTES'})
            total = dataF['CANTIDAD DE ESTUDIANTES'].sum()
            with col[0]:
                st.metric(label="TOTAL-ESTUDIANTES", value=total )
            with col[1]:
                st.dataframe(dataF) 
            #st.dataframe(dfE)
            fig = px.bar(
                dataF,
                y='CANTIDAD DE ESTUDIANTES',
                color='CANTIDAD DE ESTUDIANTES',
                color_continuous_scale=['red', 'yellow', 'green'],
                template='plotly_white',
                title=f'<b>Estudiantes  by sexo</b>'
                )
            st.plotly_chart(fig)
            dfE_facult = dfE.groupby(by= ['facultad'])['facultad']
            dataFacult = pd.DataFrame(dfE_facult)
            column1= dataFacult.columns.tolist()
            listAux= dataFacult[column1[0]].tolist()
            for i in range (len(listAux)):
                aux= listAux[i]
                listAux[i]=aux[0]
                #print("dato: ",aux[0])

            facultadSelect= st.selectbox('Seleccione la facultad',listAux )
            print(facultadSelect)
            #para mostrar la estadistica de las carrearas de la facultad seleccionada
            dfFacultadSelect= dfE.loc[dfE['facultad'] == facultadSelect]
            dfFacultadGroup= dfFacultadSelect.groupby(by=['sexo'])['sexo'].count()
            dfFacultadSelect= pd.DataFrame(dfFacultadGroup)
            dfFacultadSelect=dfFacultadSelect.rename(columns={'sexo': 'ESTUDIANTES'})
            colCarrera = st.columns((6,10, 12), gap='small')
            with colCarrera[0]:
                st.metric(label="TOTAL-ESTUDIANTES", value=dfFacultadSelect['ESTUDIANTES'].sum() )
            with colCarrera[2]:
                st.dataframe(dfFacultadSelect)
            with colCarrera[1]:
                figCarrera = px.bar(
                dfFacultadSelect,
                y='ESTUDIANTES',
                color='ESTUDIANTES',
                color_continuous_scale=['red', 'yellow', 'green'],
                template='plotly_white',
                title=f'<b>Grafica de estudiantes</b>'
                )
                st.plotly_chart(figCarrera)
        else:
            dfE_grouped = dfE.groupby(by= ['turno'])['turno'].count()
            dataF= pd.DataFrame(dfE_grouped)
            dataF=dataF.rename(columns={'turno': 'CANTIDAD DE ESTUDIANTES'})
            total = dataF['CANTIDAD DE ESTUDIANTES'].sum()
            with col[0]:
                st.metric(label="TOTAL-ESTUDIANTES", value=total )
            with col[1]:
                st.dataframe(dataF) 
            #st.dataframe(dfE)
            fig = px.bar(
                dataF,
                y='CANTIDAD DE ESTUDIANTES',
                color='CANTIDAD DE ESTUDIANTES',
                color_continuous_scale=['red', 'yellow', 'green'],
                template='plotly_white',
                title=f'<b>Estudiantes  by turno</b>'
            )
            st.plotly_chart(fig)
            dfE_facult = dfE.groupby(by= ['facultad'])['facultad']
            dataFacult = pd.DataFrame(dfE_facult)
            column1= dataFacult.columns.tolist()
            listAux= dataFacult[column1[0]].tolist()
            for i in range (len(listAux)):
                aux= listAux[i]
                listAux[i]=aux[0]
                #print("dato: ",aux[0])

            facultadSelect= st.selectbox('Seleccione la facultad',listAux )
            print(facultadSelect)
            #para mostrar la estadistica de las carrearas de la facultad seleccionada
            dfFacultadSelect= dfE.loc[dfE['facultad'] == facultadSelect]
            dfFacultadGroup= dfFacultadSelect.groupby(by=['turno'])['turno'].count()
            dfFacultadSelect= pd.DataFrame(dfFacultadGroup)
            dfFacultadSelect=dfFacultadSelect.rename(columns={'turno': 'ESTUDIANTES'})
            colCarrera = st.columns((6,10, 12), gap='small')
            with colCarrera[0]:
                st.metric(label="TOTAL-ESTUDIANTES", value=dfFacultadSelect['ESTUDIANTES'].sum() )
            with colCarrera[2]:
                st.dataframe(dfFacultadSelect)
            with colCarrera[1]:
                figCarrera = px.bar(
                dfFacultadSelect,
                y='ESTUDIANTES',
                color='ESTUDIANTES',
                color_continuous_scale=['red', 'yellow', 'green'],
                template='plotly_white',
                title=f'<b>Grafica de estudiantes</b>'
                )
                st.plotly_chart(figCarrera)
