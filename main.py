import streamlit as st
from streamlit_option_menu import option_menu

import Estadistica, Busqueda, Estudiantes
st.set_page_config(
        page_title="ESTADISTICA-UP",
)
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='ESTADISTICAUP',
                options=['Estadistica','Busqueda','Estudiantes'],
                icons=['clipboard2-data','person-circle','display'],
                menu_icon='book',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        
        if app == "Estadistica":
            Estadistica.app()
        if app == "Busqueda":
            Busqueda.app()  
        if app == "Estudiantes":
            Estudiantes.app()
  
             
          
             
    run()            