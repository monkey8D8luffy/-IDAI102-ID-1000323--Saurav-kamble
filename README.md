# 🍃 ShopImpact - The Ultimate Conscious Shopping Companion

**ShopImpact** is a robust, gamified Streamlit application designed to bridge the gap between financial tracking and environmental awareness. By acting as a personal "Eco-Accountant," it visualizes the hidden costs of consumption—Carbon Emissions (CO₂), Water Usage, and Deforestation—in real-time.

---

##  Key Features

### 1.  Interactive Dashboard
* **Smart Entry System:** Logs purchases by Category, Brand, and Price.
* **Eco-Nudging:** Proactively intercepts high-carbon selections (e.g., Fast Fashion) to suggest sustainable alternatives (e.g., "Try Thrifted or Refurbished") before submission.
* **Real-Time Animation Engine:**
    * **Eco-Burst 🍃:** Triggers rising green leaves for sustainable choices.
    * **Carbon-Drop 🍂:** Triggers falling dry leaves for high-impact purchases.
* **"Hidden Toll" Metrics:** Displays estimates for **Water Wasted (Liters)** and **Trees Cut** alongside financial spend.

### 2. Advanced Analytics
* **Easy Insights:** A beginner-friendly view featuring a "Top 5 Polluters" bar chart and a simplified Carbon Trend line.
* **Comparative Analysis:** A dedicated "Eco vs. Regular" showdown that compares the environmental impact of your sustainable choices versus your high-carbon habits side-by-side.
* **Visual Clarity:** All charts are rendered using Plotly with high-contrast styling (black text/axes) for maximum readability.

### 3. Gamification & Profile
* **Badge System:** Automatically unlocks badges based on user behavior:
    * `🌱 First Step`: First log.
    * `👑 Thrift King`: 3+ second-hand items.
    * `🛡️ Eco Warrior`: Maintaining low CO₂ (< 50kg).
    * `💰 Big Saver`: High-value tracking.
* **Data Sovereignty:** Includes a dedicated **Data Management** section to Export history as CSV or Reset all data.

---

##  Technical Stack

* **Frontend Framework:** [Streamlit](https://streamlit.io/) (Python)
* **Data Visualization:** [Plotly Express & Graph Objects](https://plotly.com/python/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Styling:** Custom CSS injection for **Glassmorphism** (frosted glass effects), gradient buttons, and keyframe animations.
* **Persistence:** Local file-based storage using JSON (`shopimpact_data_v3.json`) to persist state between sessions.

---

##  Installation & Setup

### Prerequisites
* Python 3.8 or higher installed.

### Step-by-Step Guide

1.  **Clone the Repository** (or download the script):
    ```bash
    git clone [https://github.com/yourusername/shopimpact.git](https://github.com/yourusername/shopimpact.git)
    cd shopimpact
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas plotly
    ```

4.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

5.  **Access the App:**
    The app will automatically open in your default web browser at `http://localhost:8501`.

---

##  How It Works (The Algorithm)

The application uses a weighted multiplier logic to estimate environmental impact based on the **Price** (as a proxy for material volume/complexity) and **Category**.

### 1. Carbon (CO₂) Calculation
$$ \text{CO}_2 \text{ (kg)} = \frac{\text{Price} \times \text{Multiplier}}{100} $$
* **Multipliers:**
    * High Impact: Flight Tickets (5.0), Fast Fashion (2.5), Electronics (1.8).
    * Neutral: General Goods (1.0).
    * Eco-Friendly: Second-Hand/Refurbished (0.1), Organic/Local (0.3).

### 2. Water Usage Logic
* **Textiles & Meat:** Identified as high-intensity categories (e.g., Cotton, Jeans, Beef).
    * $$ \text{Water} = \text{Base Impact} \times 150 $$
* **Standard Goods:**
    * $$ \text{Water} = \text{Base Impact} \times 20 $$

### 3. Deforestation Logic
* **Wood & Paper:** Applied to categories like Furniture, Books, and Packaging.
    * $$ \text{Trees} = \text{Base Impact} \times 0.05 $$

---

## Project Structure

```text
ShopImpact/
├── app.py                   # Main application logic
├── shopimpact_data_v3.json  # (Auto-generated) Local database storing user history
├── shopimpact_data.csv      # (Auto-generated) Exported user data
└── README.md                # Project documentation
