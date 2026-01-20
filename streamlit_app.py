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

    /* --- TEXT VISIBILITY FIXES --- */
    /* Force main text to black, but be specific to avoid breaking components */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #000000 !important;
    }
    
    /* --- DROPDOWN & INPUT FIXES (CRITICAL UPDATE) --- */
    
    /* 1. The Container for the Selected Item (The box you click) */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-color: rgba(0,0,0,0.2) !important;
        color: #000000 !important;
    }
    
    /* 2. The Text of the Selected Item */
    div[data-baseweb="select"] span {
        color: #000000 !important; 
    }

    /* 3. The Dropdown Menu (The list that pops up) */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #ccc !important;
    }

    /* 4. The Options inside the Menu */
    ul[data-baseweb="menu"] li {
        background-color: #ffffff !important;
    }
    
    /* 5. Text inside the options */
    ul[data-baseweb="menu"] li span {
        color: #000000 !important;
    }

    /* 6. Hover/Selected State in Menu */
    ul[data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #e8f5e9 !important; /* Light Green highlight */
    }

    /* Fix labels for inputs */
    .stSelectbox label, .stNumberInput label, .stSlider label, .stTextInput label {
        color: #000000 !important;
        font-weight: 800;
        font-size: 1rem;
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
    
    /* 1. Fast Falling Dry Leaves (Non-Eco) */
    @keyframes fallFast {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }
    
    .dry-leaf-burst {
        position: fixed;
        top: -10vh;
        font-size: 2.5rem;
        color: #8D6E63 !important; /* Brown/Sepia color */
        animation: fallFast 1s linear forwards;
        pointer-events: none;
        z-index: 9999;
    }

    /* 2. Fast Rising Green Leaves (Eco) */
    @keyframes riseFast {
        0% { transform: translateY(110vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-10vh) rotate(-360deg); opacity: 0; }
    }

    .green-leaf-burst {
        position: fixed;
        bottom: -10vh;
        font-size: 2.5rem;
        color: #2e7d32 !important; /* Green color */
        animation: riseFast 1s linear forwards;
        pointer-events: none;
        z-index: 9999;
    }

    /* --- GLASSMORPHISM CARDS --- */
    div[data-testid="stMetric"], div[class*="stCard"] {
        background: rgba(255, 255, 255, 0.85); 
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
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
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px;
        color: #000000;
        font-weight: 800;
    }
    .stTabs [aria-selected="true"] {
        background-color: #fff;
        color: #2e7d32 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Eco Suggestion Box */
    .eco-suggestion {
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        margin-bottom: 10px;
        color: #1b5e20 !important;
    }
</style>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
""", unsafe_allow_html=True)

# ==================== CONSTANTS ====================
PRODUCT_TYPES = [
    # --- Fashion & Apparel ---
    'Fast Fashion', 'T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater', 'Hoodie', 'Shorts', 'Skirt',
    'Blazer', 'Coat', 'Pants', 'Leggings', 'Activewear', 'Swimwear', 'Underwear', 'Socks', 'Shoes', 'Sneakers',
    'Cotton Shirt', 'Linen Shirt', 'Bamboo Fabric Clothing', 'Hemp Clothing', 'Recycled Polyester Gear',
    'Upcycled Jacket', 'Vegan Leather Jacket', 'Organic Cotton T-Shirt', 'Rental Dress', 'Rental Tuxedo',
    'Handloom Saree', 'Khadi Kurta', 'Ethical Wool Sweater', 'Silk Scarf (Ahimsa Silk)',
    
    # --- Electronics & Tech ---
    'Electronics', 'Smartphone', 'Laptop', 'Tablet', 'Desktop Computer', 'Monitor', 'Keyboard', 'Mouse',
    'Headphones', 'Gaming Console', 'Smartwatch', 'Camera', 'TV', 'Speaker', 'Drone',
    'Refurbished Smartphone', 'Refurbished Laptop', 'Second-Hand Tablet', 'Used Camera Lens', 'Used Gaming Console',
    'E-Reader', 'Solar Charger', 'Rechargeable Batteries', 'Smart Thermostat', 'LED Smart Bulb',
    'Energy Efficient AC', 'Repair Service (Phone)', 'Repair Service (Laptop)',

    # --- Food & Groceries ---
    'Local Groceries', 'Organic Vegetables', 'Organic Fruits', 'Meat', 'Dairy Products', 'Snacks',
    'Restaurant Meal', 'Fast Food', 'Coffee', 'Dessert',
    'Plant-Based Meat', 'Oat Milk', 'Almond Milk', 'Soy Milk', 'Loose Leaf Tea', 'Fair Trade Coffee',
    'Bulk Grains (No Plastic)', 'Ugly Produce (Imperfect Veg)', 'Locally Sourced Honey', 'Home-Grown Herbs',
    'Compostable Coffee Pods', 'Tap Water (Filtered)', 'Bottled Water',

    # --- Home & Living ---
    'Home Decor', 'Sofa', 'Chair', 'Table', 'Bed', 'Mattress', 'Kitchenware', 'Appliance',
    'Vintage Furniture', 'Bamboo Furniture', 'Reclaimed Wood Table', 'Cast Iron Skillet (Lifetime)',
    'Glass Food Containers', 'Beeswax Wraps', 'Silicone Stasher Bags', 'Compostable Plates',
    'Biodegradable Trash Bags', 'Loofah Sponge', 'Bamboo Toothbrush', 'Safety Razor', 'Menstrual Cup',
    'Solid Shampoo Bar', 'Refillable Soap', 'Solar Garden Lights', 'Rainwater Harvesting Kit',

    # --- Transport & Travel ---
    'Car Parts', 'Tires', 'Car Accessories',
    'Bicycle', 'E-Bike', 'Electric Scooter', 'Public Transit Pass', 'Train Ticket', 'Flight Ticket',
    'EV Charging Session', 'Carpool Contribution', 'Walking Shoes',

    # --- Books, Media & Hobbies ---
    'Books (New)', 'Books (Used)', 'E-book', 'Vinyl Record', 'Video Game',
    'Library Membership', 'Digital Magazine Subscription', 'Audiobook', 'Digital Game Download',
    'Yoga Mat (Cork)', 'Gym Equipment', 'Sports Gear', 'Camping Gear', 'Used Sports Gear',
    'Musical Instrument (Used)', 'Art Supplies (Non-Toxic)',

    # --- Specialized & Eco ---
    'Leather Goods', 'Vegan Leather',
    'Second-Hand Item', 'Thrifted Clothing', 'Used Electronics', 'Refurbished Tech',
    'Office Supplies', 'Stationery', 'Recycled Paper Notebook', 'Refillable Pen',
    'Gift Card', 'Subscription', 'Event Ticket', 'Digital Download', 'Carbon Offset Credit', 'Tree Planting Donation',
    '500+ (Other)'
]

ALL_BRANDS = [
    # Global Giants
    'Zara', 'H&M', 'Nike', 'Adidas', 'Uniqlo', 'Gucci', 'Louis Vuitton', 'Patagonia', 'The North Face', 'Levi\'s',
    'Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Asus', 'Microsoft', 'Google', 'Canon',
    'IKEA', 'West Elm', 'Pottery Barn', 'Ashley Furniture', 'Wayfair',
    'Sephora', 'L\'Oreal', 'Estee Lauder', 'Mac', 'Fenty Beauty', 'The Body Shop', 'Lush',
    'Amazon', 'Barnes & Noble', 'Penguin Random House', 'Nintendo', 'PlayStation', 'Xbox',
    'Toyota', 'Honda', 'Ford', 'Tesla', 'BMW', 'Tata Motors', 'Mahindra', 'Hyundai',
    
    # Fast Fashion & High Street
    'SHEIN', 'Forever 21', 'Primark', 'Mango', 'Pull&Bear', 'Bershka', 'Stradivarius', 'Topshop', 'Fashion Nova',
    'Urban Outfitters', 'ASOS', 'Boohoo', 'PrettyLittleThing', 'Missguided', 'Cotton On', 'Old Navy', 'GAP',
    'C&A', 'New Look', 'River Island', 'Next', 'Reserved', 'Monki', 'Weekday', '& Other Stories', 'Oysho',
    'Massimo Dutti', 'LC Waikiki', 'Defacto', 'Giordano', 'Baleno', 'Metersbonwe', 'UR (Urban Revivo)', 'Sinsay',
    'Lindex', 'Gina Tricot', 'Cubus', 'Terranova', 'Calliope', 'Splash', 'Max Fashion', 'Westside', 'Pantaloons',
    'Reliance Trends', 'Shoppers Stop', 'Avra', 'NA-KD', 'Revolve', 'FabIndia', 'Biba', 'W for Woman', 'Manyavar',
    
    # Food & Consumables
    'Whole Foods', 'Trader Joe\'s', 'Nestle', 'Coca-Cola', 'Pepsi', 'Danone', 'Beyond Meat', 'Impossible Foods',
    'Amul', 'Britannia', 'Haldiram\'s', 'ITC', 'Mother Dairy', 'Tata Consumer', 'Organic India', '24 Mantra',
    
    # Eco & Specialized
    'Local Thrift Store', 'Goodwill', 'Salvation Army', 'Depop', 'Poshmark', 'Etsy', 'eBay', 'ThredUp', 'Vinted',
    'Back Market', 'Gazelle', 'Cashify', 'OLX', 'Quikr',
    'Local Farm', 'Farmers Market', 'Small Business', 'Handmade', 'Generic', 'Zero Waste Store',
    'Bambooee', 'Who Gives A Crap', 'Stasher', 'Swell', 'Hydro Flask', 'Klean Kanteen',
    'Mamaearth', 'Forest Essentials', 'Kama Ayurveda', 'Khadi Natural', 'Bare Necessities',
    'Other'
]

# Simplified Multipliers for logic
def get_product_multiplier(product_type: str) -> float:
    base_multipliers = {
        # High Impact
        'Fast Fashion': 2.5, 'Jeans': 3.2, 'Coat': 4.2, 'Leather Goods': 3.5, 'Shoes': 3.0, 'Sneakers': 3.0,
        'Electronics': 1.8, 'Smartphone': 2.5, 'Laptop': 3.0, 'Desktop Computer': 3.5, 'Gaming Console': 3.0, 'TV': 3.0,
        'Meat': 1.5, 'Dairy Products': 0.6, 'Cheese': 1.0, 'Flight Ticket': 5.0, 'Car Parts': 2.0,
        'Sofa': 4.0, 'Bed': 3.5, 'Appliance': 2.0, 'AC': 4.0,
        
        # Medium Impact
        'Cotton Shirt': 1.5, 'T-Shirt': 1.5, 'Furniture': 1.5, 'Cosmetics': 1.5, 'Perfume': 1.5,
        'Books (New)': 0.5, 'Paper': 0.5, 'Plastic Items': 2.0,

        # Low Impact / Eco
        'Local Groceries': 0.3, 'Organic Vegetables': 0.2, 'Bulk Grains': 0.2, 'Plant-Based Meat': 0.5,
        'Bamboo Fabric': 0.8, 'Hemp Clothing': 0.6, 'Linen Shirt': 0.8, 'Organic Cotton': 0.8,
        'Books (Used)': 0.05, 'E-book': 0.02, 'Audiobook': 0.02, 'Digital Download': 0.02,
        'Bicycle': 5.0, 
        'Used Electronics': 0.15, 'Refurbished Tech': 0.15, 'Refurbished Smartphone': 0.2,
        'Second-Hand Item': 0.1, 'Thrifted Clothing': 0.08, 'Vintage Furniture': 0.1,
        'Service': 0.0, 'Repair Service': 0.05, 'Rental Dress': 0.1,
        'Solar Charger': 1.0, 'LED Bulb': 0.1
    }
    
    if product_type in base_multipliers:
        return base_multipliers[product_type]
    elif 'Refurbished' in product_type or 'Used' in product_type or 'Second-Hand' in product_type or 'Thrift' in product_type:
        return 0.1
    elif 'Bamboo' in product_type or 'Hemp' in product_type or 'Organic' in product_type:
        return 0.5
    elif 'Rental' in product_type:
        return 0.1
    elif 'Leather' in product_type:
        return 3.5
    elif 'Plastic' in product_type:
        return 2.0
    else:
        return 1.0

ECO_FRIENDLY_CATEGORIES = [
    'Second-Hand Item', 'Local Groceries', 'Books (Used)', 'Thrifted Clothing',
    'Used Electronics', 'Vintage Furniture', 'Organic Vegetables', 'Organic Fruits',
    'Refurbished Tech', 'Bicycle', 'Vegan Leather', 'Digital Download',
    'Refurbished Smartphone', 'Refurbished Laptop', 'Bamboo Fabric Clothing', 'Hemp Clothing',
    'Plant-Based Meat', 'Oat Milk', 'Reclaimed Wood Table', 'Compostable Plates',
    'Solar Charger', 'Repair Service', 'Rental Dress', 'Library Membership', 'Public Transit Pass',
    'Ugly Produce', 'Bulk Grains'
]

# ==================== BADGE SYSTEM ====================
BADGES = {
    'first_step': {'name': '🌱 First Step', 'desc': 'Logged your first purchase', 'icon': '🌱'},
    'thrift_king': {'name': '👑 Thrift King', 'desc': 'Bought 3 second-hand items', 'icon': '👑'},
    'low_carbon': {'name': '🍃 Low Carbon', 'desc': 'Logged an item with < 1kg CO₂', 'icon': '🍃'},
    'big_saver': {'name': '💰 Big Saver', 'desc': 'Spent over ₹10,000 in one go', 'icon': '💰'},
    'eco_warrior': {'name': '🛡️ Eco Warrior', 'desc': 'Maintained < 50kg CO₂ total', 'icon': '🛡️'},
    'consistent': {'name': '📅 Consistent', 'desc': 'Logged 5 items total', 'icon': '📅'}
}

# ==================== DATA MANAGEMENT ====================
DATA_FILE = Path("shopimpact_data_v3.json")

def get_default_data() -> Dict:
    return {
        'purchases': [],
        'user_profile': {
            'name': 'Friend',
            'monthlyBudget': 15000,
            'co2Goal': 50,
            'badges': []
        }
    }

@st.cache_data
def load_data_cached() -> Dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return get_default_data()
    return get_default_data()

def save_data(data: Dict) -> None:
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        load_data_cached.clear()
    except Exception as e:
        st.error(f"Error saving data: {e}")

# ==================== LOGIC FUNCTIONS ====================

def suggest_eco_option(selected_product: str) -> Optional[str]:
    suggestions = {
        'T-Shirt': "Consider **Organic Cotton**, **Hemp**, or **Thrifted** T-Shirts. They use up to 90% less water!",
        'Jeans': "Did you know **Vintage Jeans** or **Hemp Denim** are way more durable and eco-friendly?",
        'Dress': "How about a **Rental Dress** for that occasion? Or check a local **Thrift Store**.",
        'Smartphone': "A **Refurbished Smartphone** saves ~50kg of CO₂ compared to a new one!",
        'Laptop': "Check out **Refurbished Laptops** or upgrade your RAM instead of buying new.",
        'Meat': "Try **Plant-Based Meat** or have a 'Meatless Monday' to slash your carbon footprint.",
        'Dairy Products': "**Oat Milk** or **Soy Milk** have a much lower carbon footprint than dairy.",
        'Furniture': "Look for **Vintage**, **Second-Hand**, or **FSC-Certified Wood** furniture.",
        'Books (New)': "Try a **Library Membership**, **Used Books**, or **E-books** to save paper.",
        'Bottled Water': "Switch to a **Reusable Bottle** and filtered tap water. Plastic is forever!",
        'Fast Fashion': "Slow down! Try **Thrifted** or **High-Quality Ethical Brands** that last longer.",
        'Toothbrush': "Switch to a **Bamboo Toothbrush** - plastic ones take 400 years to decompose.",
        'Shampoo': "Try a **Solid Shampoo Bar** to eliminate plastic bottle waste.",
        'Coffee': "Use a **Reusable Cup**. Disposable cups are lined with plastic and rarely recycled.",
        'Gift Wrap': "Use **Old Newspapers** or **Fabric Wraps** (Furoshiki) instead of glossy paper."
    }
    
    if selected_product in suggestions:
        return suggestions[selected_product]
    
    if 'Meat' in selected_product:
        return suggestions['Meat']
    if 'Phone' in selected_product or 'Mobile' in selected_product:
        return suggestions['Smartphone']
    if 'Laptop' in selected_product or 'Computer' in selected_product:
        return suggestions['Laptop']
    if 'Clothing' in selected_product or 'Wear' in selected_product or 'Jacket' in selected_product:
        return suggestions['Fast Fashion']
    
    return None

def trigger_animation(is_eco: bool):
    """Triggers a 1-second burst of leaves."""
    leaves_html = ""
    # Setup for Eco (Green Rising) vs Non-Eco (Dry Falling)
    if is_eco:
        css_class = "green-leaf-burst"
        leaf_char = "🍃"
    else:
        css_class = "dry-leaf-burst"
        leaf_char = "🍂"
        
    # Generate 25 leaves with random horizontal positions and slight delay staggering
    for i in range(25):
        left_pos = random.randint(5, 95)
        delay = random.uniform(0, 0.5) # Stagger start times slightly
        # Randomize size slightly
        size = random.uniform(1.5, 3.0)
        leaves_html += f"""
        <div class="{css_class}" 
             style="left: {left_pos}%; animation-delay: {delay}s; font-size: {size}rem;">
             {leaf_char}
        </div>
        """
    
    st.markdown(leaves_html, unsafe_allow_html=True)

def check_badges():
    purchases = st.session_state.purchases
    my_badges = st.session_state.user_profile['badges']
    new_badge = None

    if len(purchases) >= 1 and 'first_step' not in my_badges:
        new_badge = 'first_step'
    
    thrift_count = sum(1 for p in purchases if p['type'] in ECO_FRIENDLY_CATEGORIES)
    if thrift_count >= 3 and 'thrift_king' not in my_badges:
        new_badge = 'thrift_king'
        
    if purchases and purchases[-1]['co2_impact'] < 1.0 and 'low_carbon' not in my_badges:
        new_badge = 'low_carbon'
        
    if purchases and purchases[-1]['price'] > 10000 and 'big_saver' not in my_badges:
        new_badge = 'big_saver'

    if len(purchases) >= 5 and 'consistent' not in my_badges:
        new_badge = 'consistent'

    if new_badge:
        st.session_state.user_profile['badges'].append(new_badge)
        badge_info = BADGES[new_badge]
        st.toast(f"🏆 BADGE UNLOCKED: {badge_info['name']}", icon=badge_info['icon'])
        # REMOVED BALLOONS HERE as per request
        save_data({
            'purchases': st.session_state.purchases,
            'user_profile': st.session_state.user_profile
        })

def add_purchase(product_type: str, brand: str, price: float):
    co2_impact = price * get_product_multiplier(product_type) / 100
    if product_type in ECO_FRIENDLY_CATEGORIES:
        co2_impact *= 0.5
    
    purchase = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'type': product_type,
        'brand': brand,
        'price': float(price),
        'co2_impact': float(co2_impact)
    }
    st.session_state.purchases.append(purchase)
    
    save_data({
        'purchases': st.session_state.purchases,
        'user_profile': st.session_state.user_profile
    })
    check_badges()

# ==================== INITIALIZATION ====================
if 'initialized' not in st.session_state:
    data = load_data_cached()
    st.session_state.purchases = data.get('purchases', [])
    st.session_state.user_profile = data.get('user_profile', get_default_data()['user_profile'])
    if 'badges' not in st.session_state.user_profile:
        st.session_state.user_profile['badges'] = []
    st.session_state.initialized = True

# ==================== MAIN UI ====================

# HEADER
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 🍃 ShopImpact")
    st.markdown("### *Your Conscious Shopping Companion*")
with col_h2:
    if st.session_state.user_profile['badges']:
        latest = st.session_state.user_profile['badges'][-1]
        st.info(f"Latest Badge: {BADGES[latest]['icon']} {BADGES[latest]['name']}")
    else:
        st.info("Start shopping to earn badges!")

st.markdown("---")

# TABS
tab_dash, tab_analytics, tab_profile = st.tabs(["🛍️ Dashboard", "📊 Analytics", "🏆 Profile & Badges"])

# --- DASHBOARD TAB ---
with tab_dash:
    col_input, col_stats = st.columns([1, 1.5], gap="large")
    
    with col_input:
        st.markdown("#### 📝 New Purchase")
        with st.container():
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            # Ensure unique key for form
            with st.form("add_item_form_v2", clear_on_submit=False):
                product_type = st.selectbox("📦 What did you buy?", PRODUCT_TYPES)
                
                # --- DYNAMIC ECO SUGGESTION ---
                suggestion = suggest_eco_option(product_type)
                if suggestion:
                    st.markdown(f'<div class="eco-suggestion">💡 {suggestion}</div>', unsafe_allow_html=True)
                
                brand = st.selectbox("🏷️ Brand", ALL_BRANDS)
                
                price = st.slider("💰 Price (₹)", min_value=0, max_value=50000, value=500, step=100)
                
                submitted = st.form_submit_button("Add to Tracker", type="primary", use_container_width=True)
                
                if submitted:
                    if price > 0:
                        add_purchase(product_type, brand, price)
                        st.success(f"Added {product_type}!")
                        
                        # TRIGGER ANIMATION LOGIC
                        is_eco_purchase = product_type in ECO_FRIENDLY_CATEGORIES
                        trigger_animation(is_eco_purchase)
                        
                    else:
                        st.warning("Please set a price greater than 0.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("#### 💡 Quick Eco-Tip")
            tips = [
                "Buying used saves ~80% CO₂ vs new!",
                "Local produce = 5x less transport emissions.",
                "Repair > Replace.",
                "Combine deliveries to save fuel.",
                "Thrifting is the new cool.",
                "Eating plant-based just one day a week makes a huge difference."
            ]
            st.info(random.choice(tips))

    with col_stats:
        st.markdown("#### 🚀 Live Impact Overview")
        
        if st.session_state.purchases:
            df = pd.DataFrame(st.session_state.purchases)
            total_spend = df['price'].sum()
            total_co2 = df['co2_impact'].sum()
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Spent", f"₹{total_spend:,.0f}", delta=f"{len(df)} items")
            with m2:
                st.metric("Total CO₂", f"{total_co2:.1f} kg", delta_color="inverse", delta="Low is good!")
            with m3:
                eco_items = df[df['type'].isin(ECO_FRIENDLY_CATEGORIES)].shape[0]
                rate = (eco_items/len(df)*100) if len(df) > 0 else 0
                st.metric("Eco Choices", f"{eco_items}", f"{rate:.0f}% Rate")

            st.markdown("#### 🕰️ Recent Activity")
            recent = df.tail(5).iloc[::-1]
            for _, row in recent.iterrows():
                icon = "🍃" if row['type'] in ECO_FRIENDLY_CATEGORIES else "🛍️"
                color = "#2e7d32" if row['type'] in ECO_FRIENDLY_CATEGORIES else "#4a5568"
                st.markdown(
                    f"""
                    <div style="padding: 10px; background: rgba(255,255,255,0.7); border-radius: 10px; margin-bottom: 8px; border-left: 4px solid {color}; color: black;">
                        <span style="font-size: 1.2rem;">{icon}</span> 
                        <strong>{row['type']}</strong> ({row['brand']}) 
                        <span style="float: right; color: #000; font-weight: bold;">₹{row['price']:,.0f} | {row['co2_impact']:.1f}kg CO₂</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
                <div style="text-align: center; padding: 40px; color: #000;">
                    <h3>👻 Nothing here yet!</h3>
                    <p>Log your first purchase to see your impact statistics.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

# --- ANALYTICS TAB ---
with tab_analytics:
    if st.session_state.purchases:
        df = pd.DataFrame(st.session_state.purchases)
        df['date_dt'] = pd.to_datetime(df['date'])
        
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            st.markdown("### 📅 Spending vs CO₂ Over Time")
            fig_line = px.line(df, x='date_dt', y=['price', 'co2_impact'], markers=True, 
                               labels={'value': 'Amount', 'date_dt': 'Date'},
                               color_discrete_map={'price': '#2ecc71', 'co2_impact': '#e74c3c'})
            fig_line.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                legend_title_text='',
                font=dict(color='black')
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with row1_col2:
            st.markdown("### 🍩 Category Impact Breakdown")
            fig_pie = px.sunburst(df, path=['type', 'brand'], values='co2_impact', 
                                  color='co2_impact', color_continuous_scale='RdYlGn_r')
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='black'))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("### 📉 Efficiency Scatter Plot (Price vs Impact)")
        st.caption("Identify items that were expensive but low impact (Green zone) vs cheap but high impact (Red zone)")
        fig_scatter = px.scatter(df, x='price', y='co2_impact', color='type', size='co2_impact',
                                 hover_data=['brand'], size_max=40)
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(255,255,255,0.4)',
            xaxis_title="Price (₹)",
            yaxis_title="CO₂ Impact (kg)",
            font=dict(color='black')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    else:
        st.info("Log some data to unlock analytics!")

# --- PROFILE TAB ---
with tab_profile:
    p_col1, p_col2 = st.columns([1, 1])
    
    with p_col1:
        st.markdown("### ⚙️ Settings")
        with st.form("profile_update_v2"):
            new_name = st.text_input("Display Name", st.session_state.user_profile['name'])
            new_budget = st.number_input("Monthly Budget (₹)", value=st.session_state.user_profile['monthlyBudget'])
            new_goal = st.number_input("CO₂ Limit Goal (kg)", value=st.session_state.user_profile['co2Goal'])
            
            if st.form_submit_button("Update Profile"):
                st.session_state.user_profile.update({
                    'name': new_name,
                    'monthlyBudget': new_budget,
                    'co2Goal': new_goal
                })
                save_data({'purchases': st.session_state.purchases, 'user_profile': st.session_state.user_profile})
                st.success("Updated!")
                st.rerun()
                
        if st.button("🗑️ Reset All Data", type="secondary"):
            st.session_state.purchases = []
            st.session_state.user_profile['badges'] = []
            save_data(get_default_data())
