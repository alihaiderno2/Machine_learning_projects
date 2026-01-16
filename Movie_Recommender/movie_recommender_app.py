import streamlit as st
import pickle
import pandas as pd
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full paths to the pickle files
movie_dict_path = os.path.join(current_dir, 'movie_dict.pkl')
similarity_path = os.path.join(current_dir, 'similarity.pkl')
movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key= lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

st.title('Movie  Recommender System')
selected_movie_name = st.selectbox('Which movie did you like?',movies['title'].values)
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.write("You should watch:")
    for i in recommendations:
        st.write(i)