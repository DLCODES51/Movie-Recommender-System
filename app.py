import streamlit as st
import pickle 
import requests

# paste this into app.py (replace DRIVE_FILE_ID)
import os, pickle, time, streamlit as st
DRIVE_FILE_ID = "1-FuqYIh95PWpcHxIySpdbp5sjwQR1B09"
MODEL_FILENAME = "similarity.pkl"
MAX_DOWNLOAD_ATTEMPTS = 2

def _is_probably_html(path):
    try:
        with open(path,"rb") as f:
            s = f.read(512)
        if s.lstrip().lower().startswith(b"<!doctype html") or b"<html" in s.lower():
            return True
        if b"quota" in s.lower() or b"google drive" in s.lower() or b"virus" in s.lower():
            return True
    except Exception:
        return False
    return False

def _download_with_gdown(file_id, out_path):
    import gdown
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, out_path, quiet=False)

def _download_with_requests(file_id, out_path):
    import requests
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(out_path,"wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

@st.cache_resource
def get_similarity():
    if os.path.exists(MODEL_FILENAME):
        try:
            with open(MODEL_FILENAME,"rb") as f:
                return pickle.load(f)
        except Exception:
            try: os.remove(MODEL_FILENAME)
            except: pass
            st.warning("Local copy invalid — re-downloading.")

    for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS+1):
        st.info(f"Downloading model (attempt {attempt})...")
        try:
            try:
                import gdown
                _download_with_gdown(DRIVE_FILE_ID, MODEL_FILENAME)
            except Exception:
                _download_with_requests(DRIVE_FILE_ID, MODEL_FILENAME)

            if _is_probably_html(MODEL_FILENAME):
                os.remove(MODEL_FILENAME)
                st.error("Downloaded file looks like an HTML/Drive error page. Ensure sharing is 'Anyone with the link'.")
                break

            with open(MODEL_FILENAME,"rb") as f:
                sim = pickle.load(f)
            st.success("Model loaded.")
            return sim

        except Exception as exc:
            st.warning(f"Attempt {attempt} failed: {exc}")
            time.sleep(1)
            if os.path.exists(MODEL_FILENAME):
                try: os.remove(MODEL_FILENAME)
                except: pass
            if attempt == MAX_DOWNLOAD_ATTEMPTS:
                st.error("Failed to download/unpickle model. Check Drive sharing, model integrity, or view app logs.")
                raise
    raise RuntimeError("Could not load similarity model.")




# Background image URL
background_url = "https://assets.nflxext.com/ffe/siteui/vlv3/8200f588-2e93-4c95-8eab-ebba17821657/web/IN-en-20250616-TRIFECTA-perspective_9cbc87b2-d9bb-4fa8-9f8f-a4fe8fc72545_large.jpg"

# Load all necessary Netflix Sans weights
st.markdown("""
    <style>
    @font-face {
        font-family: 'Netflix Sans';
        font-weight: 400;
        font-style: normal;
        src: url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Rg.woff2) format('woff2'),
             url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Rg.woff) format('woff');
    }

    @font-face {
        font-family: 'Netflix Sans';
        font-weight: 900;
        font-style: normal;
        src: url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Bd.woff2) format('woff2'),
             url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Bd.woff) format('woff');
    }
    </style>
""", unsafe_allow_html=True)

# Apply global styling and background
st.markdown(f"""
    <style>
              
    .stApp {{
        background: 
        linear-gradient(to top, rgba(0, 0, 0, 0.5) 0%, rgba(0,0,0,0.3) 40%, rgba(0,0,0,0) 100%),
        radial-gradient(circle at center, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0.2) 70%, rgba(0, 0, 0, 0) 100%),
        linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.85) 90%, rgba(0,0,0,1) 100%),
        url("{background_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    html, body, [class*="css"] {{
        font-family: 'Netflix Sans', sans-serif !important;
        color: white !important;
    }}

    .big {{
        font-family: 'Netflix Sans' !important;
        font-weight: 900 !important;
        font-size: 65px !important;
        text-align: center !important;
        
        line-height: 1.2 !important;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.75) !important;
    }}

    .small{{
        font-family: 'Netflix Sans' !important;
        font-weight: 570 !important;
        font-size: 25px !important;
        text-align: center !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style> 
    .custom-label {
        font-family: 'Netflix Sans', sans-serif !important;
        font-size: 17px;
        color: white;
        font-weight: 400;
        text-align: center;
        margin-top: 10px;
    }
            
    div[data-baseweb="select"]> div {
        background-color: rgba(80, 80, 80, 0.5) !important;  /* Transparent black */
        border: 1px solid #e50914;
        border-radius: 8px; 
        height: 50px !important;  /* Increase height */
            margin-top: -15px;
    }
          
    div[data-baseweb="select"] > div > div {
        color: white !important;
        font-size: 20px !important;
        padding-top: 10px;
    }

    div[data-baseweb="select"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Text that uses the custom font and weight
st.markdown('<p class="big">Unlimited movies, TV shows and more</p>', unsafe_allow_html=True)

st.markdown('<p class="small">Your next favorite movie awaits.</p>',unsafe_allow_html=True)

st.markdown('<div class="custom-label">Not sure what to watch next? Select one movie you’ve liked, and we’ll handle the rest.</div>', unsafe_allow_html=True)

#Load the data
movies = pickle.load(open("movies_list.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
movies_list = list(movies["title"].astype(str))

selectvalue = st.selectbox("", movies_list, index=0)

def poster_fetch(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7b80cd813e67b4a06ee8d9f39f87d8fb&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

def recommend(movie):
    index = movies[movies["title"]==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse= True, key= lambda vector:vector[1])  
    recommend_movies = []
    recommend_posters = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(poster_fetch(movie_id))
    return recommend_movies, recommend_posters

if st.button("Recommend"):
    movie_title, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(movie_poster[0], use_container_width=True)
        st.text(movie_title[0])
        
    with col2:
        st.image(movie_poster[1], use_container_width=True)
        st.text(movie_title[1])
        
    with col3:
        st.image(movie_poster[2], use_container_width=True)
        st.text(movie_title[2])
        
    with col4:
        st.image(movie_poster[3], use_container_width=True)
        st.text(movie_title[3])
        
    with col5:
        st.image(movie_poster[4], use_container_width=True)

        st.text(movie_title[4])




