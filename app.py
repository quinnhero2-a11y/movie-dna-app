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
# 🔥 PREMIUM HTML/CSS CINEMATIC GLOW THEME
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Base Reset and Cinematic Backgrounds */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif;
        background-color: #090b0e !important;
        color: #e2e8f0 !important;
    }
    
    /* Neon Linear Heading */
    .main-title {
        font-size: 38px; font-weight: 800; letter-spacing: -0.5px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Premium Grid Movie Cards */
    .movie-card {
        background: rgba(20, 26, 35, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 10px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .movie-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 242, 254, 0.5);
        box-shadow: 0 8px 24px rgba(0, 242, 254, 0.15);
    }
    .movie-title-text {
        font-size: 13px; font-weight: 600; color: #f1f5f9;
        margin: 8px 0 4px 0; height: 36px; overflow: hidden;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
    }
    
    /* Custom Sidebar Aesthetics */
    [data-testid="stSidebar"] {
        background-color: #0f1319 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.03);
    }
    .sidebar-item {
        background: rgba(255, 255, 255, 0.02);
        padding: 8px; border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        margin-bottom: 8px;
    }
    
    /* Premium Action Buttons Style Overrides */
    div.stButton > button {
        background: linear-gradient(135deg, #161e29, #0f151d) !important;
        color: #38bdf8 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #00f2fe, #4facfe) !important;
        color: #090b0e !important;
        border-color: #00f2fe !important;
        box-shadow: 0 0 14px rgba(0, 242, 254, 0.35);
    }
    
    /* Native Scroll Containers Styling Mod */
    div[data-testid="stElementContainer"] div[style*="overflow-y: auto"] {
        background: #0d1015 !important; 
        border: 1px solid rgba(255,255,255,0.03) !important;
        border-radius: 12px; padding: 16px;
    }
    
    /* Discovery Deck Container */
    .discovery-container {
        background: linear-gradient(145deg, #111622, #0d111a);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 16px; padding: 24px; margin-top: 10px;
        box-shadow: 0 12px 36px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- APPARATUS HEADER ---
st.markdown("<div class='main-title'>🧬 CINEMATIC DNA LAB</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:14px; margin-top: -5px;'>Next-generation multi-vector film matching engine.</p>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# --- SIDEBAR: HIGH FIDELITY VAULT ---
with st.sidebar:
    st.markdown("<h3 style='color: #38bdf8; font-size:18px; margin-bottom:15px;'>📂 MY VAULT</h3>", unsafe_allow_html=True)
    st.caption("Saved properties dynamically mapping algorithmic bias loops.")
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    if not st.session_state.my_library:
        st.info("System storage bank unallocated. Add records below.")
    else:
        for idx, lib_movie in enumerate(st.session_state.my_library):
            st.markdown("<div class='sidebar-item'>", unsafe_allow_html=True)
            col_l1, col_l2 = st.columns([1, 3])
            with col_l1:
                st.image(get_poster_url(lib_movie.get('poster_path')), use_container_width=True)
            with col_l2:
                st.markdown(f"<div style='font-size:12px; font-weight:600; line-height:1.2; color:#f1f5f9; margin-bottom:6px;'>{lib_movie['title']}</div>", unsafe_allow_html=True)
                if st.button("🗑️ Clear", key=f"rm_{lib_movie['id']}_{idx}", use_container_width=True):
                    st.session_state.my_library.pop(idx)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- DESIGN WORKSPACE TABS ---
tab1, tab2 = st.tabs(["🧬 Multi-Movie DNA Sequencer", "🎛️ Infinite Discovery Mode"])

# ==========================================
# TAB 1: MOVIE DNA SEQUENCER
# ==========================================
with tab1:
    st.markdown("<p style='color:#94a3b8; font-size:14px;'>Supply up to 3 distinct structural anchors to synthesize a blended structural recommendation output.</p>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: m1 = st.text_input("DNA Variant Alpha:", placeholder="e.g., Inception", key="dna_m1")
    with col_i2: m2 = st.text_input("DNA Variant Beta:", placeholder="e.g., Interstellar", key="dna_m2")
    with col_i3: m3 = st.text_input("DNA Variant Gamma:", placeholder="e.g., The Matrix", key="dna_m3")
    
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🧬 SYNTHESIZE COMBINED BLUEPRINT", type="primary", use_container_width=True):
        inputs = [m for m in [m1, m2, m3] if m.strip()]
        if not inputs:
            st.warning("Input titles to map dimensional target similarities.")
        else:
            with st.spinner("Decoding parallel narrative strings..."):
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
        st.markdown(f"<p style='color:#00f2fe; font-size:14px; font-weight:600; margin-top:20px;'>Generated Vectors Found: {len(st.session_state.dna_results)} Structural Variants</p>", unsafe_allow_html=True)
        
        with st.container(height=580, border=True):
            cols_per_row = 5
            for i in range(0, len(st.session_state.dna_results), cols_per_row):
                row_movies = st.session_state.dna_results[i : i + cols_per_row]
                grid_cols = st.columns(cols_per_row)
                
                for idx, movie in enumerate(row_movies):
                    with grid_cols[idx]:
                        st.markdown(f"""
                            <div class='movie-card'>
                                <img src='{get_poster_url(movie.get('poster_path'))}' style='width:100%; border-radius:8px;'>
                                <div class='movie-title-text'>{movie['title']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
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
    st.markdown("<p style='color:#94a3b8; font-size:14px;'>Train real-time feedback mechanisms continuously. Machine cycles update after each interaction execution.</p>", unsafe_allow_html=True)

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
            st.image(get_poster_url(active_movie.get('poster_