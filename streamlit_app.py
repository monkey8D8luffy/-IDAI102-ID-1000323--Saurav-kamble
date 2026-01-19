import streamlit as st
import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ShopImpact",
    layout="wide"
)

# ---------------- SESSION STATE INIT ----------------
if "show_badge_popup" not in st.session_state:
    st.session_state.show_badge_popup = False

if "oopsie_unlocked" not in st.session_state:
    st.session_state.oopsie_unlocked = False

# ---------------- STYLES ----------------
st.markdown("""
<style>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.popup-box {
    background: #ffffff;
    padding: 35px;
    border-radius: 16px;
    width: 420px;
    text-align: center;
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    border: 3px solid #6BE585;
}

.popup-box h1 {
    margin-bottom: 10px;
}

.badge {
    font-size: 64px;
}

.special {
    margin-top: 10px;
    display: inline-block;
    padding: 6px 16px;
    background: #e6fff0;
    border-radius: 20px;
    font-weight: bold;
    color: #2f9e44;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🛍️ ShopImpact")
st.subheader("Track your shopping CO₂ impact")

st.divider()

# ---------------- INPUT SECTION ----------------
st.header("Log a Product")

product_name = st.text_input("Product name")
co2_value = st.number_input(
    "CO₂ Emissions (kg)",
    min_value=0.0,
    step=1.0
)

submit = st.button("Log Item")

# ---------------- LOGIC ----------------
if submit:
    st.success(f"✅ Logged **{product_name}** with **{co2_value} kg CO₂**")

    # Badge unlock condition (only once)
    if co2_value > 50 and not st.session_state.oopsie_unlocked:
        st.session_state.show_badge_popup = True
        st.session_state.oopsie_unlocked = True

# ---------------- BADGE POPUP ----------------
if st.session_state.show_badge_popup:
    st.markdown("""
    <div class="popup-overlay">
        <div class="popup-box">
            <div class="badge">🤡</div>
            <h1>BADGE UNLOCKED!</h1>
            <h3>Oopsie</h3>
            <p>Logged an item with <b>&gt; 50kg CO₂</b></p>
            <span class="special">SPECIAL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Close"):
            st.session_state.show_badge_popup = False
            st.rerun()

# ---------------- FOOTER ----------------
st.divider()
st.caption("🌱 Make smarter, eco-friendly choices with ShopImpact")
