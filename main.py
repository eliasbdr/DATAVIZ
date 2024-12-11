import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graphlect import lecture, graphe

#changement dans la branche elias

def main(): #fonction principale du programme
    st.title("Multi-File Interactive Chart Reader")
    uploaded_files = st.file_uploader("Import Files", type=['csv', 'txt', 'data'], accept_multiple_files=True) #module streamlit importation fichier


    # Création du fichier paramètrage propre à streamlit
    if 'file_configs' not in st.session_state:
        st.session_state.file_configs = {}

    if uploaded_files:
        cols = st.columns(len(uploaded_files)) #colonne = emplacement des commandes d'un seul fichier
        dataframes = [] #liste des df : 1 df = 1fichier
        colors = [] #liste des couleurs

        for i, (col, uploaded_file) in enumerate(zip(cols, uploaded_files)):#enumerate nous permet de récupérer l'indice du fichier dans la liste uploaded_files
            with col:
                st.subheader(f"File {i+1}") #nom de la section avec nom du fichier

                #selection paramètres avec choix utilisateur    

                # Selection Délimiteur
                delimiter = st.selectbox("Delimiter", [',', ';', '.', '\t'], key=f'delimiter_{uploaded_file.name}')
                # Selection separateur
                decimal_separator = st.selectbox("Decimal Separator", [',', '.'], key=f'decimal_{uploaded_file.name}')
                # Color selection
                color = st.color_picker("Choose Color", key=f'color_{uploaded_file.name}')
                
                # Lecture avec fonction lecture
                df = lecture(uploaded_file, delimiter, decimal_separator)

                if df is not None:
                    dataframes.append(df)
                    colors.append(color)
                    
                    # Affichage d'une partie du fichier concaténé avec les dataframes streamlit
                    st.dataframe(df.head())

        # Generation graphique
        if st.button("Generate Chart"):#attente d'activation du bouton
            if dataframes:#liste dataframe non-vide
                fig = graphe(dataframes, colors) # objet plotly créée avec la fonction graphe 
                st.plotly_chart(fig, use_container_width=True) #affichage du graphique plotly avec streamlit
            else:
                st.warning("No valid files imported")



if __name__ == "__main__":
    main()


