import streamlit as st
from pymongo import MongoClient
import pandas as pd
def app():
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
    def asignarSemestre(data,plan):
        semestrexMateria=[]
        for i in range(len(data)):
            aux= data.iloc[i]['asignatura']
            aux= aux[:5]
            #print(aux)
            aux2= plan[plan['asignatura']==aux]
            aux3= aux2["anoSemestre"].tolist()
            semestrexMateria.append(aux3[0])
        return(semestrexMateria)
    def eliminarSpacios(dato):
        tokens= dato.split()
        nuevaCadena=""
        for i in range(len(tokens)):
            nuevaCadena= nuevaCadena+tokens[i]
        return(nuevaCadena)
    def agruparEstudiantes(cedula,materias,estado,materiasP,materiasS,materiasT,materiasC,materiasQ):
        year="No tiene"
        contarGrup1=0
        contarGrup2=0
        contarGrup3=0
        contarGrup4=0
        contarGrup5=0
           # print(cedulaEstudiante)
        for j in range(len(materias)):
            sw=0
            cedulas=materias.iloc[j]['cedulas']
            semestre=materias.iloc[j]['semestre']
            for x in range(len(cedulas)):
                cedulaCurso= cedulas[x]
                cedulaCurso= eliminarSpacios(cedulaCurso)
                if cedula==cedulaCurso:
                    sw=1
            if sw==1:
                if semestre.find("PRIMER AÑO")>-1:
                    contarGrup1= contarGrup1+1
                else:
                    if semestre.find("SEGUNDO AÑO")>-1:
                        contarGrup2= contarGrup2+1
                    else:
                        if semestre.find("TERCER AÑO")>-1:
                            contarGrup3= contarGrup3+1
                        else:
                            if semestre.find("CUARTO AÑO")>-1:
                                contarGrup4= contarGrup4+1
                            else:
                                contarGrup5=contarGrup5+1
            #print(i+1,"-",contarGrup1,contarGrup2,contarGrup3,contarGrup4,contarGrup5)
        materiasP.append(contarGrup1)
        materiasS.append(contarGrup2)
        materiasT.append(contarGrup3)
        materiasC.append(contarGrup4)
        materiasQ.append(contarGrup5)
        if(contarGrup1>contarGrup2 and contarGrup1> contarGrup3 and contarGrup1>contarGrup4 and contarGrup1> contarGrup5):
            year="PRIMER AÑO"
            if contarGrup2==0 and contarGrup3==0 and contarGrup4==0 and contarGrup5==0:
                estado[0]="REGULAR"
        if(contarGrup2>contarGrup1 and contarGrup2> contarGrup3 and contarGrup2>contarGrup4 and contarGrup2> contarGrup5):
            year="SEGUNDO AÑO"
            if contarGrup1==0 and contarGrup3==0 and contarGrup4==0 and contarGrup5==0:
                estado[0]="REGULAR"
        if(contarGrup3>contarGrup1 and contarGrup3> contarGrup2 and contarGrup3>contarGrup4 and contarGrup3> contarGrup5):
            year="TERCER AÑO"
            if contarGrup1==0 and contarGrup2==0 and contarGrup4==0 and contarGrup5==0:
                estado[0]="REGULAR"
        if(contarGrup4>contarGrup1 and contarGrup4> contarGrup2 and contarGrup4>contarGrup3 and contarGrup4> contarGrup5):
            year="CUARTO AÑO"
            if contarGrup1==0 and contarGrup2==0 and contarGrup3==0 and contarGrup5==0:
                estado[0]="REGULAR"
        if(contarGrup5>contarGrup1 and contarGrup5> contarGrup2 and contarGrup5>contarGrup3 and contarGrup5> contarGrup4):
            year="QUINTO AÑO"
            if contarGrup1==0 and contarGrup2==0 and contarGrup3==0 and contarGrup4==0:
                estado[0]="REGULAR"
        return year
    estudiantes= read_mongo('cruv', 'estudiantes')
    dfE= read_mongo('cruv', 'datos')
    materiasP=[]
    materiasS=[]
    materiasT=[]
    materiasC=[]
    materiasQ=[]
    mate= read_mongo('cruv', 'materias')
    st.title("BUSQUEDA DE ESTUDIANTE")
    col = st.columns((4.5, 4.5,1.5), gap='medium')
    text=st.text_input("Ingrese su cedula, ejemplo 9-758-46")
    data=text.split("-")
    aux=""
    if text!="":
        for i in range(5-(len(data[2]))):
            aux=aux+"0"
        asiento= aux+data[2]
        if len(data[0])>1:
            cedula=data[0]+"00"+"0"+data[1]+asiento
        else:
            cedula="0"+data[0]+"00"+"0"+data[1]+asiento
        st.write(cedula)
        estudiante=estudiantes.loc[estudiantes['cedula'] == cedula]
        cedula= estudiante['cedula'].values.item()
        carrera= estudiante['carrera'].values.item()
       # carrera=carrera[:2]+carrera[4:len(carrera)]
        #st.write(carrera)
        materias= dfE.loc[dfE['carrera']== carrera]
        mate=mate[mate['carrera']== carrera]
        semestrexMateria=asignarSemestre(materias,mate)
        materias=materias.assign(semestre=semestrexMateria)
        estado=['No Regular']
        year= agruparEstudiantes(cedula,materias,estado,materiasP,materiasS,materiasT,materiasC,materiasQ)
        #st.write(materias)
        st.write(year)
        estudiante=estudiante.assign(año=year)
        estudiante=estudiante.assign(Estado=estado,MateriasPrimerA=materiasP,MateriasSegundoA=materiasS,
                                     MateriasTercerA=materiasT,MateriasCuartoA=materiasC,MateriasQuintoA=materiasQ)
        estudiante=estudiante.drop(['__v', 'cedula', 'ano','escuela'], axis=1)
        st.dataframe(estudiante)
