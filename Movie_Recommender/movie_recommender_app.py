import streamlit as st
import pickle
import pandas as pd
import os
import requests
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full paths to the pickle files
movie_dict_path = os.path.join(current_dir, 'movie_dict.pkl')
similarity_path = os.path.join(current_dir, 'similarity.pkl')
movie_dict = pickle.load(open(movie_dict_path,'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open(similarity_path,'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=658b01c3f4b98d35352b4104c26e37b0&language=en-US"
    try:
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"
    
def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key= lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies,recommended_posters

st.title('Movie  Recommender System')
selected_movie_name = st.selectbox('Which movie did you like?',movies['title'].values)
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])