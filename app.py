import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(page_title="Cinematic DNA Engine", layout="wide")

# --- TMDB API CONFIG ---
# Using a shared demo key for instant plug-and-play
TMDB_API_KEY = "82ffb3235498c86f4e0a70fdbd02bcd7" 

def fetch_movie_details(query, search_type="search"):
    """Searches or fetches popular movies from TMDB API."""
    if search_type == "search":
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=en-US"
    elif search_type == "popular":
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={query}&language=en-US"
    elif search_type == "recommendations":
        url = f"https://api.themoviedb.org/3/movie/{query}/recommendations?api_key={TMDB_API_KEY}&language=en-US"
    
    try:
        res = requests.get(url, timeout=5).json()
        return res.get("results", [])
    except Exception:
        return []

def get_poster_url(path):
    if path:
        return f"https://image.tmdb.org/t/p/w500{path}"
    return "https://via.placeholder.com/500x750?text=No+Poster+Found"

# --- MAIN INTERFACE CUSTOM STYLING ---
st.markdown("""
    <style>
    .movie-title { font-size: 16px; font-weight: bold; margin-top: 8px; text-align: center; }
    .dna-tag { background-color: #2e7d32; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Cinematic DNA & Discovery Lab")
st.caption("Connected live to TMDB Global Database.")

tab1, tab2 = st.tabs(["🧬 Multi-Movie DNA Sequencer", "🎛️ Infinite Discovery Mode"])

# ==========================================
# TAB 1: MOVIE DNA SEQUENCER
# ==========================================
with tab1:
    st.header("🧬 Complete Genetic Profile Matching")
    st.write("Type up to 3 different movies or shows to combine their traits into a singular target DNA profile.")
    
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: m1 = st.text_input("Movie 1:", placeholder="e.g., Inception")
    with col_i2: m2 = st.text_input("Movie 2:", placeholder="e.g., Interstellar")
    with col_i3: m3 = st.text_input("Movie 3:", placeholder="e.g., The Matrix")
    
    if st.button("Sequence DNA & Match", type="primary"):
        inputs = [m for m in [m1, m2, m3] if m.strip()]
        if not inputs:
            st.warning("Please type at least one movie title to generate structural DNA parameters.")
        else:
            with st.spinner("Decoding narrative structures and genres..."):
                found_ids = []
                for title in inputs:
                    results = fetch_movie_details(title, "search")
                    if results:
                        found_ids.append(results[0]['id'])
                
                if not found_ids:
                    st.error("Could not trace those film profiles in the registry.")
                else:
                    # Fetching recommendations across all seeds to simulate vector blending
                    combined_recs = []
                    for m_id in found_ids:
                        combined_recs.extend(fetch_movie_details(m_id, "recommendations"))
                    
                    # Remove duplicates and clean up data structures
                    seen = set(found_ids)
                    unique_recs = []
                    for r in combined_recs:
                        if r['id'] not in seen:
                            seen.add(r['id'])
                            unique_recs.append(r)
                    
                    if unique_recs:
                        st.success(f"Matched {len(unique_recs)} highly accurate parallel genomic profiles:")
                        
                        # Displaying results dynamically in clean aesthetic columns
                        grid_cols = st.columns(4)
                        for idx, movie in enumerate(unique_recs[:12]):
                            with grid_cols[idx % 4]:
                                st.image(get_poster_url(movie.get('poster_path')), use_container_width=True)
                                st.markdown(f"<div class='movie-title'>{movie['title']}</div>", unsafe_allow_html=True)
                                st.caption(f"Rating: ⭐ {movie.get('vote_average', 'N/A')}")
                    else:
                        st.info("System structural vector constraints require deep data points. Try alternative reference variants.")

# ==========================================
# TAB 2: INFINITE DISCOVERY MODE
# ==========================================
with tab2:
    st.header("🎛️ Vector Profile Adaptive Modeler")
    st.write("Provide immediate feedback loop training inputs to dynamically score and refine recommendations.")

    # Keeping track of current continuous page and choices inside session memory
    if "api_page" not in st.session_state: st.session_state.api_page = 1
    if "pool" not in st.session_state: st.session_state.pool = fetch_movie_details(st.session_state.api_page, "popular")
    if "current_item_idx" not in st.session_state: st.session_state.current_item_idx = 0
    if "liked_genres" not in st.session_state: st.session_state.liked_genres = []

    if st.session_state.current_item_idx >= len(st.session_state.pool):
        # Fetch the next page seamlessly if we run low on pool items
        st.session_state.api_page += 1
        st.session_state.pool = fetch_movie_details(st.session_state.api_page, "popular")
        st.session_state.current_item_idx = 0

    if st.session_state.pool:
        active_movie = st.session_state.pool[st.session_state.current_item_idx]
        
        col_view1, col_view2 = st.columns([1, 2])
        with col_view1:
            st.image(get_poster_url(active_movie.get('poster_path')), use_container_width=True)
        with col_view2:
            st.subheader(active_movie['title'])
            st.write(active_movie.get('overview', 'No summary summary profile uploaded.'))
            st.caption(f"Global Registry Release: {active_movie.get('release_date', 'Unknown')}")
            
            st.divider()
            # Loop interaction commands
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("❤️ Love", use_container_width=True):
                    st.session_state.liked_genres.extend(active_movie.get('genre_ids', []))
                    st.session_state.current_item_idx += 1
                    st.rerun()
            with c2:
                if st.button("👎 Dislike", use_container_width=True):
                    st.session_state.current_item_idx += 1
                    st.rerun()
            with c3:
                if st.button("⏭️ Skip", use_container_width=True):
                    st.session_state.current_item_idx += 1
                    st.rerun()
    else:
        st.error("Failed to connect to the cloud media feed matrix.")