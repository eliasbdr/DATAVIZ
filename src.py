import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def lecture(uploaded_file, delimiter, decimal_separator):#fonction lecture fichier pour main
    try:
        df = pd.read_csv(uploaded_file, sep=delimiter, decimal=decimal_separator) # lecture fichier + stockage dans une BDD pandas
        return df 
    except Exception as e:
        st.error(f"Error reading file {uploaded_file.name}: {e}")
        return None
    

def graphe(dataframes, colors):
    fig = go.Figure() #initialisation figure subplot

    for i, (df, color) in enumerate(zip(dataframes, colors)):#parcours dans l'itérable formé de tuple (pos, (dataframes,couleur))
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns #identification des colonnes chiffrées, avec une selection de type


        x_column = df.columns[0] if len(df.columns) > 1 else None #création de la colonne des x en prenant la première colonne, lorsque 

        for col in numeric_columns[1:]:  #boucle for de la 1ere à la n-eme colonne
            x_data = df[x_column].tolist() if x_column else list(range(len(df))) # on prend la colonne des x pour abcisse si la première colonne est composée d'entiers
            #tracé d'une courbe pour chacune des colonnes
            fig.add_trace(go.Scatter(x=x_data, y=df[col],mode='lines+markers',name=f"File {i+1} - {col}",line=dict(color=color)))

    # Update layout for better interactivity
    fig.update_layout(title='Imported Files Chart',height=600,width=1000,hovermode='x unified',legend_title_text='Series',xaxis_title='X',yaxis_title='Y',template='plotly_white' )

    # Add zoom and pan tools
    fig.update_xaxes(rangeslider_visible=True,type='linear')
    return fig
