import streamlit as st
import pickle
import requests
# from dotenv import load_dotenv
import os

# load_dotenv()
api_key = os.getenv("API_KEY")

movies_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity_matrix.pkl','rb'))
all_movies = movies_list['title'].values

def fetch_poster(id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US")
    data = response.json()
    if data['poster_path']:
        return "http://image.tmdb.org/t/p/w500/"+data['poster_path']
    return "https://www.kingsporttn.gov/wp-content/uploads/Image-Not-Available.jpg"
    
    
def recommend(movie):
  recommended_movie = []
  recommended_movie_poster = []
  index = movies_list[movies_list['title']==movie].index[0]
  movieList = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])[1:6]
  for i in movieList:
      movie_id = movies_list.loc[i[0]].id
      poster_path = fetch_poster(movie_id)
      recommended_movie.append(movies_list.loc[i[0]].title) 
      recommended_movie_poster.append(poster_path)
  return recommended_movie,recommended_movie_poster

st.title('Movie Recommendation System')
movieName = st.selectbox('Enter the movie',all_movies)
if st.button('Recommend'):
    st.write('You might like:')
    recommendations,posters = recommend(movieName)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])

