import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import random
from pathlib import Path
from typing import Dict, Optional

# ==================== CONFIGURATION & CONSTANTS ====================
st.set_page_config(
    page_title="EcoShop Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colors from the design
COLORS = {
    "primary": "#36e27b",        # The bright green
    "primary_bg": "#eaffe5",     # Light green background for accents
    "background": "#f6f8f7",     # Main app background
    "surface": "#ffffff",        # Card background
    "text_main": "#111714",      # Dark text
    "text_sub": "#648772",       # Muted text
    "border": "#dce5df"          # Border color
}

# Product Data Lists
PRODUCT_TYPES = [
    'Fast Fashion', 'T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater',
    'Smartphone', 'Laptop', 'Tablet', 'Gaming Console', 'Smartwatch',
    'Local Groceries', 'Organic Vegetables', 'Meat', 'Dairy Products', 'Coffee',
    'Furniture', 'Home Decor', 'Bicycle', 'Public Transit Pass', 'Flight Ticket',
    'Books (New)', 'Books (Used)', 'Thrifted Clothing', 'Refurbished Tech',
    'Plant-Based Meat', 'Second-Hand Item'
]

ALL_BRANDS = [
    'Whole Foods', 'Shell', 'Local Market', 'Target', 'Zara', 'H&M', 'Nike', 
    'Apple', 'Samsung', 'IKEA', 'Patagonia', 'The North Face', 'Beyond Meat',
    'Thrift Store', 'Depop', 'Etsy', 'Generic', 'Other'
]

ECO_FRIENDLY_CATEGORIES = [
    'Second-Hand Item', 'Local Groceries', 'Books (Used)', 'Thrifted Clothing',
    'Used Electronics', 'Organic Vegetables', 'Refurbished Tech', 'Bicycle', 
    'Plant-Based Meat', 'Public Transit Pass'
]

BADGES = {
    'first_step': {'name': 'First Step', 'desc': 'Logged first purchase', 'icon': '🌱'},
    'eco_warrior': {'name': 'Eco Warrior', 'desc': 'Maintained < 50kg CO₂', 'icon': '🛡️'},
    'thrift_king': {'name': 'Thrift King', 'desc': 'Bought 3 used items', 'icon': '👑'}
}

DATA_FILE = Path("ecoshop_data.json")

# ==================== DATA LOGIC ====================

def get_default_data() -> Dict:
    return {
        'purchases': [],
        'user_profile': {
            'name': 'Jane Doe',
            'level': 'Eco Warrior Lvl 5',
            'badges': []
        }
    }

def load_data() -> Dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return get_default_data()
    return get_default_data()

def save_data(data: Dict) -> None:
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_product_multiplier(product_type: str) -> float:
    # Simplified logic for demo
    if product_type in ECO_FRIENDLY_CATEGORIES: return 0.1
    if 'Meat' in product_type or 'Flight' in product_type: return 3.5
    if 'Fashion' in product_type or 'Jeans' in product_type: return 2.5
    if 'Electronics' in product_type: return 1.8
    return 1.0

def suggest_eco_option(selected_product: str) -> Optional[str]:
    suggestions = {
        'T-Shirt': "Try **Organic Cotton** or **Thrifted** options.",
        'Meat': "Try **Plant-Based Meat** to save CO₂.",
        'Smartphone': "A **Refurbished Phone** saves ~50kg CO₂.",
        'Fast Fashion': "Consider **Ethical Brands** or **Second-Hand**."
    }
    return suggestions.get(selected_product)

def add_purchase_logic(product_type, brand, price):
    multiplier = get_product_multiplier(product_type)
    co2 = (price * multiplier) / 100
    
    new_item = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'type': product_type,
        'brand': brand,
        'price': float(price),
        'co2_impact': float(co2)
    }
    st.session_state.data['purchases'].append(new_item)
    save_data(st.session_state.data)
    
    # Badge Logic Check (Simplified)
    badges = st.session_state.data['user_profile']['badges']
    if 'first_step' not in badges:
        badges.append('first_step')
        st.toast("🏆 Badge Unlocked: First Step!", icon='🌱')
    
    return True

# Initialize Session State
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# ==================== CSS STYLING (Manrope & UI Overrides) ====================
st.markdown(f"""
<style>
    /* Import Manrope Font */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap');

    /* General App Styling */
    .stApp {{
        background-color: {COLORS['background']};
        font-family: 'Manrope', sans-serif;
        color: {COLORS['text_main']};
    }}
    
    /* Remove top header padding */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['surface']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* Custom Card Styling */
    .custom-card {{
        background-color: {COLORS['surface']};
        padding: 24px;
        border-radius: 16px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        height: 100%;
    }}
    
    /* Metric styling inside cards */
    .metric-label {{
        color: {COLORS['text_sub']};
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .metric-value {{
        color: {COLORS['text_main']};
        font-size: 2rem;
        font-weight: 800;
        margin-top: 8px;
    }}
    
    .metric-delta {{
        font-size: 0.85rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
    }}
    
    .delta-pos {{ background-color: {COLORS['primary_bg']}; color: #2e7d32; }}
    .delta-neg {{ background-color: #fee2e2; color: #ef4444; }}

    /* Custom Button Styling */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: #112117;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }}
    .stButton > button:hover {{
        background-color: #32d673;
        box-shadow: 0 4px 12px rgba(54, 226, 123, 0.3);
        transform: translateY(-1px);
    }}
    
    /* Secondary Button Styling */
    .secondary-btn > button {{
        background-color: transparent;
        border: 1px solid {COLORS['border']};
        color: {COLORS['text_main']};
    }}

    /* Inputs */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{
        background-color: {COLORS['surface']};
        border-radius: 8px;
        border-color: {COLORS['border']};
    }}

    /* Navigation Menu in Sidebar */
    .nav-item {{
        display: flex;
        align-items: center;
        padding: 12px 16px;
        margin-bottom: 4px;
        border-radius: 12px;
        cursor: pointer;
        transition: background-color 0.2s;
        text-decoration: none;
        color: {COLORS['text_sub']};
        font-weight: 500;
    }}
    .nav-item:hover {{
        background-color: {COLORS['background']};
        color: {COLORS['text_main']};
    }}
    .nav-active {{
        background-color: {COLORS['primary_bg']};
        color: #1a4d2e; /* Darker green for text */
        font-weight: 700;
    }}
    
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px; padding: 0 10px;">
            <div style="width: 40px; height: 40px; background: {COLORS['primary']}; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                🌿
            </div>
            <h1 style="margin: 0; font-size: 20px; font-weight: 800; color: {COLORS['text_main']};">EcoShop</h1>
        </div>
    """, unsafe_allow_html=True)

    # Navigation (Using radio to control state, but styled via CSS if needed, standard radio is cleaner for Streamlit)
    nav_selection = st.radio(
        "Navigation", 
        ["Dashboard", "Transactions", "Impact Report", "Settings"], 
        label_visibility="collapsed"
    )
    st.session_state.page = nav_selection

    st.markdown("---")
    
    # User Profile at Bottom
    user = st.session_state.data['user_profile']
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px; margin-top: auto;">
            <div style="width: 40px; height: 40px; background-color: #eee; border-radius: 50%; background-image: url('https://api.dicebear.com/7.x/avataaars/svg?seed={user['name']}'); background-size: cover;"></div>
            <div>
                <div style="font-weight: 700; font-size: 14px; color: {COLORS['text_main']}">{user['name']}</div>
                <div style="font-size: 12px; color: {COLORS['text_sub']}">{user['level']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== MAIN DASHBOARD ====================

if st.session_state.page == "Dashboard":
    
    # --- HEADER ---
    col_head_1, col_head_2 = st.columns([3, 1])
    with col_head_1:
        st.markdown(f"""
            <h1 style="font-weight: 800; font-size: 2.5rem; margin-bottom: 0;">Dashboard</h1>
            <p style="color: {COLORS['text_sub']}; font-weight: 500; margin-top: 5px;">Track your sustainable journey and carbon footprint</p>
        """, unsafe_allow_html=True)
    
    with col_head_2:
        # We use an expander to act as the "New Entry" modal
        with st.expander("➕ New Entry", expanded=False):
            with st.form("new_entry_form"):
                p_type = st.selectbox("Product", PRODUCT_TYPES)
                
                # Dynamic Suggestion
                sugg = suggest_eco_option(p_type)
                if sugg:
                    st.info(sugg)
                    
                p_brand = st.selectbox("Brand", ALL_BRANDS)
                p_price = st.number_input("Price ($)", min_value=0.0, value=20.0, step=5.0)
                
                if st.form_submit_button("Add Transaction"):
                    add_purchase_logic(p_type, p_brand, p_price)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CALCULATE STATS ---
    df = pd.DataFrame(st.session_state.data['purchases'])
    
    total_spent = 0
    total_co2 = 0
    eco_rate = 0
    
    if not df.empty:
        total_spent = df['price'].sum()
        total_co2 = df['co2_impact'].sum()
        eco_count = df[df['type'].isin(ECO_FRIENDLY_CATEGORIES)].shape[0]
        eco_rate = int((eco_count / len(df)) * 100)
    
    # --- METRICS ROW (CUSTOM CARDS) ---
    c1, c2, c3 = st.columns(3)
    
    def render_metric_card(icon, label, value, delta, is_good_delta=True):
        delta_class = "delta-pos" if is_good_delta else "delta-neg"
        delta_icon = "↗" if is_good_delta else "↘"
        return f"""
        <div class="custom-card">
            <div class="metric-label">
                <span style="font-size: 1.2rem;">{icon}</span> {label}
            </div>
            <div style="display: flex; align-items: baseline; gap: 10px;">
                <div class="metric-value">{value}</div>
                <div class="metric-delta {delta_class}">
                    {delta_icon} {delta}
                </div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 5px;">Vs. last month</div>
        </div>
        """

    with c1:
        st.markdown(render_metric_card("💳", "Total Spent", f"${total_spent:,.2f}", "5%", False), unsafe_allow_html=True)
    with c2:
        st.markdown(render_metric_card("☁️", "Total CO2", f"{total_co2:.1f}kg", "12%", False), unsafe_allow_html=True)
    with c3:
        st.markdown(render_metric_card("♻️", "Eco Choices Rate", f"{eco_rate}%", "8%", True), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MAIN SPLIT (ACTIVITY & CHART) ---
    col_activity, col_chart = st.columns([1, 2], gap="large")

    # --- LEFT COLUMN: RECENT ACTIVITY ---
    with col_activity:
        st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;"><h3 style="margin:0; font-weight:700;">Recent Activity</h3><a href="#" style="color:{COLORS["primary"]}; text-decoration:none; font-size:0.9rem;">View All</a></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="custom-card" style="padding: 0; overflow: hidden;">', unsafe_allow_html=True)
        
        if df.empty:
            st.markdown('<div style="padding:20px; text-align:center; color:#888;">No purchases yet.</div>', unsafe_allow_html=True)
        else:
            # Sort by recent
            recent_df = df.iloc[::-1].head(5)
            
            for index, row in recent_df.iterrows():
                is_eco = row['type'] in ECO_FRIENDLY_CATEGORIES
                icon = "nutrition" if "Food" in row['type'] or "Groceries" in row['type'] else "shopping_bag"
                icon_bg = "#eaffe5" if is_eco else "#f3f4f6"
                icon_color = "#2e7d32" if is_eco else "#4b5563"
                dot_color = "#36e27b" if is_eco else "#d1d5db"
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 16px 20px; border-bottom: 1px solid {COLORS['border']};">
                    <div style="width: 48px; height: 48px; border-radius: 12px; background: {icon_bg}; display: flex; align-items: center; justify-content: center; color: {icon_color}; margin-right: 16px;">
                        <span style="font-size: 24px;" class="material-symbols-outlined">{icon}</span>
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 700; color: {COLORS['text_main']}; font-size: 1rem;">{row['brand']}</div>
                        <div style="font-size: 0.75rem; color: {COLORS['text_sub']}; font-weight: 500;">{row['date']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700; color: {COLORS['text_main']}; font-size: 1rem;">-${row['price']:.2f}</div>
                        <div style="width: 8px; height: 8px; background: {dot_color}; border-radius: 50%; display: inline-block; margin-top: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- RIGHT COLUMN: LIVE IMPACT CHART ---
    with col_chart:
        st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;"><h3 style="margin:0; font-weight:700;">Live Impact Overview</h3></div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
            
            if not df.empty:
                # Prepare data for chart
                # Grouping by mock days for visual similarity to design
                chart_data = df.reset_index()
                
                # Create Plotly Chart matching the design style
                fig = go.Figure()

                # 1. Spending Line (Grey Dashed)
                fig.add_trace(go.Scatter(
                    x=chart_data.index, 
                    y=chart_data['price'],
                    mode='lines',
                    name='Spending',
                    line=dict(color='#9ca3af', width=2, dash='dash'),
                    hoverinfo='y'
                ))

                # 2. CO2 Line (Green Filled)
                fig.add_trace(go.Scatter(
                    x=chart_data.index, 
                    y=chart_data['co2_impact'],
                    mode='lines+markers',
                    name='CO2 Impact',
                    line=dict(color=COLORS['primary'], width=3),
                    marker=dict(size=8, color=COLORS['primary'], line=dict(width=2, color='white')),
                    fill='tozeroy', # Fill area below
                    fillcolor='rgba(54, 226, 123, 0.1)' # Transparent green
                ))

                # Layout customization to match design (Minimalist)
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=350,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    xaxis=dict(showgrid=False, showline=False, showticklabels=True, tickfont=dict(color=COLORS['text_sub'])),
                    yaxis=dict(showgrid=True, gridcolor='#f3f4f6', showline=False, zeroline=False, tickfont=dict(color=COLORS['text_sub']))
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Add some data to see the chart!")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ==================== OTHER PAGES (Placeholder) ====================
elif st.session_state.page == "Settings":
    st.title("Settings")
    st.write("Profile configuration goes here.")
    if st.button("Reset Data"):
        save_data(get_default_data())
        st.session_state.data = get_default_data()
        st.rerun()

else:
    st.title(st.session_state.page)
    st.write("Feature coming soon.")
