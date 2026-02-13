# 🚀 Setup Guide - E-Commerce Funnel Analytics

## Complete Installation & Usage Instructions

---

## 📋 Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (optional, for cloning)
- **4GB RAM minimum**
- **500MB free disk space**

---

## 🔧 Installation Steps

### Step 1: Download Project

**Option A: Git Clone**
```bash
git clone https://github.com/yourusername/ecommerce-funnel-analytics.git
cd ecommerce-funnel-analytics
```

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to your desired location
3. Open terminal/command prompt in the extracted folder

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib (static charts)
- seaborn (statistical visualizations)
- plotly (interactive charts)
- openpyxl (Excel generation)
- kaleido (chart export)

### Step 4: Verify Installation

```bash
python -c "import pandas, plotly, matplotlib; print('✓ All packages installed!')"
```

---

## 🎯 Quick Start Guide

### Option 1: Complete Analysis (Recommended for First Run)

```bash
python main.py
```

**In the menu, select:**
- **Option 11: "Run Complete Analysis"**

This will:
1. Generate 15,000 sessions (takes ~30 seconds)
2. Load data into SQLite
3. Run all SQL queries
4. Create 14 visualizations
5. Generate Excel report
6. Create business insights document

**Total time:** ~2-3 minutes

### Option 2: Step-by-Step Exploration

```bash
python main.py
```

**Try these menu options in order:**
1. **Option 1:** Generate Data
2. **Option 2:** Load to Database
3. **Option 3:** View Overall Metrics
4. **Option 4:** Analyze Conversion Funnel
5. **Option 5:** Traffic Source Analysis
6. **Option 7:** Generate Visualizations
7. **Option 8:** Create Excel Report

---

## 📊 Understanding the Output

### 1. Generated Data Files

**Location:** `data/`

- `sessions_data.csv` - 15,000 session records
  - Columns: session_id, user_id, timestamp, traffic_source, device, revenue, etc.
  
- `events_data.csv` - Event-level tracking
  - Columns: event_id, session_id, event_type, timestamp, page

### 2. Database

**Location:** `database/ecommerce.db`

SQLite database with 2 tables:
- `sessions` - Main session data
- `events` - User event tracking

**Accessing the database:**
```bash
sqlite3 database/ecommerce.db
.tables
SELECT * FROM sessions LIMIT 5;
```

### 3. Visualizations

**Location:** `output/`

**Interactive HTML charts (open in browser):**
- `conversion_funnel.html` - Funnel visualization
- `traffic_sources.html` - Traffic breakdown
- `cart_abandonment_trend.html` - Time series
- `traffic_roi.html` - ROI analysis
- `conversion_trends.html` - Daily trends
- `customer_segmentation.html` - New vs returning
- `location_performance.html` - Geographic analysis
- `session_duration_analysis.html` - Duration boxplots
- `kpi_dashboard.html` - KPI summary table
- And more...

**Static PNG images:**
- `conversion_funnel.png`
- `hourly_heatmap.png`
- `revenue_by_category.png`
- `weekday_performance.png`
- `revenue_distribution.png`

### 4. Reports

**Location:** `reports/`

**Excel Report:** `ecommerce_analysis_report.xlsx`
- 10 sheets with comprehensive analysis
- Professional formatting
- Charts and tables
- Business recommendations

**Business Insights:** `business_insights.md`
- Markdown format
- Executive summary
- Detailed recommendations
- Implementation timeline

**SQL Queries:** `analytical_queries.sql`
- All 15+ queries documented
- Copy-paste ready
- Includes comments

---

## 💻 Menu Options Explained

### Main Menu

```
1. Generate Data
   → Creates 15,000 synthetic e-commerce sessions
   → Realistic behavior patterns
   → Takes ~30 seconds

2. Load Data into Database
   → Imports CSV files into SQLite
   → Creates database schema
   → Takes ~10 seconds

3. View Overall Metrics
   → Shows KPIs: sessions, conversions, revenue, ROI
   → Bounce rate, conversion rate
   → Average session duration

4. Analyze Conversion Funnel
   → 5-stage funnel breakdown
   → Drop-off percentages
   → Cart abandonment metrics

5. Traffic Source Analysis
   → Performance by source (Google Ads, Facebook, etc.)
   → ROI comparison
   → Best/worst performers

6. Cart Abandonment Analysis
   → Detailed cart abandonment breakdown
   → By traffic source and device
   → Potential revenue loss

7. Generate All Visualizations
   → Creates all 14 charts
   → Both HTML (interactive) and PNG
   → Takes ~1-2 minutes

8. Create Excel Report
   → Comprehensive 10-sheet Excel file
   → Professional formatting
   → Charts and recommendations

9. Generate Business Insights
   → Markdown document with insights
   → SQL queries file
   → Actionable recommendations

10. View All SQL Queries
    → Lists all analytical queries used
    → Reference for documentation

11. Run Complete Analysis
    → End-to-end pipeline
    → All steps automated
    → Complete in 2-3 minutes

12. Exit
    → Close application
```

---

## 🔍 Exploring the Analysis

### Viewing HTML Charts

1. Navigate to `output/` folder
2. Double-click any `.html` file
3. Opens in default browser
4. Interactive - hover, zoom, pan

### Opening Excel Report

1. Go to `reports/` folder
2. Open `ecommerce_analysis_report.xlsx`
3. Explore different sheets
4. View charts and tables

### Reading Business Insights

1. Go to `reports/` folder
2. Open `business_insights.md` in any text editor
3. Or view on GitHub for formatted display
4. Contains all recommendations

---

## 🛠️ Customization

### Modify Number of Sessions

Edit `main.py` or run directly:

