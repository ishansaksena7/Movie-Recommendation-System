import pickle
import streamlit as st
import requests
import pandas as pd
import ast


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    try:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    except TypeError:
        full_path = 'https://www.themoviedb.org/t/p/original/yTqzXgzgms0qdb2sgc63BUCKvhO.jpg'

    return full_path

def fetch_plot(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    overview = data['overview']
    return overview

def fetch_genre(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    genre = ''

    for i in range(0, len(data['genres'])):
        if genre == '':
            genre = data['genres'][i]['name']
        else:
            genre = genre + ", " + data['genres'][i]['name']
    
    return genre

def fetch_cast(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    cast = ''

    for i in range(0, 3):
        if cast == '':
            cast = data['cast'][i]['name']
        else:
            cast = cast + ", " + data['cast'][i]['name']
    
    return cast

def fetch_director(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    directors = [] 
    director_str = ''

    for credit in data['crew']:  
        if credit["job"] == "Director":  
            directors.append(credit['name'])
    

    for i in range(0, len(directors)):
        director_str = directors[i] 

    return director_str
    
    

def fetch_popularity(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    popularity = data['popularity']
    if popularity > 50:
        return 5
    if popularity > 20 and popularity < 50:
        return 4
    if popularity > 10 and popularity < 20:
        return 3
    if popularity > 4 and popularity < 10:
        return 2
    if popularity > 0 and popularity < 4:
        return 1


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_plot = []
    recommended_movie_posters = []
    recommended_movie_popularity = []
    recommended_movie_genre = []
    recommended_movie_cast = []
    recommended_movie_crew = []
    wrongrecommendflag = False


    for i in distances[1:5]:
        # fetch the movie poster
        list1 = (movies.iloc[i[0]].genres)
        list2 = (movies['genres'].loc[movies[movies['title'] == movie].index[0]])
        
        check =  any(item in list1 for item in list2)
        if check is True:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_plot.append(fetch_plot(movie_id))
            recommended_movie_popularity.append(fetch_popularity(movie_id))
            recommended_movie_genre.append(fetch_genre(movie_id))
            recommended_movie_cast.append(fetch_cast(movie_id))
            recommended_movie_crew.append(fetch_director(movie_id))
        else:
            wrongrecommendflag = True
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_plot.append(fetch_plot(movie_id))
            recommended_movie_popularity.append(fetch_popularity(movie_id))
            recommended_movie_genre.append(fetch_genre(movie_id))
            recommended_movie_cast.append(fetch_cast(movie_id))
            recommended_movie_crew.append(fetch_director(movie_id))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_popularity, recommended_movie_plot, recommended_movie_genre, recommended_movie_cast, recommended_movie_crew, wrongrecommendflag


st.title('Movie Recommender System')
movies = pd.read_pickle(open('movie_listnew.pkl', 'rb'))
similarity = pd.read_pickle(open('TFIDFsimilaritynew.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    
    recommended_movie_names, recommended_movie_posters, recommended_movie_popularity, recommended_movie_plot, recommended_movie_genre, recommended_movie_cast, recommended_movie_crew, wrongrecommendflag = recommend(selected_movie)
    for i in range(0, 1):
        if(wrongrecommendflag == True):
            st.error('Sorry, I could not find enough movies of this Theme. Some of these may be a bit different!')
            

    col1, col2 = st.beta_columns(2)
    with col1:
        if recommended_movie_popularity[0] >= 3:
            st.success( 'Popularity Score: ' + str(recommended_movie_popularity[0]))
        if recommended_movie_popularity[0] < 3:
            st.warning( 'Popularity Score: ' + str(recommended_movie_popularity[0]))

        
        
        st.image(recommended_movie_posters[0])
        my_plot = st.beta_expander('Plotline')
        with my_plot:
            st.markdown('<p>' + recommended_movie_plot[0] +'</p>', unsafe_allow_html=True)
        my_expander = st.beta_expander('More Information')
        with my_expander:
            st.write('Directed By: ' + recommended_movie_crew[0])
            st.write('Cast: ' + recommended_movie_cast[0])
        st.info(recommended_movie_genre[0])
            
        
    with col2:
        if recommended_movie_popularity[1] >= 3:
            st.success( 'Popularity Score: ' + str(recommended_movie_popularity[1]))
        if recommended_movie_popularity[1] < 3:
            st.warning( 'Popularity Score: ' + str(recommended_movie_popularity[1]))

        
        
        st.image(recommended_movie_posters[1])
        my_plot = st.beta_expander('Plotline')
        with my_plot:
            st.markdown('<p>' + recommended_movie_plot[1] +'</p>', unsafe_allow_html=True)
        my_expander = st.beta_expander('More Information')
        with my_expander:
            st.write('Directed By: ' + recommended_movie_crew[1])
            st.write('Cast: ' + recommended_movie_cast[1])
        st.info(recommended_movie_genre[1])

    st.markdown('<p> ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------    </p>', unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)
    with col1:
        if recommended_movie_popularity[2] >= 3:
            st.success( 'Popularity Score: ' + str(recommended_movie_popularity[2]))
        if recommended_movie_popularity[2] < 3:
            st.warning( 'Popularity Score: ' + str(recommended_movie_popularity[2]))

        
        
        st.image(recommended_movie_posters[2])
        my_plot = st.beta_expander('Plotline')
        with my_plot:
            st.markdown('<p>' + recommended_movie_plot[2] +'</p>', unsafe_allow_html=True)
        my_expander = st.beta_expander('More Information')
        with my_expander:
            st.write('Directed By: ' + recommended_movie_crew[2])
            st.write('Cast: ' + recommended_movie_cast[2])
        st.info(recommended_movie_genre[2])
        

    with col2:
        if recommended_movie_popularity[3] >= 3:
            st.success( 'Popularity Score: ' + str(recommended_movie_popularity[3]))
        if recommended_movie_popularity[3] < 3:
            st.warning( 'Popularity Score: ' + str(recommended_movie_popularity[3]))

        
        
        st.image(recommended_movie_posters[3])
        my_plot = st.beta_expander('Plotline')
        with my_plot:
            st.markdown('<p>' + recommended_movie_plot[3] +'</p>', unsafe_allow_html=True)
        my_expander = st.beta_expander('More Information')
        with my_expander:
            st.write('Directed By: ' + recommended_movie_crew[3])
            st.write('Cast: ' + recommended_movie_cast[3])
        st.info(recommended_movie_genre[3])
        


   
