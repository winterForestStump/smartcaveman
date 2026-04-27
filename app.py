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

def show_stats(df):
    if df is not None:
        st.sidebar.title("Stats")
        text_len = df['text'].str.len().sum()
        cave_len = df['temp_1.0'].str.len().sum()
        saving = (text_len - cave_len) / text_len if text_len > 0 else 0
        
        st.sidebar.metric("original words", f"{text_len:,}")
        st.sidebar.metric("caveman words", f"{cave_len:,}")
        st.sidebar.metric("reduction", f"{saving:.1%}")

# --- MAIN CONTENT: 1977 LETTER ONLY ---
st.markdown("### Warren Buffett 1977 Shareholder Letter. by smart caveman")

# Load data directly
df = load_data("results/caveman_1977_baffet_letter_ver2.csv")
show_stats(df)

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


st.markdown('''
        This application is created solely for educational purposes.<br>
        The text in the left column ("Original letter text") from Chairman's Letters for Berkshire Hathaway Inc. shareholders, authored by Warren E. Buffett. 
        Official Source: [Berkshire Hathaway Inc. Website](https://www.berkshirehathaway.com/letters/letters.html)''')