import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster URL
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=db3c9938a2d67356e00f343588d57d32&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    try:
        # Get the index of the selected movie
        movie_index = movies[movies['title'] == movie].index[0]

        # Validate movie_index
        if movie_index >= len(similarity):
            raise ValueError("Invalid movie index.")

        # Get distances from similarity matrix
        distances = similarity[movie_index]

        # Sort distances and get top 5 similar movies
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []

        # Iterate over recommended movies
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_posters

    except IndexError:
        st.error("Movie not found. Please select a valid movie.")
        return [], []

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [], []

# Load movies data and similarity matrix
movies_dict = pickle.load(open('movies_dictionary.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

try:
    with open('similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)
except (IOError, OSError, pickle.UnpicklingError) as e:
    print(f"Error loading similarity data: {e}")
    similarity = None

# Streamlit app title
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

# Button to trigger movie recommendation
if st.button('Recommend'):
    names, poster_urls = recommend(selected_movie_name)

    # Display recommended movies and posters in a grid layout
    num_columns = 3  # Number of columns for display
    col_width = int(12 / num_columns)  # Column width based on Bootstrap grid system

    # Create a row for displaying movies
    for i in range(0, len(names), num_columns):
        row_data = names[i:i + num_columns]
        row_posters = poster_urls[i:i + num_columns]
        cols = st.columns(num_columns)

        for col, movie_name, poster_url in zip(cols, row_data, row_posters):
            with col:
                st.subheader(movie_name)  # Display movie name as subheader
                st.image(poster_url, width=200)  # Display movie poster with specified width
