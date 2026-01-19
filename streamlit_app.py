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
"st.markdown"("""
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
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stMetricValue, .stMetricLabel {
        color: #000000 !important;
    }
    
    /* --- DROPDOWN & INPUT FIXES --- */
    div[data-baseweb="select"] div {
        color: white !important;
        background-color: #262730 !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #262730 !important;
    }
    ul[data-baseweb="menu"] li div, 
    ul[data-baseweb="menu"] li span {
        color: white !important;
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
        pointer-events: none;
        z-index: 0;
    }
    .leaf:nth-child(1) { left: 10%; animation-duration: 12s; animation-delay: 0s; }
    .leaf:nth-child(2) { left: 30%; animation-duration: 18s; animation-delay: 2s; font-size: 1.5rem; }
    .leaf:nth-child(3) { left: 70%; animation-duration: 14s; animation-delay: 5s; }
    .leaf:nth-child(4) { left: 90%; animation-duration: 20s; animation-delay: 1s; font-size: 2.5rem; }

    /* --- NEW ACTION ANIMATIONS (TRIGGERED) --- */
    
    /* 1. Fast Falling Dry Leaves (Non-Eco) - DOWNWARD */
    @keyframes fallFast {
        0% { top: -10vh; opacity: 1; transform: rotate(0deg); }
        100% { top: 110vh; opacity: 0; transform: rotate(720deg); }
    }
    
    .dry-leaf-burst {
        position: fixed;
        color: #8D6E63 !important; /* Brown/Sepia */
        animation: fallFast 2s ease-in forwards; /* Slower, smoother fall */
        pointer-events: none;
        z-index: 999999;
    }

    /* 2. Fast Rising Green Leaves (Eco) - UPWARD */
    @keyframes riseFast {
        0% { bottom: -10vh; opacity: 1; transform: rotate(0deg); }
        100% { bottom: 110vh; opacity: 0; transform: rotate(-720deg); }
    }

    .green-leaf-burst {
        position: fixed;
        color: #2e7d32 !important; /* Green */
        animation: riseFast 2s ease-out forwards;
        pointer-events: none;
        z-index: 999999;
    }

    /* --- GLASSMORPHISM CARDS --- */
    div[data-testid="stMetric"], div[class*="stCard"] {
        background: rgba(255, 255, 255, 0.85); 
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    [data-testid="stMetricValue"] { color: #000000 !important; }
    [data-testid="stMetricLabel"] { color: #333333 !important; }

    /* --- BUTTONS --- */
    .stButton > button {
        background: linear-gradient(45deg, #43a047, #66bb6a);
        color: white !important;
        border: none;
        border-radius: 15px;
        padding: 10px 25px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(67, 160, 71, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(67, 160, 71, 0.5);
    }
    
    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255,255,255,0.6);
        border-radius: 15px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-
