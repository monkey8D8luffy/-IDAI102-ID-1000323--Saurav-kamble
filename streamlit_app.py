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
        'Fast Fashion': 2.5, 'Jeans': 3.2, 'Coat': 4.2, 'Leather Goods': 3.5, 'Shoes': 3.0, 'Sneakers':
