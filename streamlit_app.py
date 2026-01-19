"""
ShopImpact - Ultimate Streamlit Edition
Fully Optimized, Gamified, and Beautifully Animated.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import time
from pathlib import Path
from typing import Dict, List, Optional

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED CSS & ANIMATIONS ====================
st.markdown("""
<style>
    /* --- GLOBAL THEME --- */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background: linear-gradient(120deg, #e0f2f1 0%, #f1f8e9 50%, #fffde7 100%);
        background-attachment: fixed;
    }

    /* --- TEXT VISIBILITY FORCE BLACK (General Content) --- */
    /* We exclude specific UI elements like popovers/menus from this rule */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stMetricValue, .stMetricLabel {
        color: #000000 !important;
    }
    
    /* --- DROPDOWN & INPUT FIXES --- */
    /* Force text inside the selected box (collapsed dropdown) to be BLACK for visibility on light bg */
    div[data-baseweb="select"] div {
        color: #000000 !important;
    }

    /* Force text inside the OPEN dropdown menu options to be WHITE */
    /* This overrides the global black rule for the floating menu */
    ul[data-baseweb="menu"] li span,
    ul[data-baseweb="menu"] li div,
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] span {
        color: #FFFFFF !important;
    }

    /* Ensure the dropdown menu background is dark so white text pops */
    ul[data-baseweb="menu"], div[data-baseweb="popover"] {
        background-color: #262730 !important;
    }
    
    /* --- INPUT LABELS --- */
    .stSelectbox label, .stNumberInput label, .stSlider label, .stTextInput label {
        color: #000000 !important;
        font-weight: 800;
        font-size: 1.1rem !important;
    }

    /* --- BACKGROUND AMBIENT ANIMATION --- */
    @keyframes dropAndDry {
        0% { transform: translateY(-10vh) rotate(0deg) translateX(0px); opacity: 0; filter: hue-rotate(0deg); }
        10% { opacity: 1; }
        50% { filter: hue-rotate(0deg); } /* Green */
        80% { filter: hue-rotate(90deg) sepia(1); } /* Dried/Brown */
        100% { transform: translateY(110vh) rotate(720deg) translateX(50px); opacity: 0; filter: hue-rotate(90deg) sepia(1); }
    }

    .leaf {
        position: fixed;
        top: 0;
        left: 50%;
        font-size: 2rem;
        animation: dropAndDry 15s infinite linear;
        pointer-events:
