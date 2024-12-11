import streamlit as st
import pandas as pd
import plotly.express as px  
from pymongo import MongoClient
def app():
    st.title("ESTUDIANTES POR CARRERA-AÑO")
    semestre="PRIMER SEMESTRE"
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
    semestrexMateria=[]
    def asignarSemestre(data,plan):
        for i in range(len(data)):
            aux= data.iloc[i]['asignatura']
            print(aux)
            aux= aux[:5]
            print(aux)
            aux2= plan[plan['asignatura']==aux]
            aux3= aux2["anoSemestre"].tolist()
            print(aux3)
            semestrexMateria.append(aux3[0])
        #print("datos::::",semestrexMateria)
        return(semestrexMateria)
    def agruparEstudiantes(estudiantes,materias,nombres1,nombres2,nombres3,nombres4,nombres5,nombresSin):
        primer=0
        segundo=0
        tercero=0
        cuarto=0
        quinto=0
        sinMatricula=0
        #print(len(estudiantes))
        for i in range(len(estudiantes)):
            contarGrup1=0
            contarGrup2=0
            contarGrup3=0
            contarGrup4=0
            contarGrup5=0
            cedulaEstudiante= estudiantes.iloc[i]['cedula']
            nombre=estudiantes.iloc[i]['nombre']
           # print(cedulaEstudiante)
            for j in range(len(materias)):
                sw=0
                cedulas=materias.iloc[j]['cedulas']
                semestre=materias.iloc[j]['semestre']
                for x in range(len(cedulas)):
                    cedulaCurso= cedulas[x]
                    cedulaCurso= eliminarSpacios(cedulaCurso)
                    if (cedulaEstudiante==cedulaCurso):
                        sw=1
                if (sw==1):
                    if (semestre.find("PRIMER AÑO")>-1):
                        contarGrup1= contarGrup1+1
                    else:
                        if(semestre.find("SEGUNDO AÑO")>-1):
                            contarGrup2= contarGrup2+1
                        else:
                            if(semestre.find("TERCER AÑO")>-1):
                                contarGrup3= contarGrup3+1
                            else:
                                if(semestre.find("CUARTO AÑO")>-1):
                                    contarGrup4= contarGrup4+1
                                else:
                                    contarGrup5=contarGrup5+1
            #print(i+1,"-",contarGrup1,contarGrup2,contarGrup3,contarGrup4,contarGrup5)
            if(contarGrup1>contarGrup2 and contarGrup1> contarGrup3 and contarGrup1>contarGrup4 and contarGrup1> contarGrup5):
                primer= primer+1 
                nombres1.append(str(primer)+"-"+nombre)

            else:
                if(contarGrup2>contarGrup1 and contarGrup2> contarGrup3 and contarGrup2>contarGrup4 and contarGrup2> contarGrup5):
                    segundo=segundo+1
                    nombres2.append(str(segundo)+"-"+nombre)
                else:
                    if(contarGrup3>contarGrup1 and contarGrup3> contarGrup2 and contarGrup3>contarGrup4 and contarGrup3> contarGrup5):
                        tercero= tercero+1
                        nombres3.append(str(tercero)+"-"+nombre)
                    else:
                        if(contarGrup4>contarGrup1 and contarGrup4> contarGrup2 and contarGrup4>contarGrup3 and contarGrup4> contarGrup5):
                            cuarto=cuarto+1
                            nombres4.append(str(cuarto)+"-"+nombre)
                        else:
                            if(contarGrup5>contarGrup1 and contarGrup5> contarGrup2 and contarGrup5>contarGrup3 and contarGrup5> contarGrup4):
                                quinto=quinto+1
                                nombres5.append(str(quinto)+"-"+nombre)
                            else:
                                sinMatricula=sinMatricula+1
                                nombresSin.append(nombre)
        contador=[primer,segundo,tercero,cuarto,quinto,sinMatricula]
        return(contador)
    def eliminarSpacios(dato):

        tokens= dato.split()
        nuevaCadena=""
        for i in range(len(tokens)):
            nuevaCadena= nuevaCadena+tokens[i]
        return(nuevaCadena)
    dfE= read_mongo('cruv', 'datos')
    mate= read_mongo('cruv', 'materias')#materias de las carreras
    estudiantes= read_mongo('cruv', 'estudiantes')
    #st.dataframe(dfE)
    dfE_facult = dfE.groupby(by= ['facultad'])['facultad']
    dataFacult = pd.DataFrame(dfE_facult)
    #dataFacult = dataFacult.loc[['01-ADMINISTRACION PÚBLICA','05-DERECHO Y CIENCIAS POLITICAS','09-ODONTOLOGIA.']]
    column1= dataFacult.columns.tolist()
    #print(column1)
    listAux= dataFacult[column1[0]].tolist()
    facultades=[]
    for i in range (len(listAux)):
        aux= listAux[i]
        #listAux[i]=aux[0]
        if(aux[0]== '01-ADMINISTRACION PÚBLICA' or aux[0]=='05-DERECHO Y CIENCIAS POLITICAS' or aux[0]=='09-ODONTOLOGIA.' ):
            facultades.append(aux[0])
            #print("dato: ",aux[0])
        #st.plotly_chart(fig)
    facultadSelect= st.selectbox('Seleccione la facultad',facultades )
    dfFacultadSelect=  dfE[dfE['facultad']== facultadSelect]
    carreraGroup= dfFacultadSelect.groupby(by= ['carrera'])
    dfCarreras = pd.DataFrame(carreraGroup)
    column2= dfCarreras.columns.tolist()
    #print (column2)
    #print(dfCarreras)
    listAux2= dfCarreras[column2[0]].tolist()
    for i in range (len(listAux2)):
        aux2= listAux2[i]
        listAux2[i]=aux2[0]
    #print(listAux2)
    carreraSelect= st.selectbox('Seleccione la carrera',listAux2 )
    dfCarreraSelect=dfE[dfE['carrera']== carreraSelect]
    #st.write(dfCarreraSelect)
    #st.dataframe(dfCarreraSelect)
    #st.dataframe(estudiantes)
    mate=mate[mate['carrera']== carreraSelect]
    print("carrera:",carreraSelect," facultad: ", facultadSelect)
    estudiantes= estudiantes[estudiantes['carrera']==carreraSelect]
    semestrexMateria= asignarSemestre(dfCarreraSelect,mate)
    dfCarreraSelect=dfCarreraSelect.assign(semestre=semestrexMateria)
    #st.dataframe(dfCarreraSelect)
    #st.dataframe(estudiantes)
    nombre1=[]
    nombre2=[]
    nombre3=[]
    nombre4=[]
    nombre5=[]
    nombreSin=[]
    contador=agruparEstudiantes(estudiantes,dfCarreraSelect,nombre1,nombre2,nombre3,nombre4,nombre5,nombreSin)
    anos={
        'Año': ["Primer año","Segundo año","Tercer año","Cuarto año", "Quinto año","Sin matricula"],
        'Cantidad de estudiantes':contador,
        'Nombres':[nombre1,nombre2,nombre3,nombre4,nombre5,nombreSin]
    }
    #st.write(nombreSin)
    grupo= pd.DataFrame(data=anos)
    col = st.columns((0.5, 2), gap='small')
    with col[0]:
        st.metric(label="TOTAL-ESTUDIANTES", value=grupo['Cantidad de estudiantes'].sum() )
    with col[1]:
        st.dataframe(grupo)
    figCarrera = px.bar(
        grupo,
        y='Año',
        x='Cantidad de estudiantes',
        color='Cantidad de estudiantes',
        orientation='h',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Grafica de estudiantes</b>'
    )
    st.plotly_chart(figCarrera)
    #print("contadores del 1 a 5 ano",contador)
    #st.dataframe(mate)
