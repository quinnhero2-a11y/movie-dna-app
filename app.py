import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="Movie DNA & Discovery Engine", layout="wide")
st.title("🎬 Top-Tier Movie AI Engine")
st.caption("Zero-install cloud environment running vector-based recommendation algorithms.")

# --- MOCK DATA ENGINE (Simulating the Movie Genome) ---
# In a full build, this would be replaced by loading a real dataset like MovieLens.
@st.cache_data
def load_movie_database():
    movies = [
        "Inception", "Interstellar", "The Dark Knight", "Pulp Fiction", 
        "The Matrix", "Blade Runner 2049", "Spirited Away", "The Godfather",
        "Gladiator", "Whiplash", "The Grand Budapest Hotel", "Parasite"
    ]
    # Simulate a small 10-feature structural DNA vector for each movie
    np.random.seed(42)
    dna_vectors = np.random.uniform(0.1, 1.0, size=(len(movies), 10))
    
    # Normalize vectors for simple Cosine Similarity simulation
    norms = np.linalg.norm(dna_vectors, axis=1, keepdims=True)
    normalized_dna = dna_vectors / norms
    
    df = pd.DataFrame(normalized_dna, index=movies)
    return df

dna_matrix = load_movie_database()
all_movies = dna_matrix.index.tolist()

# --- APP NAVIGATION ---
tab1, tab2 = st.tabs(["🧬 Movie DNA Sequencer", "🎛️ Interactive Discovery Mode"])

# ==========================================
# TAB 1: MOVIE DNA SEQUENCER
# ==========================================
with tab1:
    st.header("🧬 The DNA Matching Formula")
    st.write("Select up to 3 anchor movies to sequence a blended structural vector target.")
    
    selected_movies = st.multiselect(
        "Choose your core profile anchors:", 
        options=all_movies, 
        max_selections=3,
        key="dna_select"
    )
    
    if st.button("Sequence Profiles", type="primary"):
        if not selected_movies:
            st.warning("Please select at least 1 movie to extract a DNA blueprint.")
        else:
            with st.spinner("Processing structural matrix vectors..."):
                # Extract chosen vectors and calculate the blended mean vector
                chosen_vectors = dna_matrix.loc[selected_movies]
                target_vector = chosen_vectors.mean(axis=0).values
                
                # Filter out the input movies from recommendation pool
                pool = dna_matrix.drop(selected_movies)
                
                # Calculate dot product (cosine similarity since vectors are normalized)
                scores = pool.dot(target_vector)
                results = pd.DataFrame({"Match Match %": scores * 100}).sort_values(by="Match Match %", ascending=False)
                
                st.success("DNA sequence generation complete!")
                
                # Display Results
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric(label="Top Recommendation Match", value=results.index[0])
                with col2:
                    st.dataframe(results.style.format("{:.1f}%"))

# ==========================================
# TAB 2: INTERACTIVE DISCOVERY MODE
# ==========================================
with tab2:
    st.header("🎛️ Active Preference Modeler")
    st.write("Provide feedback on movies to actively shift your session's vector weights.")

    # Initialize cloud-based session tracking states
    if "user_profile_vector" not in st.session_state:
        st.session_state.user_profile_vector = np.zeros(10)
    if "current_movie_idx" not in st.session_state:
        st.session_state.current_movie_idx = 0

    current_movie = all_movies[st.session_state.current_movie_idx]
    movie_vector = dna_matrix.loc[current_movie].values

    st.subheader(f"Do you like: **{current_movie}**?")
    
    # Layout choice configuration
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("❤️ Love It (Heavy Weight Increase)"):
            st.session_state.user_profile_vector += (movie_vector * 1.5)
            st.session_state.current_movie_idx = (st.session_state.current_movie_idx + 1) % len(all_movies)
            st.rerun()
            
    with c2:
        if st.button("👍 Like It (Standard Increase)"):
            st.session_state.user_profile_vector += movie_vector
            st.session_state.current_movie_idx = (st.session_state.current_movie_idx + 1) % len(all_movies)
            st.rerun()
            
    with c3:
        if st.button("👎 Dislike It (Vector Subtraction)"):
            st.session_state.user_profile_vector -= movie_vector
            st.session_state.current_movie_idx = (st.session_state.current_movie_idx + 1) % len(all_movies)
            st.rerun()
            
    with c4:
        if st.button("⏭️ Skip"):
            st.session_state.current_movie_idx = (st.session_state.current_movie_idx + 1) % len(all_movies)
            st.rerun()

    st.divider()
    
    # Dynamic Live Recommendation output
    if np.any(st.session_state.user_profile_vector):
        st.subheader("🔮 Your Real-Time Tailored Recommendations:")
        
        # Calculate matching based on user's active session history
        scores = dna_matrix.dot(st.session_state.user_profile_vector)
        live_results = pd.DataFrame({"Match Score": scores}).sort_values(by="Match Score", ascending=False)
        
        st.dataframe(live_results)
        
        if st.button("Reset Dynamic Profile"):
            st.session_state.user_profile_vector = np.zeros(10)
            st.session_state.current_movie_idx = 0
            st.rerun()