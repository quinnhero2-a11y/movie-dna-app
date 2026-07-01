import streamlit as st
import pandas as pd
import numpy as np
import requests

# --- LAUNCH APP CONFIG ---
st.set_page_config(page_title="Cinematic DNA Lab", layout="wide", initial_sidebar_state="expanded")

# --- TMDB CONFIG ---
TMDB_API_KEY = "82ffb3235498c86f4e0a70fdbd02bcd7" 

# --- INITIALIZE TRACKING MEMORY ---
if "my_library" not in st.session_state: st.session_state.my_library = []
if "liked_genres" not in st.session_state: st.session_state.liked_genres = []
if "dna_results" not in st.session_state: st.session_state.dna_results = []

def fetch_movie_details(query, search_type="search"):
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
    if path: return f"https://image.tmdb.org/t/p/w342{path}"
    return "https://via.placeholder.com/342x513?text=No+Poster"

# --- CLEAN CARD TITLES ADJUSTMENT ---
st.markdown("""
    <style>
    .clean-title {
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        margin-top: 5px;
        min-height: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# --- MAIN APP TITLE ---
st.title("🧬 Cinematic DNA & Discovery Lab")
st.subheader("Next-generation multi-vector film matching engine")

# --- SIDEBAR: USER VAULT ---
with st.sidebar:
    st.header("📂 My Vault")
    st.write("Saved movies actively training your custom match settings:")
    
    if not st.session_state.my_library:
        st.info("Your vault is currently empty. Click 'Add 💾' on any movie card to save it here!")
    else:
        for idx, lib_movie in enumerate(st.session_state.my_library):
            col_l1, col_l2 = st.columns([1, 2])
            with col_l1:
                st.image(get_poster_url(lib_movie.get('poster_path')), use_container_width=True)
            with col_l2:
                st.write(f"**{lib_movie['title']}**")
                if st.button("🗑️ Clear", key=f"rm_{lib_movie['id']}_{idx}", use_container_width=True):
                    st.session_state.my_library.pop(idx)
                    st.rerun()
            st.divider()

# --- APP NAVIGATION TABS ---
tab1, tab2 = st.tabs(["🧬 Multi-Movie DNA Sequencer", "🎛️ Infinite Discovery Mode"])

# ==========================================
# TAB 1: MOVIE DNA SEQUENCER
# ==========================================
with tab1:
    st.write("Supply up to 3 different movies to combine their unique traits into a targeted recommendation blueprint.")
    
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: m1 = st.text_input("First Anchor Film:", placeholder="e.g., Inception", key="dna_m1")
    with col_i2: m2 = st.text_input("Second Anchor Film:", placeholder="e.g., Interstellar", key="dna_m2")
    with col_i3: m3 = st.text_input("Third Anchor Film:", placeholder="e.g., The Matrix", key="dna_m3")
    
    if st.button("🧬 Compute Combined Blueprint", type="primary", use_container_width=True):
        inputs = [m for m in [m1, m2, m3] if m.strip()]
        if not inputs:
            st.warning("Please type a movie title above to extract a profile blueprint.")
        else:
            with st.spinner("Decoding narrative structures and genres..."):
                found_ids = []
                for title in inputs:
                    search_res = fetch_movie_details(title, "search")
                    if search_res: found_ids.append(search_res[0]['id'])
                
                combined_recs = []
                for m_id in found_ids:
                    combined_recs.extend(fetch_movie_details(m_id, "recommendations"))
                
                seen = set(found_ids)
                unique_recs = []
                for r in combined_recs:
                    if r['id'] not in seen:
                        seen.add(r['id'])
                        unique_recs.append(r)
                st.session_state.dna_results = unique_recs

    if st.session_state.dna_results:
        st.write(f"### Found Profiles Match Loop ({len(st.session_state.dna_results)} Results)")
        
        # Fixed scrollable clean gallery view
        with st.container(height=600, border=True):
            cols_per_row = 5
            for i in range(0, len(st.session_state.dna_results), cols_per_row):
                row_movies = st.session_state.dna_results[i : i + cols_per_row]
                grid_cols = st.columns(cols_per_row)
                
                for idx, movie in enumerate(row_movies):
                    with grid_cols[idx]:
                        st.image(get_poster_url(movie.get('poster_path')), use_container_width=True)
                        st.markdown(f"<div class='clean-title'>{movie['title']}</div>", unsafe_allow_html=True)
                        
                        is_saved = any(item['id'] == movie['id'] for item in st.session_state.my_library)
                        if is_saved:
                            st.button("Saved ✓", key=f"dna_sv_{movie['id']}", disabled=True, use_container_width=True)
                        else:
                            if st.button("Add 💾", key=f"dna_add_{movie['id']}", use_container_width=True):
                                st.session_state.my_library.append(movie)
                                st.session_state.liked_genres.extend(movie.get('genre_ids', []))
                                st.rerun()

# ==========================================
# TAB 2: INFINITE DISCOVERY MODE
# ==========================================
with tab2:
    st.write("Rate movies as they appear to dynamically change and refine your real-time session updates.")

    if "api_page" not in st.session_state: st.session_state.api_page = 1
    if "pool" not in st.session_state: st.session_state.pool = fetch_movie_details(st.session_state.api_page, "popular")
    if "current_item_idx" not in st.session_state: st.session_state.current_item_idx = 0

    if st.session_state.current_item_idx >= len(st.session_state.pool):
        st.session_state.api_page += 1
        st.session_state.pool = fetch_movie_details(st.session_state.api_page, "popular")
        st.session_state.current_item_idx = 0

    if st.session_state.pool:
        active_movie = st.session_state.pool[st.session_state.current_item_idx]
        
        col_view1, col_view2 = st.columns([1, 2])
        
        with col_view1:
            st.image(get_poster_url(active_movie.get('poster_path')), use_container_width=True)
        with col_view2:
            st.title(active_movie['title'])
            st.write(f"**Global Rating:** ⭐ {active_movie.get('vote_average', 'N/A')} | **Release:** {active_movie.get('release_date', 'Unknown')}")
            st.write(active_movie.get('overview', 'No summary summary profile uploaded.'))
            
            st.divider()
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("❤️ Love & Save", use_container_width=True, key="disc_love"):
                    if not any(item['id'] == active_movie['id'] for item in st.session_state.my_library):
                        st.session_state.my_library.append(active_movie)
                    st.session_state.liked_genres.extend(active_movie.get('genre_ids', []))
                    st.session_state.current_item_idx += 1
                    st.rerun()
            with c2:
                if st.button("👍 Like", use_container_width=True, key="disc_like"):
                    st.session_state.liked_genres.extend(active_movie.get('genre_ids', []))
                    st.session_state.current_item_idx += 1
                    st.rerun()
            with c3:
                if st.button("👎 Dislike", use_container_width=True, key="disc_dis"):
                    st.session_state.current_item_idx += 1
                    st.rerun()
            with c4:
                if st.button("Skip ⏭️", use_container_width=True, key="disc_skp"):
                    st.session_state.current_item_idx += 1
                    st.rerun()