import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import random

# --- STAGE 1 & 3: CONFIGURATION & VISUAL STYLE ---
st.set_page_config(
    page_title="ShopImpact | Conscious Shopping",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS for Earthy Themes and Large Fonts
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F7F9F4; /* Soft Beige/Green tint */
    }
    /* Headers */
    h1, h2, h3 {
        color: #2E5936; /* Forest Green */
        font-family: 'Helvetica', sans-serif;
    }
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #4A7A58;
    }
    /* Buttons */
    div.stButton > button {
        background-color: #2E5936;
        color: white;
        border-radius: 10px;
        font-size: 18px;
    }
    div.stButton > button:hover {
        background-color: #4A7A58;
        border-color: #F7F9F4;
    }
    /* Success/Info boxes */
    div.stAlert {
        background-color: #E8F5E9;
        border: 1px solid #C8E6C9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STAGE 2: PYTHON LOGIC & DATA STRUCTURES ---

# Impact Multipliers (CO2 kg estimated per $ spent)
# This is a simplified logic as requested: Price * Multiplier
IMPACT_DATA = {
    "Fast Fashion": {"multiplier": 0.50, "alt": "Thrift stores, organic cotton, or hemp clothing.", "type": "high"},
    "Red Meat": {"multiplier": 0.80, "alt": "Plant-based proteins, lentils, or locally sourced poultry.", "type": "high"},
    "Electronics": {"multiplier": 0.30, "alt": "Refurbished tech or repair existing devices.", "type": "medium"},
    "Local Vegetables": {"multiplier": 0.05, "alt": "Great choice! Try growing your own herbs too.", "type": "low"},
    "Public Transport": {"multiplier": 0.02, "alt": "Walking or cycling is zero carbon!", "type": "low"},
    "Imported Snacks": {"multiplier": 0.40, "alt": "Bulk-buy local snacks or homemade alternatives.", "type": "medium"},
    "Eco-Certified Home": {"multiplier": 0.10, "alt": "Keep it up! Look for zero-waste packaging.", "type": "low"},
}

# Initialize Session State (The "Database")
if 'purchases' not in st.session_state:
    st.session_state.purchases = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = None 

# --- TURTLE GRAPHICS SIMULATION (Matplotlib) ---
# Since standard 'turtle' cannot run in a browser, we draw shapes programmatically
def draw_eco_graphic(graphic_type):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('#F7F9F4') # Match background
    
    if graphic_type == "leaf":
        # Draw a Leaf for good choices
        leaf = patches.Ellipse((5, 5), 4, 8, angle=45, color='#66BB6A')
        ax.add_patch(leaf)
        ax.text(5, 1, "Eco Choice!", ha='center', fontsize=12, color='#2E5936')
        
    elif graphic_type == "footprint":
        # Draw a footprint for high impact
        # Sole
        sole = patches.Ellipse((5, 4), 3, 5, color='#8D6E63')
        ax.add_patch(sole)
        # Toes
        for i in range(5):
            toe = patches.Circle((3.5 + (i*0.75), 7.5 - (abs(i-2)*0.3)), 0.3, color='#8D6E63')
            ax.add_patch(toe)
        ax.text(5, 0.5, "Heavy Footprint", ha='center', fontsize=12, color='#5D4037')
        
    elif graphic_type == "badge":
        # Draw a Star Badge
        star = patches.RegularPolygon((5, 5), numVertices=5, radius=4, orientation=0, color='#FFD54F')
        ax.add_patch(star)
        ax.text(5, 4.5, "ECO\nSAVER", ha='center', va='center', fontsize=14, fontweight='bold', color='#BF360C')

    return fig

# --- STAGE 3: INTERFACE LAYOUT ---

# Header
st.title("🌱 ShopImpact")
st.markdown("### Your Mindful Shopping Companion")
st.markdown("---")

# 1. SIDEBAR INPUTS
with st.sidebar:
    st.header("📝 Log a Purchase")
    
    item_name = st.text_input("Product Name (e.g., Denim Jacket)")
    category = st.selectbox("Product Category", list(IMPACT_DATA.keys()))
    price = st.number_input("Price ($)", min_value=0.0, step=0.5)
    brand = st.text_input("Brand Name")
    
    if st.button("Add to Dashboard"):
        if item_name and price > 0:
            # Logic: Calculate Impact
            factor = IMPACT_DATA[category]['multiplier']
            co2_impact = price * factor
            
            # Logic: Save to History
            new_purchase = {
                "Item": item_name,
                "Category": category,
                "Price": price,
                "Brand": brand,
                "CO2 (kg)": round(co2_impact, 2),
                "Time": datetime.now().strftime("%H:%M")
            }
            st.session_state.purchases.append(new_purchase)
            
            # Logic: Determine Graphic Type
            impact_type = IMPACT_DATA[category]['type']
            if impact_type == "low":
                st.session_state.last_action = "leaf"
            elif impact_type == "high":
                st.session_state.last_action = "footprint"
            else:
                st.session_state.last_action = "neutral"
                
            st.success("Logged!")
        else:
            st.error("Please enter a valid name and price.")

# 2. MAIN DASHBOARD

# Calculate Totals
if len(st.session_state.purchases) > 0:
    df = pd.DataFrame(st.session_state.purchases)
    total_spend = df["Price"].sum()
    total_co2 = df["CO2 (kg)"].sum()
    
    # Logic: Eco Score (Simple ratio)
    # Lower ratio of CO2 to Spend is better
    eco_ratio = total_co2 / total_spend if total_spend > 0 else 0
else:
    df = pd.DataFrame(columns=["Item", "Category", "Price", "Brand", "CO2 (kg)", "Time"])
    total_spend = 0
    total_co2 = 0
    eco_ratio = 0

# --- METRICS ROW ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Spend", f"${total_spend:.2f}")
with col2:
    st.metric("Estimated Footprint", f"{total_co2:.2f} kg CO₂")
with col3:
    if eco_ratio < 0.3 and total_spend > 0:
        st.metric("Status", "Eco Warrior! 🌿")
    elif eco_ratio < 0.6 and total_spend > 0:
        st.metric("Status", "Conscious Shopper 🚶")
    else:
        st.metric("Status", "High Impact 🏭")

# --- FEEDBACK & GRAPHICS AREA ---
st.markdown("### 🎨 Visual Feedback")
c1, c2 = st.columns([1, 2])

with c1:
    # This is where the "Turtle" draws
    if st.session_state.last_action == "leaf":
        st.pyplot(draw_eco_graphic("leaf"))
        st.caption("You made a green choice! A leaf is added to your garden.")
    elif st.session_state.last_action == "footprint":
        st.pyplot(draw_eco_graphic("footprint"))
        st.caption("High impact purchase detected. Here is the footprint left behind.")
    elif total_spend > 50 and eco_ratio < 0.2:
        st.pyplot(draw_eco_graphic("badge"))
        st.caption("Achievement Unlocked: Eco Saver Badge!")
    else:
        st.info("Log a purchase to see your impact drawing!")

with c2:
    # Suggestions based on last input
    if len(st.session_state.purchases) > 0:
        last_cat = st.session_state.purchases[-1]["Category"]
        suggestion = IMPACT_DATA[last_cat]["alt"]
        st.info(f"💡 **Tip for your recent {last_cat} purchase:**")
        st.markdown(f"> {suggestion}")
        
        # Random motivational quote
        quotes = [
            "Small acts, when multiplied by millions of people, can transform the world.",
            "Buy less, choose well, make it last.",
            "Every dollar you spend is a vote for the kind of world you want."
        ]
        st.markdown(f"*{random.choice(quotes)}*")

# --- DATA VISUALIZATION ---
st.markdown("---")
st.markdown("### 📊 Monthly Impact Dashboard")

if not df.empty:
    tab1, tab2 = st.tabs(["Spending vs Impact", "Recent Log"])
    
    with tab1:
        # Simple Bar Chart comparing Spend vs CO2 per item
        chart_data = df.set_index("Item")[["Price", "CO2 (kg)"]]
        st.bar_chart(chart_data)
        
    with tab2:
        st.dataframe(df, use_container_width=True)
else:
    st.markdown("Start logging items to see your dashboard come to life!")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
        Made with 💚 by ShopImpact Ltd.
    </div>
    """, 
    unsafe_allow_html=True
) 
