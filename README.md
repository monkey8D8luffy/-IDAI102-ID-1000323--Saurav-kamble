# ShopImpact: A Computational Approach to Sustainable Consumerism

**Project Name:** ShopImpact
**Version:** 3.0 (Ultimate Streamlit Edition)
**Domain:** Personal Finance / Environmental Science
**Framework:** Python (Streamlit)

---

## 1. Project Overview

### 1.1 The Problem
Modern consumerism suffers from an information asymmetry: while the *financial cost* of a product is explicit, its *environmental cost*—measured in carbon emissions, water depletion, and deforestation—is largely invisible to the end-user at the point of purchase. This lack of immediate feedback contributes to unsustainable purchasing behaviors ("Fast Fashion" cycles, high-turnover electronics).

### 1.2 The Solution
**ShopImpact** is a data-driven application designed to bridge this gap. It functions as a "Conscious Shopping Companion" that utilizes heuristic algorithms to estimate the hidden environmental toll of purchases in real-time. By combining financial tracking with environmental metrics and gamification theory (positive/negative reinforcement), the application aims to modify user behavior toward sustainability.

---

## 2. System Architecture & Tech Stack

The application is built using a modular architecture to ensure scalability and maintainability.

* **Frontend & Logic Layer:** [Streamlit](https://streamlit.io/) (Python) - chosen for its rapid prototyping capabilities and seamless data integration.
* **Data Visualization:** [Plotly Express & Graph Objects](https://plotly.com/python/) - used for interactive, high-contrast analytics.
* **Data Persistence:** JSON-based local storage (`shopimpact_data_v3.json`) for session persistence without the overhead of a SQL server.
* **UI/UX Design:** Custom CSS injection implementing **Glassmorphism** (backdrop-filter effects) and CSS Keyframe animations to enhance user retention.

---

## 3. Algorithmic Logic & Computational Thinking

The core of ShopImpact relies on a **Weighted Multiplier Algorithm** to translate monetary value into environmental impact. This abstraction allows the system to estimate impact without requiring granular supply chain data for every unique SKU.

### 3.1 Carbon Footprint Estimation ($\text{CO}_2$)
The system uses price as a proxy for material volume and complexity, adjusted by a category-specific coefficient.

$$\text{Impact}_{CO2} = \frac{\text{Price} \times \mu_{category}}{100}$$

Where $\mu$ (Mu) represents the specific multiplier coefficient:
* **$\mu = 2.5$ (High Impact):** Applied to *Fast Fashion* due to rapid obsolescence and synthetic materials.
* **$\mu = 0.1$ (Low Impact):** Applied to *Second-Hand/Refurbished* goods to model the diversion of waste from landfills.
* **$\mu = 5.0$ (Critical Impact):** Applied to *Air Travel* due to high fuel combustion per capita.

### 3.2 The "Hidden Toll" Heuristics
Beyond Carbon, the system calculates secondary environmental metrics using conditional logic maps:

* **Water Usage Algorithm:**
    * *Condition:* If Category $\in$ {Textiles, Meat, Dairy}
    * *Calculation:* $\text{Water (L)} = \text{Base Impact} \times 150$
    * *Rationale:* Accounts for the high water footprint of cotton cultivation and livestock farming.

* **Deforestation Algorithm:**
    * *Condition:* If Category $\in$ {Furniture, Paper, Packaging}
    * *Calculation:* $\text{Trees Cut} = \text{Base Impact} \times 0.05$

---

## 4. Key Features & Functionality

### 4.1 Dashboard & Live Feedback
* **Dynamic Nudging Engine:** Uses conditional statements to intercept high-impact inputs. If a user selects "Fast Fashion," the system interrupts the workflow to suggest alternatives (e.g., "Consider Thrifted or Organic Cotton") before the data is committed.
* **Visual Reinforcement:**
    * *Positive Feedback:* Green Leaf Animation (CSS Keyframes) for Eco-choices.
    * *Negative Feedback:* Dry Leaf Drop Animation for high-carbon choices.

### 4.2 Analytics Suite
* **Comparative Analysis:** A distinct module comparing the user's "Eco-Friendly" vs. "High-Carbon" purchases side-by-side, visually demonstrating that similar financial spend can result in vastly different environmental outcomes.
* **Trend Analysis:** Temporal analysis of CO₂ emissions using area charts to track behavioral improvement over time.

### 4.3 Gamification System
To ensure user engagement, a badge system tracks cumulative logic states:
* **`Thrift King`:** Logic check for $>3$ items where `Category` is in `ECO_FRIENDLY_LIST`.
* **`Eco Warrior`:** Logic check for `Total_CO2 < Goal_Limit`.

---

## 5. Installation & Usage

### Prerequisites
* Python 3.8+
* pip package manager

### Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-repo/shopimpact.git](https://github.com/your-repo/shopimpact.git)
    cd shopimpact
    ```

2.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas plotly
    ```

3.  **Execute the Application:**
    ```bash
    streamlit run app.py
    ```

4.  **Local Data Management:**
    * The app generates a `shopimpact_data_v3.json` file in the root directory.
    * Users can **Export** their longitudinal data to CSV via the Profile tab.

---

## 6. Evaluation & Future Scope

### 6.1 Success Criteria Evaluation
The project successfully meets the criteria of providing a transparent, engaging interface for tracking environmental impact. The heuristic algorithms provide a reasonable approximation of impact, sufficient for behavioral modification.

### 6.2 Future Improvements
* **API Integration:** Replacing heuristic multipliers with real-time API calls to databases like *Climatiq* or *CarbonInterface* for industrial-grade accuracy.
* **OCR Implementation:** utilizing Computer Vision (Tesseract) to parse text from physical receipts, automating the data entry process.
* **Cloud Database:** Migrating from JSON flat-file storage to SQL (PostgreSQL) to support multi-user authentication.

---

**Academic Honesty Declaration:**
* *Libraries Used:* Streamlit (UI), Pandas (Data Processing), Plotly (Visualization).
* *Logic:* All environmental multipliers and gamification algorithms were self-authored based on research into average industry carbon intensities.

---
