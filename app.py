import streamlit as st
import pandas as pd
import numpy as np
import requests

# --- LAUNCH APP CONFIG ---
st.set_page_config(page_title="Cinematic DNA Lab", layout="wide", initial_sidebar_state="collapsed")

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

# --- POSITIONED CUSTOM LAYOUT STYLING ---
st.markdown("""
    <style>
    .img-container {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    .rating-badge {
        position: absolute;
        bottom: 8px;
        right: 8px;
        background-color: rgba(0, 0, 0, 0.75);
        color: #f59e0b;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .clean-title {
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        margin-top: 6px;
        min-height: 42px;
        line-height: 1.3;
    }
    </style>
""", unsafe_allow_html=True)

# --- MAIN APP TITLE ---
st.title("🧬 Cinematic DNA Lab")
st.markdown("<p style='color:gray; margin-top:-15px;'>Top-tier multi-vector algorithmic recommendation system</p>", unsafe_allow_html=True)
st.divider()

# --- APP NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["🧬 Multi-Movie DNA Sequencer", "🎛️ Infinite Discovery Mode", "📂 My Vault"])

# ==========================================
# TAB 1: MOVIE DNA SEQUENCER (Natural Scroll)
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
        st.write(f"### Found Profiles ({len(st.session_state.dna_results)} Results)")
        
        # Site scrolls naturally down with the elements
        cols_per_row = 5
        for i in range(0, len(st.session_state.dna_results), cols_per_row):
            row_movies = st.session_state.dna_results[i : i + cols_per_row]
            grid_cols = st.columns(cols_per_row)
            
            for idx, movie in enumerate(row_movies):
                with grid_cols[idx]:
                    # Embedded poster containing structural overlay badge metrics
                    rating = movie.get('vote_average', 0)
                    rating_str = f"{rating:.1f}" if rating > 0 else "N/A"
                    
                    st.markdown(f"""
                        <div class='img-container'>
                            <img src='{get_poster_url(movie.get('poster_path'))}' style='width:100%; border-radius:8px;'>
                            <div class='rating-badge'>⭐ {rating_str}</div>
                        </div>
                        <div class='clean-title'>{movie['title']}</div>
                    """, unsafe_allow_html=True)
                    
                    is_saved = any(item['id'] == movie['id'] for item in st.session_state.my_library)
                    if is_saved:
                        st.button("Saved ✓", key=f"dna_sv_{movie['id']}_{i}", disabled=True, use_container_width=True)
                    else:
                        if st.button("Save 💾", key=f"dna_add_{movie['id']}_{i}", use_container_width=True):
                            st.session_state.my_library.append(movie)
                            st.rerun()

# ==========================================
# TAB 2: INFINITE DISCOVERY MODE (Separated Actions)
# ==========================================
with tab2:
    st.write("Rate movies to train algorithm weights, or simply save items you want to watch later.")

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
            rating = active_movie.get('vote_average', 0)
            rating_str = f"{rating:.1f}" if rating > 0 else "N/A"
            st.markdown(f"""
                <div class='img-container' style='max-width:300px;'>
                    <img src='{get_poster_url(active_movie.get('poster_path'))}' style='width:100%; border-radius:12px;'>
                    <div class='rating-badge' style='font-size:14px; padding:4px 8px;'>⭐ {rating_str}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_view2:
            st.title(active_movie['title'])
            st.write(f"**Release Date:** {active_movie.get('release_date', 'Unknown')}")
            st.write(active_movie.get('overview', 'No description profile distributed.'))
            
            st.divider()
            
            # Top Layer: Recommendation Training Signals
            st.write("**Algorithmic Feedback (Moves to next movie):**")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("❤️ Love", use_container_width=True, key="disc_love"):
                    st.session_state.liked_genres.extend(active_movie.get('genre_ids', []))
                    st.session_state.current_item_idx += 1
                    st.rerun()
            with c2:
                if st.button("👎 Dislike", use_container_width=True, key="disc_dis"):
                    st.session_state.current_item_idx += 1
                    st.rerun()
            with c3:
                if st.button("Skip ⏭️", use_container_width=True, key="disc_skp"):
                    st.session_state.current_item_idx += 1
                    st.rerun()
            
            st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
            
            # Bottom Layer: Independent Utility Actions
            st.write("**Collection Actions:**")
            is_active_saved = any(item['id'] == active_movie['id'] for item in st.session_state.my_library)
            if is_active_saved:
                st.button("Saved in Vault ✓", key="disc_sv_disabled", disabled=True)
            else:
                if st.button("💾 Save to Library (Watch Later)", key="disc_save_clean"):
                    st.session_state.my_library.append(active_movie)
                    st.toast(f"Added {active_movie['title']} to your Vault!")
                    st.rerun()

# ==========================================
# TAB 3: DEDICATED VAULT LIBRARY
# ==========================================
with tab3:
    st.header("📂 My Collection Vault")
    st.write("Your personal catalogued storage logs.")
    
    if not st.session_state.my_library:
        st.info("Your vault is currently empty. Use the tabs above to find and store movies!")
    else:
        # Render lists cleanly with original structural widths
        for idx, lib_movie in enumerate(st.session_state.my_library):
            col_v1, col_v2 = st.columns([1, 4])
            with col_v1:
                rating = lib_movie.get('vote_average', 0)
                rating_str = f"{rating:.1f}" if rating > 0 else "N/A"
                st.markdown(f"""
                    <div class='img-container'>
                        <img src='{get_poster_url(lib_movie.get('poster_path'))}' style='width:100%; border-radius:8px;'>
                        <div class='rating-badge'>⭐ {rating_str}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_v2:
                st.subheader(lib_movie['title'])
                st.write(f"**Released:** {lib_movie.get('release_date', 'Unknown')}")
                st.write(lib_movie.get('overview', 'No summary summary profile uploaded.'))
                if st.button("🗑️ Remove from Vault", key=f"vault_rm_{lib_movie['id']}_{idx}"):
                    st.session_state.my_library.pop(idx)
                    st.rerun()
            st.divider()