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

# ==========================================
# 🔥 ULTRA PREMIUM HTML/CSS DESIGN INJECTION
# ==========================================
st.markdown("""
    <style>
    /* Global background overrides and clean font systems */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d0f12 !important;
        color: #e2e8f0;
    }
    
    /* Modern Header */
    .main-title {
        font-size: 42px; font-weight: 700;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    /* Premium Movie Cards UI */
    .movie-card {
        background: rgba(22, 28, 36, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-align: center;
        margin-bottom: 15px;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        border-color: #00f2fe;
        box-shadow: 0 8px 24px rgba(0, 242, 254, 0.15);
    }
    .movie-title-text {
        font-size: 14px; font-weight: 600; color: #f8fafc;
        margin: 8px 0; height: 36px; overflow: hidden;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
    }
    
    /* Action Buttons Restyling */
    div.stButton > button {
        background: linear-gradient(135deg, #1e293b, #0f172a) !important;
        color: #38bdf8 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #00f2fe, #4facfe) !important;
        color: #0f172a !important;
        border-color: #00f2fe !important;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.4);
    }
    
    /* Interactive Swiper Box Styling */
    .discovery-container {
        background: #111827; border: 1px solid #1f2937;
        border-radius: 16px; padding: 24px; margin-top: 15px;
    }
    
    /* Scroll Window Layout */
    div[data-testid="stElementContainer"] div[style*="overflow-y: auto"] {
        background: #090d11 !important; border-radius: 12px; padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- APPARATUS HEADER ---
st.markdown("<div class='main-title'>🧬 CINEMATIC DNA LAB</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;'>Next-gen hyper-targeted algorithmic vector matching sandbox.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR: HIGH FIDELITY VAULT ---
with st.sidebar:
    st.markdown("### 📂 SYSTEM COLLECTION")
    st.caption("Active data nodes modifying algorithm loops dynamically.")
    st.markdown("---")
    if not st.session_state.my_library:
        st.info("No records stored in local memory bank yet.")
    else:
        for idx, lib_movie in enumerate(st.session_state.my_library):
            col_l1, col_l2 = st.columns([1, 3])
            with col_l1:
                st.image(get_poster_url(lib_movie.get('poster_path')), use_container_width=True)
            with col_l2:
                st.markdown(f"<span style='font-size:13px; font-weight:600;'>{lib_movie['title']}</span>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"rm_{lib_movie['id']}_{idx}"):
                    st.session_state.my_library.pop(idx)
                    st.rerun()
            st.markdown("<div style='margin:-5px 0;'></div>", unsafe_allow_html=True)

# --- WORKSPACE MODULES ---
tab1, tab2 = st.tabs(["🧬 Multi-Movie DNA Sequencer", "🎛️ Infinite Discovery Mode"])

# ==========================================
# TAB 1: MOVIE DNA SEQUENCER
# ==========================================
with tab1:
    st.markdown("### 🧬 Multi-Vector Genetic Blending Engine")
    
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: m1 = st.text_input("Profile Anchor Alpha:", placeholder="e.g., Inception", key="dna_m1")
    with col_i2: m2 = st.text_input("Profile Anchor Beta:", placeholder="e.g., Interstellar", key="dna_m2")
    with col_i3: m3 = st.text_input("Profile Anchor Gamma:", placeholder="e.g., The Matrix", key="dna_m3")
    
    if st.button("🧬 COMPUTE DNA MATCHES", type="primary", use_container_width=True):
        inputs = [m for m in [m1, m2, m3] if m.strip()]
        if not inputs:
            st.warning("Input operational keys to balance vector parameters.")
        else:
            with st.spinner("Analyzing multi-variant spatial similarities..."):
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
        st.markdown(f"#### 🔮 Match Vectors Found ({len(st.session_state.dna_results)})")
        
        with st.container(height=550, border=True):
            cols_per_row = 5
            for i in range(0, len(st.session_state.dna_results), cols_per_row):
                row_movies = st.session_state.dna_results[i : i + cols_per_row]
                grid_cols = st.columns(cols_per_row)
                
                for idx, movie in enumerate(row_movies):
                    with grid_cols[idx]:
                        # Wrap item in HTML Card Structure
                        st.markdown(f"""
                            <div class='movie-card'>
                                <img src='{get_poster_url(movie.get('poster_path'))}' style='width:100%; border-radius:8px;'>
                                <div class='movie-title-text'>{movie['title']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
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
    st.markdown("### 🎛️ Vector Profile Adaptive Modeler")

    if "api_page" not in st.session_state: st.session_state.api_page = 1
    if "pool" not in st.session_state: st.session_state.pool = fetch_movie_details(st.session_state.api_page, "popular")
    if "current_item_idx" not in st.session_state: st.session_state.current_item_idx = 0

    if st.session_state.current_item_idx >= len(st.session_state.pool):
        st.session_state.api_page += 1
        st.session_state.pool = fetch_movie_details(st.session_state.api_page, "popular")
        st.session_state.current_item_idx = 0

    if st.session_state.pool:
        active_movie = st.session_state.pool[st.session_state.current_item_idx]
        
        st.markdown("<div class='discovery-container'>", unsafe_allow_html=True)
        col_view1, col_view2 = st.columns([1, 2])
        
        with col_view1:
            st.image(get_poster_url(active_movie.get('poster_path')), use_container_width=True)
        with col_view2:
            st.markdown(f"<h2 style='margin-top:0; color:#00f2fe;'>{active_movie['title']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#cbd5e1; font-size:15px; line-height:1.6;'>{active_movie.get('overview', 'Missing log data.')}</p>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#64748b;'>Rating: ⭐ {active_movie.get('vote_average', 'N/A')} | Airdate: {active_movie.get('release_date', 'Unknown')}</span>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("❤️ Love", use_container_width=True, key="disc_love"):
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
        st.markdown("</div>", unsafe_allow_html=True)