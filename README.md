# 🍃 ShopImpact - Ultimate Streamlit Edition

**ShopImpact** is a gamified personal finance tool that tracks the **environmental cost** of shopping. It estimates carbon footprint, water usage, and tree loss for every purchase, encouraging sustainable habits through real-time visual feedback and badges.

## 🚀 Key Features

* **Real-Time Impact Tracking:** Calculates **CO₂**, **Water Wasted (L)**, and **Trees Cut** based on product category and price.
* **Gamification:** Unlocks badges (e.g., "👑 Thrift King", "🛡️ Eco Warrior") for hitting sustainability milestones.
* **Visual Feedback:** Triggers **Green Leaf** animations for eco-friendly choices and **Dry Leaf** drops for high-carbon items.
* **Eco-Nudging:** Suggests sustainable alternatives (e.g., "Try Refurbished") before a purchase is logged.
* **Analytics:** Interactive charts showing Spending vs. CO₂ trends, category breakdowns, and "Eco vs. Regular" comparisons.
* **Data Management:** Local data persistence with **CSV Export** and **Reset Data** capabilities.

## 🛠️ Installation & Setup

1.  **Prerequisites:**
    * Python 3.8+
    * pip

2.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas plotly
    ```

3.  **Run the App:**
    ```bash
    streamlit run app.py
    ```
    *(Replace `app.py` with your script's filename)*

4.  **Access:**
    Open `http://localhost:8501` in your browser.

## 📂 Files

* `app.py`: Main application code.
* `shopimpact_data_v3.json`: Auto-generated local database for user history.
* `shopimpact_data.csv`: Generated file when using the "Export" feature.

## 📊 Calculation Logic

* **Carbon (CO₂):** `(Price × Multiplier) / 100`
    * *Multipliers:* Fast Fashion (2.5), Electronics (1.8), Second-hand (0.1).
* **Water:** High intensity (150x) for Textiles/Meat; Standard (20x) for others.
* **Trees:** Applied to Paper, Furniture, and Wood-based categories.

---
*Built with [Streamlit](https://streamlit.io/)*
