#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import streamlit as st
from linkpreview import link_preview
from PIL import Image
import urllib.request

st.write("""
# J'ai pas d'idée de titre.
""")

@st.cache(show_spinner=False)
def imports():
    movies=pd.read_csv(r"C:/Users/Dumont/Desktop/20 Wilde code school/project movies/movies2.csv")
    distances=pd.read_csv(r"C:/Users/Dumont/Desktop/20 Wilde code school/project movies/distances.csv")
    genome_score=pd.read_csv(r"C:/Users/Dumont/Desktop/20 Wilde code school/project movies/genome-scores.csv")
    MB=movies[movies.tags==True].reset_index(drop=True)
    links=pd.read_csv(r"C:/Users/Dumont/Desktop/20 Wilde code school/project movies/image.csv")
    return (movies,distances,genome_score,MB,links)

movies,distances,genome_score,MB,links=imports()

def userinput():
    out=st.text_input("Entrez un nom de film")
    return out.lower()

entry1=userinput()

@st.cache(show_spinner=False)
def pos(entry):
    possibilities=movies[movies.title2.str.contains(entry)].reset_index(drop=True)
    return possibilities

possibilities=pos(entry1)
if len(possibilities)==0:
    st.write("Désolé, pas de film avec ce nom.")    
else:      
    if len(possibilities)==1:
        target=possibilities.title[0]    
    else:
        choice=st.selectbox(label="Cherchez vous un de ces films?",options=possibilities.title)

        if st.button('Valider'):
            target=choice
    try:
        target_index=movies.loc[movies.title==target].index[0]  
        if movies.loc[target_index,"tags"]:
            st.write("Recommandations par mot-clés")
            IdFilmChosen=movies.loc[target_index,"movieId"]
            top_20_tags_id = genome_score[genome_score['movieId'] == IdFilmChosen].sort_values('relevance', ascending = False).iloc[0:20,1]

            most_relevant_movies = genome_score[genome_score['tagId'].isin(list(top_20_tags_id))].groupby(
                'movieId', as_index = False).mean().drop('tagId', axis = 1)
            df2=MB.loc[most_relevant_movies.sort_values('relevance', ascending = False).head(6).index.values,["title","movieId"]]    
            st.write(df2.title)
            

        st.write("Recommandations par genres")
        df1=movies.loc[np.array(distances.loc[target_index]).reshape(10,),["title","movieId"]].head(6)
        st.write(df1.title)

        df = pd.concat([df1,df2],axis=0).drop_duplicates()
        image=links.loc[links.movieId.isin(df.movieId),"final_link"]
        liste=[]
        for i in image:
            pic=Image.open(urllib.request.urlopen(link_preview(i).absolute_image))
            liste.append(pic)
        
        st.image(liste,width=120)    
    except:
        pass