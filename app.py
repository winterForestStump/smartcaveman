import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="smart caveman")

# --- STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #f5f5f5; }
    .text-chunk {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 0px;
        white-space: pre-wrap;
        word-wrap: break-word;
        font-family: 'Times New Roman', serif;
        line-height: 1.6;
        background-color: white;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    h3 { color: #333; border-bottom: 2px solid #ddd; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- HELPERS ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        for col in ['text']:
            if col in df.columns:
                # Handle formatting and escape dollar signs for LaTeX safety
                df[col] = df[col].fillna("").str.replace('\n\n', '\n', regex=False).str.replace('\n', '', regex=False)
        for col in ['temp_1.0']:
            if col in df.columns:
                # Handle formatting and escape dollar signs for LaTeX safety
                df[col] = df[col].fillna("").str.replace('\n\n', '\n', regex=False)
        
        return df
    except Exception as e:
        st.error(f"CSV Error: {e}")
        return None

def count_words(text_series):
    """Count words in a pandas series of strings"""
    # Split by whitespace and count the number of elements
    return text_series.str.split().str.len().sum()


# Define available CSV files
csv_files = {
    "Buffett 1977 letter": {
        "path": "results/caveman_1977_baffet_letter_ver2.csv",
        "source_link": "https://www.berkshirehathaway.com/letters/1977.html",
        "source_text": "view original 1977 letter on Berkshire Hathaway website"
    },
    "SAP CEO 2025 letter": {
        "path": "results/SAP_caveman.csv",  # CHANGE THIS TO YOUR ACTUAL FILE PATH
        "source_link": "https://www.lobbyregister.bundestag.de/media/2c/d5/710485/SAP-Integrated-Report-2025.pdf",  # UPDATE WITH CORRECT LINK
        "source_text": "view original CEO letter on 2025 SAP Integrated Report (pages 5-6)"
    }
}


# Add file selector
selected_file = st.sidebar.selectbox(
    "choose a letter to read:",
    options=list(csv_files.keys())
)

# Load the selected file
file_info = csv_files[selected_file]
df = load_data(file_info["path"])

# Display statistics in sidebar under the selector
st.sidebar.markdown("---")
st.sidebar.markdown("### statistics")
if df is not None:
    # Calculate WORD counts instead of character counts
    text_words = count_words(df['text'])
    cave_words = count_words(df['temp_1.0'])
    saving = (text_words - cave_words) / text_words if text_words > 0 else 0
    
    st.sidebar.metric("original words", f"{text_words:,}")
    st.sidebar.metric("caveman words", f"{cave_words:,}")
    st.sidebar.metric("reduction", f"{saving:.1%}")

# --- MAIN CONTENT ---
st.markdown(f"### {selected_file} by smart caveman")
st.markdown(
    f'<div class="source-link"><a href="{file_info["source_link"]}" target="_blank">{file_info["source_text"]}</a></div>',
    unsafe_allow_html=True)

if df is not None:
    colors = ["#FFE5E5", "#E5FFE5", "#E5E5FF", "#FFE5FF", "#E5FFFF", "#FFFFE5", "#FFE5CC", "#CCFFE5"]
    
    col_header_left, col_header_right = st.columns(2)
    with col_header_left: st.markdown("**original letter**")
    with col_header_right: st.markdown("**smart caveman version**")

    for idx, row in df.iterrows():
        c = colors[idx % len(colors)]
        l, r = st.columns(2, gap="medium")
        l.markdown(f'<div class="text-chunk" style="background-color:{c}">{row["text"]}</div>', unsafe_allow_html=True)
        r.markdown(f'<div class="text-chunk" style="background-color:{c}">{row["temp_1.0"]}</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown('''
---
<div style="font-size: 0.9em; color: #666;">
This application is created solely for educational purposes.<br>
</div>
''', unsafe_allow_html=True)