```python
from src.data_generator import EcommerceDataGenerator

# Generate 50,000 sessions instead of 15,000
generator = EcommerceDataGenerator(num_sessions=50000)
sessions_df = generator.generate_sessions()
```

### Change Conversion Rates

Edit `src/data_generator.py`:

```python
self.conversion_rates = {
    'Google Ads': 0.20,      # Increase from 0.18
    'Facebook Ads': 0.18,    # Increase from 0.15
    'Organic Search': 0.20,  # Increase from 0.16
    # ...
}
```

### Add Custom SQL Query

Edit `src/database.py`:

```python
def get_custom_metric(self):
    query = """
    SELECT 
        category,
        AVG(revenue) as avg_revenue
    FROM sessions
    WHERE completed_purchase = 1
    GROUP BY category
    """
    return pd.read_sql_query(query, self.conn)
```

Then use in `main.py`:
```python
custom_data = db.get_custom_metric()
print(custom_data)
```

---

## ⚠️ Troubleshooting

### Issue: ModuleNotFoundError

**Error:** `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Permission Denied (Database)

**Error:** `PermissionError: [Errno 13] Permission denied: 'database/ecommerce.db'`

**Solution:**
```bash
# Delete existing database
rm database/ecommerce.db  # macOS/Linux
del database\ecommerce.db  # Windows

# Recreate
python main.py
# Select Option 2
```

### Issue: Charts Not Displaying

**Error:** Blank HTML files

**Solution:**
```bash
# Install kaleido for chart export
pip install kaleido==0.2.1
```

### Issue: Slow Performance

**Problem:** Takes too long to generate data

**Solution:**
```python
# Reduce session count in data_generator.py
generator = EcommerceDataGenerator(num_sessions=5000)
```

---

## 📊 Sample Output

### Console Output Example

```
======================================================================
E-COMMERCE FUNNEL & CONVERSION ANALYTICS
======================================================================

Generating 15000 e-commerce sessions...
  Generated 1000 sessions...
  Generated 2000 sessions...
  ...
  Generated 15000 sessions...
✓ Generated 15000 sessions successfully!

Generating event-level data...
✓ Generated 42350 events!

✓ Data saved:
  - data/sessions_data.csv
  - data/events_data.csv

======================================================================
QUICK STATISTICS
======================================================================
Total Sessions: 15,000
Total Events: 42,350
Unique Users: 10,500
Conversions: 2,100
Conversion Rate: 14.00%
Total Revenue: ₹4,725,000.00
======================================================================
```

---

## 🎯 Best Practices

### For Presentation

1. **Run Complete Analysis** (Option 11) before demo
2. **Keep these files ready:**
   - Excel report (`reports/ecommerce_analysis_report.xlsx`)
   - Business insights (`reports/business_insights.md`)
   - 2-3 key visualizations from `output/`

3. **Demo Flow:**
   - Show overall metrics (Option 3)
   - Explain funnel (Option 4)
   - Show visualizations (open HTML files)
   - Walk through Excel report
   - Discuss recommendations from insights doc

### For Portfolio

1. **Upload to GitHub:**
   - Include all code files
   - Add sample visualizations to README
   - Remove generated data files (too large)
   - Keep `.gitignore` to exclude data/

2. **Create Screenshots:**
   - Terminal output
   - Interactive charts
   - Excel report sheets
   - Add to README

3. **Write Blog Post:**
   - Explain methodology
   - Share key findings
   - Include visualizations
   - Link to GitHub repo

---

## 📚 Further Learning

### Extending the Project

**1. Add Real-Time Dashboard**
```bash
pip install streamlit
```

Create `dashboard.py`:
```python
import streamlit as st
import pandas as pd

st.title("E-Commerce Analytics Dashboard")
df = pd.read_csv('data/sessions_data.csv')
st.dataframe(df.head())
```

Run: `streamlit run dashboard.py`

**2. Connect to Real Database**

Replace SQLite with PostgreSQL:
```python
# In database.py
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="ecommerce",
    user="your_user",
    password="your_pass"
)
```

**3. Add Machine Learning**

Predict conversion probability:
```python
from sklearn.ensemble import RandomForestClassifier

X = df[['session_duration_seconds', 'pages_viewed']]
y = df['completed_purchase']

model = RandomForestClassifier()
model.fit(X, y)
```

---

## 📞 Support

### Getting Help

**Email:** akshay.tiwari@example.com

**Common Questions:**
1. How do I change the number of sessions?
   → Edit `num_sessions` in `data_generator.py`

2. Can I use real data instead of synthetic?
   → Yes! Replace CSV files in `data/` with your own

3. How do I export charts as images?
   → PNG files are auto-generated in `output/`

4. Can I modify the SQL queries?
   → Yes! Edit methods in `src/database.py`

---

## ✅ Pre-Submission Checklist

Before submitting/presenting:

- [ ] All dependencies installed
- [ ] Complete analysis runs without errors
- [ ] All visualizations generated
- [ ] Excel report created successfully
- [ ] Business insights document complete
- [ ] SQL queries file present
- [ ] README updated with your info
- [ ] Screenshots added (optional)
- [ ] GitHub repository created (optional)
- [ ] Practiced presentation

---

## 🎓 Project Timeline

**Recommended workflow:**

- **Week 1:** Setup, understand code structure
- **Week 2:** Run analysis, explore visualizations
- **Week 3:** Customize, add features
- **Week 4:** Prepare presentation, documentation

**Minimum viable:** Can be completed in 1 day!

---

## 📝 Citation

If using this project:

```
E-Commerce Funnel Analytics
Author: Akshay Tiwari
Year: 2026
Institution: [Your College Name]
```

---

**Ready to start? Run:** `python main.py`

**© 2026 Akshay Tiwari. All Rights Reserved.**
