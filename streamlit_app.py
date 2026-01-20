import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import random
from pathlib import Path
from typing import Dict, List, Optional

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ShopImpact 🍃",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapsed sidebar for cleaner look
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
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stMetricLabel {
        color: #0d0d0d !important;
    }
    .stMetricValue {
        color: #1a1a1a !important;
    }
    
    /* --- INPUT FIELDS & CARDS --- */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.1);
    }

    /* --- ANALYTICS DASHBOARD CARDS --- */
    .kpi-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
    .kpi-icon { font-size: 2.5rem; margin-bottom: 10px; }
    .kpi-value { font-size: 1.5rem; font-weight: 800; color: #333; }
    .kpi-label { font-size: 0.8rem; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

    /* --- IMPROVED BADGE POPUP --- */
    @keyframes popIn {
        0% { transform: scale(0); opacity: 0; }
        60% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }

    .badge-popup-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.6);
        z-index: 10000;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(8px);
    }
    .badge-popup-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        padding: 40px;
        border-radius: 30px;
        text-align: center;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        border: 4px solid #4ade80;
        animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        max-width: 450px;
        width: 90%;
        position: relative;
    }
    .badge-popup-icon { font-size: 5rem; margin-bottom: 10px; display: block; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1)); }
    .badge-popup-title { font-size: 2rem; font-weight: 900; color: #15803d !important; margin: 0; text-transform: uppercase; letter-spacing: 1px;}
    .badge-popup-subtitle { font-size: 1.5rem; color: #333 !important; font-weight: 700; margin-top: 5px; }
    .badge-popup-desc { font-size: 1.1rem; color: #4b5563 !important; margin-top: 10px; line-height: 1.4; }
    
    /* Close Buttons */
    .close-btn-corner {
        position: absolute; top: 15px; right: 20px;
        font-size: 2rem; color: #9ca3af; cursor: pointer;
        background: none; border: none; font-weight: bold;
        transition: color 0.2s;
    }
    .close-btn-corner:hover { color: #dc2626; }

    .close-btn-main {
        margin-top: 25px;
        background: #22c55e; color: white;
        border: none; padding: 12px 30px;
        border-radius: 50px; font-weight: bold; font-size: 1rem;
        cursor: pointer; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
        transition: transform 0.2s;
    }
    .close-btn-main:hover { transform: scale(1.05); background: #16a34a; }

    .badge-popup-rarity {
        display: inline-block; margin-top: 15px; padding: 5px 15px;
        background: #dcfce7; color: #15803d; border-radius: 20px;
        font-weight: 800; font-size: 0.8rem; text-transform: uppercase;
    }

    /* --- BADGE GRID --- */
    .badge-grid-item {
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.2s;
        margin-bottom: 10px;
        height: 140px; /* Fixed height for alignment */
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .badge-grid-item.locked { opacity: 0.5; filter: grayscale(1); background: rgba(255,255,255,0.3); }
    .badge-grid-item:hover { transform: scale(1.05); background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .badge-grid-icon { font-size: 2.5rem; margin-bottom: 5px; }
    .badge-grid-name { font-weight: 700; font-size: 0.9rem; margin-top: 5px; color: #000; line-height: 1.2; }

    /* --- ANIMATION HELPERS --- */
    .green-leaf-burst {
        position: fixed; bottom: -10vh; color: #2e7d32 !important;
        animation: riseFast 1s linear forwards; pointer-events: none; z-index: 9999;
    }
    .dry-leaf-burst {
        position: fixed; top: -10vh; color: #8D6E63 !important;
        animation: fallFast 1s linear forwards; pointer-events: none; z-index: 9999;
    }
    @keyframes riseFast { 0% { transform: translateY(110vh) rotate(0deg); opacity: 1; } 100% { transform: translateY(-10vh) rotate(-360deg); opacity: 0; } }
    @keyframes fallFast { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; } 100% { transform: translateY(110vh) rotate(360deg); opacity: 0; } }
    
    /* Suggestion Box */
    .eco-suggestion {
        background-color: #f0fdf4; border-left: 5px solid #22c55e;
        padding: 12px; border-radius: 8px; margin: 10px 0;
        color: #14532d !important; font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONSTANTS ====================
PRODUCT_TYPES = [
    'Fast Fashion', 'T-Shirt', 'Jeans', 'Dress', 'Suit', 'Jacket', 'Sweater', 'Hoodie', 'Shorts', 'Skirt',
    'Blazer', 'Coat', 'Pants', 'Leggings', 'Activewear', 'Swimwear', 'Underwear', 'Socks', 'Shoes', 'Sneakers',
    'Cotton Shirt', 'Linen Shirt', 'Bamboo Fabric Clothing', 'Hemp Clothing', 'Recycled Polyester Gear',
    'Upcycled Jacket', 'Vegan Leather Jacket', 'Organic Cotton T-Shirt', 'Rental Dress', 'Rental Tuxedo',
    'Handloom Saree', 'Khadi Kurta', 'Ethical Wool Sweater', 'Silk Scarf (Ahimsa Silk)',
    'Electronics', 'Smartphone', 'Laptop', 'Tablet', 'Desktop Computer', 'Monitor', 'Keyboard', 'Mouse',
    'Headphones', 'Gaming Console', 'Smartwatch', 'Camera', 'TV', 'Speaker', 'Drone',
    'Refurbished Smartphone', 'Refurbished Laptop', 'Second-Hand Tablet', 'Used Camera Lens', 'Used Gaming Console',
    'E-Reader', 'Solar Charger', 'Rechargeable Batteries', 'Smart Thermostat', 'LED Smart Bulb',
    'Energy Efficient AC', 'Repair Service (Phone)', 'Repair Service (Laptop)',
    'Local Groceries', 'Organic Vegetables', 'Organic Fruits', 'Meat', 'Dairy Products', 'Snacks',
    'Restaurant Meal', 'Fast Food', 'Coffee', 'Dessert',
    'Plant-Based Meat', 'Oat Milk', 'Almond Milk', 'Soy Milk', 'Loose Leaf Tea', 'Fair Trade Coffee',
    'Bulk Grains (No Plastic)', 'Ugly Produce (Imperfect Veg)', 'Locally Sourced Honey', 'Home-Grown Herbs',
    'Compostable Coffee Pods', 'Tap Water (Filtered)', 'Bottled Water',
    'Home Decor', 'Sofa', 'Chair', 'Table', 'Bed', 'Mattress', 'Kitchenware', 'Appliance',
    'Vintage Furniture', 'Bamboo Furniture', 'Reclaimed Wood Table', 'Cast Iron Skillet (Lifetime)',
    'Glass Food Containers', 'Beeswax Wraps', 'Silicone Stasher Bags', 'Compostable Plates',
    'Biodegradable Trash Bags', 'Loofah Sponge', 'Bamboo Toothbrush', 'Safety Razor', 'Menstrual Cup',
    'Solid Shampoo Bar', 'Refillable Soap', 'Solar Garden Lights', 'Rainwater Harvesting Kit',
    'Car Parts', 'Tires', 'Car Accessories',
    'Bicycle', 'E-Bike', 'Electric Scooter', 'Public Transit Pass', 'Train Ticket', 'Flight Ticket',
    'EV Charging Session', 'Carpool Contribution', 'Walking Shoes',
    'Books (New)', 'Books (Used)', 'E-book', 'Vinyl Record', 'Video Game',
    'Library Membership', 'Digital Magazine Subscription', 'Audiobook', 'Digital Game Download',
    'Yoga Mat (Cork)', 'Gym Equipment', 'Sports Gear', 'Camping Gear', 'Used Sports Gear',
    'Musical Instrument (Used)', 'Art Supplies (Non-Toxic)',
    'Leather Goods', 'Vegan Leather',
    'Second-Hand Item', 'Thrifted Clothing', 'Used Electronics', 'Refurbished Tech',
    'Office Supplies', 'Stationery', 'Recycled Paper Notebook', 'Refillable Pen',
    'Gift Card', 'Subscription', 'Event Ticket', 'Digital Download', 'Carbon Offset Credit', 'Tree Planting Donation',
    '500+ (Other)'
]

ALL_BRANDS = [
    'Zara', 'H&M', 'Nike', 'Adidas', 'Uniqlo', 'Gucci', 'Louis Vuitton', 'Patagonia', 'The North Face', 'Levi\'s',
    'Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo', 'Asus', 'Microsoft', 'Google', 'Canon',
    'IKEA', 'West Elm', 'Pottery Barn', 'Ashley Furniture', 'Wayfair',
    'Sephora', 'L\'Oreal', 'Estee Lauder', 'Mac', 'Fenty Beauty', 'The Body Shop', 'Lush',
    'Amazon', 'Barnes & Noble', 'Penguin Random House', 'Nintendo', 'PlayStation', 'Xbox',
    'Toyota', 'Honda', 'Ford', 'Tesla', 'BMW', 'Tata Motors', 'Mahindra', 'Hyundai',
    'SHEIN', 'Forever 21', 'Primark', 'Mango', 'Pull&Bear', 'Bershka', 'Stradivarius', 'Topshop', 'Fashion Nova',
    'Urban Outfitters', 'ASOS', 'Boohoo', 'PrettyLittleThing', 'Missguided', 'Cotton On', 'Old Navy', 'GAP',
    'C&A', 'New Look', 'River Island', 'Next', 'Reserved', 'Monki', 'Weekday', '& Other Stories', 'Oysho',
    'Massimo Dutti', 'LC Waikiki', 'Defacto', 'Giordano', 'Baleno', 'Metersbonwe', 'UR (Urban Revivo)', 'Sinsay',
    'Lindex', 'Gina Tricot', 'Cubus', 'Terranova', 'Calliope', 'Splash', 'Max Fashion', 'Westside', 'Pantaloons',
    'Reliance Trends', 'Shoppers Stop', 'Avra', 'NA-KD', 'Revolve', 'FabIndia', 'Biba', 'W for Woman', 'Manyavar',
    'Whole Foods', 'Trader Joe\'s', 'Nestle', 'Coca-Cola', 'Pepsi', 'Danone', 'Beyond Meat', 'Impossible Foods',
    'Amul', 'Britannia', 'Haldiram\'s', 'ITC', 'Mother Dairy', 'Tata Consumer', 'Organic India', '24 Mantra',
    'Local Thrift Store', 'Goodwill', 'Salvation Army', 'Depop', 'Poshmark', 'Etsy', 'eBay', 'ThredUp', 'Vinted',
    'Back Market', 'Gazelle', 'Cashify', 'OLX', 'Quikr',
    'Local Farm', 'Farmers Market', 'Small Business', 'Handmade', 'Generic', 'Zero Waste Store',
    'Bambooee', 'Who Gives A Crap', 'Stasher', 'Swell', 'Hydro Flask', 'Klean Kanteen',
    'Mamaearth', 'Forest Essentials', 'Kama Ayurveda', 'Khadi Natural', 'Bare Necessities',
    'Other'
]

# Simplified Multipliers
def get_product_multiplier(product_type: str) -> float:
    base_multipliers = {
        'Fast Fashion': 2.5, 'Jeans': 3.2, 'Coat': 4.2, 'Leather Goods': 3.5, 'Shoes': 3.0, 'Sneakers': 3.0,
        'Electronics': 1.8, 'Smartphone': 2.5, 'Laptop': 3.0, 'Desktop Computer': 3.5, 'Gaming Console': 3.0, 'TV': 3.0,
        'Meat': 1.5, 'Dairy Products': 0.6, 'Cheese': 1.0, 'Flight Ticket': 5.0, 'Car Parts': 2.0,
        'Sofa': 4.0, 'Bed': 3.5, 'Appliance': 2.0, 'AC': 4.0,
        'Cotton Shirt': 1.5, 'T-Shirt': 1.5, 'Furniture': 1.5, 'Cosmetics': 1.5, 'Perfume': 1.5,
        'Books (New)': 0.5, 'Paper': 0.5, 'Plastic Items': 2.0,
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

# ==================== BADGE DATA ====================
BADGES = {
    # --- LEVEL 1: BEGINNER ---
    'first_step': {'name': 'First Step', 'desc': 'Logged your first purchase', 'icon': '🌱', 'rarity': 'Common'},
    'baby_steps': {'name': 'Baby Steps', 'desc': 'Logged 5 items total', 'icon': '👶', 'rarity': 'Common'},
    'bronze_logger': {'name': 'Bronze Logger', 'desc': 'Logged 10 items', 'icon': '🥉', 'rarity': 'Common'},
    'thrift_curious': {'name': 'Thrift Curious', 'desc': 'Bought 1 second-hand item', 'icon': '👀', 'rarity': 'Common'},
    'veggie_patch': {'name': 'Veggie Patch', 'desc': 'Bought organic vegetables twice', 'icon': '🥦', 'rarity': 'Common'},
    'hydration': {'name': 'Hydration Hero', 'desc': 'Avoided bottled water 5 times', 'icon': '💧', 'rarity': 'Common'},
    'bookworm': {'name': 'Bookworm', 'desc': 'Bought a book (new or used)', 'icon': '🐛', 'rarity': 'Common'},
    'tech_savvy': {'name': 'Tech Savvy', 'desc': 'Logged an electronic item', 'icon': '🔌', 'rarity': 'Common'},
    'fashionista': {'name': 'Fashionista', 'desc': 'Logged a clothing item', 'icon': '👗', 'rarity': 'Common'},
    'grocery_getter': {'name': 'Grocery Getter', 'desc': 'Logged 5 food items', 'icon': '🛒', 'rarity': 'Common'},

    # --- LEVEL 2: INTERMEDIATE ---
    'silver_logger': {'name': 'Silver Logger', 'desc': 'Logged 25 items', 'icon': '🥈', 'rarity': 'Uncommon'},
    'thrift_king': {'name': 'Thrift King', 'desc': 'Bought 5 second-hand items', 'icon': '👑', 'rarity': 'Uncommon'},
    'repair_master': {'name': 'Repair Master', 'desc': 'Used a repair service', 'icon': '🔧', 'rarity': 'Uncommon'},
    'plastic_hater': {'name': 'Plastic Hater', 'desc': 'Bought 5 plastic-free items', 'icon': '🚫', 'rarity': 'Uncommon'},
    'vegan_vibes': {'name': 'Vegan Vibes', 'desc': 'Bought plant-based meat or milk', 'icon': '🥑', 'rarity': 'Uncommon'},
    'low_carbon': {'name': 'Low Carbon', 'desc': 'Logged an item with < 0.5kg CO₂', 'icon': '🍃', 'rarity': 'Uncommon'},
    'rental_star': {'name': 'Rental Star', 'desc': 'Rented clothes or gear', 'icon': '🌠', 'rarity': 'Uncommon'},
    'public_mover': {'name': 'Public Mover', 'desc': 'Used public transport or bike', 'icon': '🚌', 'rarity': 'Uncommon'},
    'bulk_buyer': {'name': 'Bulk Buyer', 'desc': 'Bought bulk grains', 'icon': '⚖️', 'rarity': 'Uncommon'},
    'local_legend': {'name': 'Local Legend', 'desc': 'Shopped local 3 times', 'icon': '📍', 'rarity': 'Uncommon'},

    # --- LEVEL 3: ADVANCED ---
    'gold_logger': {'name': 'Gold Logger', 'desc': 'Logged 50 items', 'icon': '🥇', 'rarity': 'Rare'},
    'vintage_vulture': {'name': 'Vintage Vulture', 'desc': 'Bought vintage furniture', 'icon': '🏺', 'rarity': 'Rare'},
    'tech_rescuer': {'name': 'Tech Rescuer', 'desc': 'Bought refurbished tech', 'icon': '💾', 'rarity': 'Rare'},
    'zero_waster': {'name': 'Zero Waster', 'desc': 'Bought 10 eco-friendly items', 'icon': '♻️', 'rarity': 'Rare'},
    'tree_hugger': {'name': 'Tree Hugger', 'desc': 'Saved 100kg CO₂ total', 'icon': '🌳', 'rarity': 'Rare'},
    'big_saver': {'name': 'Big Saver', 'desc': 'Spent over ₹10,000 but stayed eco', 'icon': '💰', 'rarity': 'Rare'},
    'ethical_threads': {'name': 'Ethical Threads', 'desc': 'Bought organic cotton or hemp', 'icon': '🧵', 'rarity': 'Rare'},
    'energy_miser': {'name': 'Energy Miser', 'desc': 'Bought LED or Solar items', 'icon': '💡', 'rarity': 'Rare'},
    'flight_skipper': {'name': 'Flight Skipper', 'desc': 'Chose train over plane', 'icon': '🚆', 'rarity': 'Rare'},
    'consistent': {'name': 'Consistent', 'desc': 'Logged items 3 days in a row', 'icon': '📅', 'rarity': 'Rare'},

    # --- LEVEL 4: ELITE ---
    'diamond_logger': {'name': 'Diamond Logger', 'desc': 'Logged 100 items', 'icon': '💎', 'rarity': 'Epic'},
    'eco_warrior': {'name': 'Eco Warrior', 'desc': '50% of all purchases are Eco', 'icon': '🛡️', 'rarity': 'Epic'},
    'carbon_neutral': {'name': 'Carbon Neutral', 'desc': 'Offset your emissions', 'icon': '⚖️', 'rarity': 'Epic'},
    'planet_savior': {'name': 'Planet Savior', 'desc': 'Saved 500kg CO₂ total', 'icon': '🌍', 'rarity': 'Epic'},
    'minimalist': {'name': 'Minimalist', 'desc': 'Logged < 5 items in a month', 'icon': '🧘', 'rarity': 'Epic'},
    'second_life': {'name': 'Second Life', 'desc': '10 Refurbished/Used items total', 'icon': '🧟', 'rarity': 'Epic'},
    'plastic_terminator': {'name': 'Plastic Terminator', 'desc': '20 Plastic-free items', 'icon': '🦾', 'rarity': 'Epic'},
    'influencer': {'name': 'Influencer', 'desc': 'Shared your impact (simulated)', 'icon': '🤳', 'rarity': 'Epic'},
    'guardian_angel': {'name': 'Guardian Angel', 'desc': 'Kept total CO2 under 10kg for 10 items', 'icon': '👼', 'rarity': 'Epic'},
    'arctic_guardian': {'name': 'Arctic Guardian', 'desc': 'Saved 50 sq ft of Ice (calc)', 'icon': '❄️', 'rarity': 'Legendary'},
    
    # --- SECRET/FUN ---
    'richie_rich': {'name': 'Richie Rich', 'desc': 'Spent ₹50k in one item', 'icon': '🎩', 'rarity': 'Special'},
    'oopsie': {'name': 'Oopsie', 'desc': 'Logged an item with > 50kg CO₂', 'icon': '🤡', 'rarity': 'Special'},
    'night_owl': {'name': 'Night Owl', 'desc': 'Logged an item after 11 PM', 'icon': '🦉', 'rarity': 'Special'},
    'morning_bird': {'name': 'Morning Bird', 'desc': 'Logged an item before 7 AM', 'icon': '🐦', 'rarity': 'Special'},
    'coffee_addict': {'name': 'Coffee Addict', 'desc': 'Logged 5 coffees', 'icon': '☕', 'rarity': 'Special'},
    'gamer': {'name': 'Gamer', 'desc': 'Bought a game or console', 'icon': '🎮', 'rarity': 'Special'},
    'musician': {'name': 'Musician', 'desc': 'Bought an instrument', 'icon': '🎸', 'rarity': 'Special'},
    'artist': {'name': 'Artist', 'desc': 'Bought art supplies', 'icon': '🎨', 'rarity': 'Special'},
    'sweet_tooth': {'name': 'Sweet Tooth', 'desc': 'Bought dessert 3 times', 'icon': '🍬', 'rarity': 'Special'},
    'weekend_warrior': {'name': 'Weekend Warrior', 'desc': 'Bought camping/sports gear', 'icon': '🏕️', 'rarity': 'Special'},
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
            'badges': [],
            'joined_date': datetime.now().strftime('%Y-%m-%d')
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
    
    if 'Meat' in selected_product: return suggestions['Meat']
    if 'Phone' in selected_product or 'Mobile' in selected_product: return suggestions['Smartphone']
    if 'Laptop' in selected_product or 'Computer' in selected_product: return suggestions['Laptop']
    if 'Clothing' in selected_product or 'Wear' in selected_product or 'Jacket' in selected_product: return suggestions['Fast Fashion']
    
    return None

def trigger_animation(is_eco: bool):
    leaves_html = ""
    if is_eco:
        css_class = "green-leaf-burst"
        leaf_char = "🍃"
    else:
        css_class = "dry-leaf-burst"
        leaf_char = "🍂"
        
    for i in range(25):
        left_pos = random.randint(5, 95)
        delay = random.uniform(0, 0.5)
        size = random.uniform(1.5, 3.0)
        leaves_html += f"""
        <div class="{css_class}" 
             style="left: {left_pos}%; animation-delay: {delay}s; font-size: {size}rem;">
             {leaf_char}
        </div>
        """
    st.markdown(leaves_html, unsafe_allow_html=True)

def show_badge_popup(badge_key):
    badge = BADGES[badge_key]
    # NOTE: Added a clear Close button and X icon in the HTML using JS to hide the overlay
    # This prevents the need for a server round-trip just to close a modal.
    html_content = f"""
    <div class="badge-popup-overlay" id="badgeOverlay">
        <div class="badge-popup-card">
            <button class="close-btn-corner" onclick="document.getElementById('badgeOverlay').style.display='none'">×</button>
            <span class="badge-popup-icon">{badge['icon']}</span>
            <h2 class="badge-popup-title">Badge Unlocked!</h2>
            <h3 class="badge-popup-subtitle">{badge['name']}</h3>
            <p class="badge-popup-desc">{badge['desc']}</p>
            <div class="badge-popup-rarity">{badge['rarity']}</div>
            <br>
            <button class="close-btn-main" onclick="document.getElementById('badgeOverlay').style.display='none'">Awesome!</button>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def check_badges():
    purchases = st.session_state.purchases
    my_badges = st.session_state.user_profile['badges']
    new_badge_key = None
    
    count = len(purchases)
    eco_count = sum(1 for p in purchases if p['type'] in ECO_FRIENDLY_CATEGORIES)
    total_co2 = sum(p['co2_impact'] for p in purchases)
    
    # Check logic
    if count >= 1 and 'first_step' not in my_badges: new_badge_key = 'first_step'
    elif count >= 5 and 'baby_steps' not in my_badges: new_badge_key = 'baby_steps'
    elif count >= 10 and 'bronze_logger' not in my_badges: new_badge_key = 'bronze_logger'
    elif count >= 25 and 'silver_logger' not in my_badges: new_badge_key = 'silver_logger'
    elif count >= 50 and 'gold_logger' not in my_badges: new_badge_key = 'gold_logger'
    elif count >= 100 and 'diamond_logger' not in my_badges: new_badge_key = 'diamond_logger'
    
    elif eco_count >= 1 and 'thrift_curious' not in my_badges: new_badge_key = 'thrift_curious'
    elif eco_count >= 5 and 'thrift_king' not in my_badges: new_badge_key = 'thrift_king'
    elif eco_count >= 10 and 'zero_waster' not in my_badges: new_badge_key = 'zero_waster'
    
    elif count > 10 and (eco_count/count) >= 0.5 and 'eco_warrior' not in my_badges: new_badge_key = 'eco_warrior'
    
    if purchases:
        last = purchases[-1]
        if last['co2_impact'] < 0.5 and 'low_carbon' not in my_badges: new_badge_key = 'low_carbon'
        if last['price'] > 10000 and last['type'] in ECO_FRIENDLY_CATEGORIES and 'big_saver' not in my_badges: new_badge_key = 'big_saver'
        if last['price'] > 50000 and 'richie_rich' not in my_badges: new_badge_key = 'richie_rich'
        if last['co2_impact'] > 50 and 'oopsie' not in my_badges: new_badge_key = 'oopsie'
        
        # Category checks
        if 'Coffee' in last['type'] and 'coffee_addict' not in my_badges:
            coffee_count = sum(1 for p in purchases if 'Coffee' in p['type'])
            if coffee_count >= 5: new_badge_key = 'coffee_addict'
            
        if ('Game' in last['type'] or 'Console' in last['type']) and 'gamer' not in my_badges: new_badge_key = 'gamer'
        
        if 'Dessert' in last['type']:
             sweet_count = sum(1 for p in purchases if 'Dessert' in p['type'])
             if sweet_count >= 3 and 'sweet_tooth' not in my_badges: new_badge_key = 'sweet_tooth'

    # Save and Trigger
    if new_badge_key:
        st.session_state.user_profile['badges'].append(new_badge_key)
        save_data({'purchases': purchases, 'user_profile': st.session_state.user_profile})
        st.session_state.latest_badge_pop = new_badge_key 
        st.rerun()

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

# CHECK FOR POPUP
if 'latest_badge_pop' in st.session_state:
    show_badge_popup(st.session_state.latest_badge_pop)
    del st.session_state.latest_badge_pop

# ==================== MAIN UI ====================

# HEADER
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 🍃 ShopImpact")
    st.markdown("### *Your Conscious Shopping Companion*")
with col_h2:
    if st.session_state.user_profile['badges']:
        latest = st.session_state.user_profile['badges'][-1]
        st.info(f"Latest Badge: {BADGES[latest]['name']}")
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
            with st.form("add_item_form_v2", clear_on_submit=True): # Clear form after submit
                product_type = st.selectbox("📦 What did you buy?", PRODUCT_TYPES)
                
                suggestion = suggest_eco_option(product_type)
                if suggestion:
                    st.markdown(f'<div class="eco-suggestion">💡 {suggestion}</div>', unsafe_allow_html=True)
                
                brand = st.selectbox("🏷️ Brand", ALL_BRANDS)
                # UX IMPROVEMENT: Changed Slider to Number Input for easier exact pricing
                price = st.number_input("💰 Price (₹)", min_value=0.0, step=100.0, value=0.0)
                
                submitted = st.form_submit_button("Add to Tracker", type="primary", use_container_width=True)
                
                if submitted:
                    if price > 0:
                        add_purchase(product_type, brand, price)
                        st.success(f"Added {product_type}!")
                        is_eco_purchase = product_type in ECO_FRIENDLY_CATEGORIES
                        trigger_animation(is_eco_purchase)
                    else:
                        st.warning("Please set a price greater than 0.")
            
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
            with m1: st.metric("Total Spent", f"₹{total_spend:,.0f}", delta=f"{len(df)} items")
            with m2: st.metric("Total CO₂", f"{total_co2:.1f} kg", delta_color="inverse", delta="Low is good!")
            with m3:
                eco_items = df[df['type'].isin(ECO_FRIENDLY_CATEGORIES)].shape[0]
                rate = (eco_items/len(df)*100) if len(df) > 0 else 0
                st.metric("Eco Choices", f"{eco_items}", f"{rate:.0f}% Rate")

            st.markdown("#### 🕰️ Recent Activity")
            recent = df.tail(5).iloc[::-1]
            for _, row in recent.iterrows():
                icon = "🍃" if row['type'] in ECO_FRIENDLY_CATEGORIES else "🛍️"
                color = "#2e7d32" if row['type'] in ECO_FRIENDLY_CATEGORIES else "#4a5568"
                # Improved readability for recent items
                st.markdown(
                    f"""
                    <div style="padding: 12px; background: white; border-radius: 10px; margin-bottom: 8px; border-left: 5px solid {color}; box-shadow: 0 2px 4px rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <span style="font-size: 1.2rem; margin-right: 10px;">{icon}</span> 
                            <strong>{row['type']}</strong> <span style="color: #666; font-size: 0.9rem;">({row['brand']})</span>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: bold; color: #333;">₹{row['price']:,.0f}</div>
                            <div style="font-size: 0.8rem; color: #666;">{row['co2_impact']:.1f}kg CO₂</div>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.markdown("""<div style="text-align: center; padding: 40px; color: #333; background: rgba(255,255,255,0.5); border-radius: 15px;"><h3>👻 Nothing here yet!</h3><p>Log your first purchase to see your impact statistics.</p></div>""", unsafe_allow_html=True)

# --- ANALYTICS TAB ---
with tab_analytics:
    st.markdown("## Your Community Impact")
    
    if st.session_state.purchases:
        df = pd.DataFrame(st.session_state.purchases)
        df['date_dt'] = pd.to_datetime(df['date'])
        total_co2 = df['co2_impact'].sum()
        
        # 1. TOP CARDS
        trees_saved = int(total_co2 / 20) 
        lightbulbs = int(total_co2 * 10)
        ice_saved = int(total_co2 * 3) 
        cars_off_road = round(total_co2 / 4600, 4)
        
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">☁️</div><div class="kpi-value">{total_co2:.0f}</div><div class="kpi-label">Kg of CO2</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">🌲</div><div class="kpi-value">{trees_saved}</div><div class="kpi-label">Trees Equivalent</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">💡</div><div class="kpi-value">{lightbulbs}</div><div class="kpi-label">Lightbulbs Powered</div></div>""", unsafe_allow_html=True)
        with c4: st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">❄️</div><div class="kpi-value">{ice_saved}</div><div class="kpi-label">Sq ft Ice Saved</div></div>""", unsafe_allow_html=True)
        with c5: st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">🚗</div><div class="kpi-value">{cars_off_road}</div><div class="kpi-label">Cars off road</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. ROW 2 CHARTS
        r2c1, r2c2, r2c3 = st.columns([1.5, 1.5, 1])
        
        # Chart 1: Customer Adoption (Spending Trend Area Chart)
        with r2c1:
            st.markdown("### 📈 Spending Trend")
            daily_spend = df.groupby(df['date_dt'].dt.date)['price'].sum().reset_index()
            fig_area = px.area(daily_spend, x='date_dt', y='price', color_discrete_sequence=['#4ade80'])
            fig_area.update_layout(xaxis_title="", yaxis_title="", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(255,255,255,0.5)', margin=dict(l=20,r=20,t=20,b=20), height=250)
            fig_area.update_xaxes(showgrid=False)
            fig_area.update_yaxes(showgrid=True, gridcolor='#e5e7eb')
            st.plotly_chart(fig_area, use_container_width=True)
            
        # Chart 2: Emissions (Top Categories Horizontal Bar)
        with r2c2:
            st.markdown("### 🏭 Impact by Category")
            cat_impact = df.groupby('type')['co2_impact'].sum().sort_values(ascending=True).tail(5)
            # Simulate "Shipping vs Manufacturing"
            df_stack = pd.DataFrame({
                'Category': cat_impact.index,
                'Manufacturing': cat_impact.values * 0.7,
                'Shipping': cat_impact.values * 0.3
            })
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(y=df_stack['Category'], x=df_stack['Manufacturing'], name='Mfg', orientation='h', marker_color='#22c55e'))
            fig_bar.add_trace(go.Bar(y=df_stack['Category'], x=df_stack['Shipping'], name='Ship', orientation='h', marker_color='#86efac'))
            fig_bar.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(255,255,255,0.5)', margin=dict(l=20,r=20,t=20,b=20), height=250, showlegend=True, legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig_bar, use_container_width=True)

        # Chart 3: Demographic (Eco vs Non-Eco Pie)
        with r2c3:
            st.markdown("### 🥬 Eco Split")
            eco_count = df[df['type'].isin(ECO_FRIENDLY_CATEGORIES)].shape[0]
            non_eco_count = len(df) - eco_count
            fig_pie = px.pie(values=[eco_count, non_eco_count], names=['Eco', 'Std'], color_discrete_sequence=['#22c55e', '#374151'], hole=0.6)
            fig_pie.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10), height=250, paper_bgcolor='rgba(255,255,255,0)', annotations=[dict(text=f"{int(eco_count/len(df)*100)}%", x=0.5, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig_pie, use_container_width=True)
            
        # 3. ROW 3: TOTAL EMISSIONS (Bar Chart)
        st.markdown("### 📊 Total Emissions History")
        df['month'] = df['date_dt'].dt.strftime('%b')
        monthly_impact = df.groupby('month')['co2_impact'].sum().reset_index()
        monthly_impact['offset'] = monthly_impact['co2_impact'] * 0.4 
        
        fig_total = go.Figure()
        fig_total.add_trace(go.Bar(x=monthly_impact['month'], y=monthly_impact['co2_impact'], name='Total CO2', marker_color='#4ade80'))
        fig_total.add_trace(go.Bar(x=monthly_impact['month'], y=monthly_impact['offset'], name='Offset', marker_color='#15803d'))
        fig_total.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(255,255,255,0.5)', margin=dict(l=20,r=20,t=20,b=20), height=300)
        fig_total.update_yaxes(showgrid=True, gridcolor='#e5e7eb')
        st.plotly_chart(fig_total, use_container_width=True)

    else:
        st.info("Log some purchases to generate your analytics dashboard!")

# --- PROFILE TAB ---
with tab_profile:
    p_col1, p_col2 = st.columns([1, 2])
    
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
                
        st.divider()
        if st.button("🗑️ Reset All Data", type="secondary"):
            st.session_state.purchases = []
            st.session_state.user_profile['badges'] = []
            save_data(get_default_data())
            st.rerun()

    with p_col2:
        st.markdown("### 🏆 Your Badge Collection")
        my_badges = st.session_state.user_profile['badges']
        
        # Create a grid for badges
        cols = st.columns(4)
        for i, (key, badge) in enumerate(BADGES.items()):
            is_unlocked = key in my_badges
            col_idx = i % 4
            
            with cols[col_idx]:
                css_class = "badge-grid-item" if is_unlocked else "badge-grid-item locked"
                st.markdown(f"""
                <div class="{css_class}">
                    <div class="badge-grid-icon">{badge['icon']}</div>
                    <div class="badge-grid-name">{badge['name']}</div>
                    <div style="font-size:0.7rem; color:#666; margin-top: auto;">{badge['rarity'] if is_unlocked else 'Locked'}</div>
                </div>
                """, unsafe_allow_html=True)
