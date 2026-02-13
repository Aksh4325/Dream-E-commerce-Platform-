# 🛒 E-Commerce Funnel & Conversion Analytics

A comprehensive data analytics project analyzing e-commerce website funnel performance, conversion metrics, and user behavior using SQL, Python, and interactive visualizations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![SQL](https://img.shields.io/badge/SQL-SQLite-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📊 Project Overview

This project analyzes **~15,000 e-commerce sessions** to identify conversion bottlenecks, optimize marketing spend, and provide actionable business recommendations. Built as a college-level data analytics portfolio project showcasing advanced SQL, Python analytics, and data visualization skills.

### Key Achievements
- ✅ **14% Overall Conversion Rate** identified
- ✅ **30% Checkout Drop-off** - Critical bottleneck found
- ✅ **65% Cart Abandonment Rate** - Major opportunity area
- ✅ **15+ SQL Analytical Queries** for deep insights
- ✅ **14 Interactive Visualizations** created
- ✅ **ROI Analysis** across all traffic sources

---

## 🎯 Business Problem

E-commerce websites lose potential revenue at every stage of the customer journey. This project:
- Identifies where users drop off in the conversion funnel
- Analyzes which traffic sources provide best ROI
- Measures cart abandonment and checkout completion rates
- Provides data-driven recommendations to improve conversion

---

## 💻 Tech Stack

```
Data Generation:  Python (Pandas, NumPy, Faker)
Database:         SQLite
Analytics:        Python (Pandas, NumPy)
Visualization:    Matplotlib, Seaborn, Plotly
Reports:          Excel (openpyxl), Markdown
SQL:              15+ Complex Queries
```

---

## 📂 Project Structure

```
ecommerce-funnel-analytics/
│
├── data/
│   ├── sessions_data.csv      # 15,000 session records
│   └── events_data.csv         # Event-level tracking
│
├── database/
│   └── ecommerce.db            # SQLite database
│
├── src/
│   ├── data_generator.py       # Generate realistic data
│   ├── database.py             # SQL operations (15+ queries)
│   ├── funnel_analysis.py      # Conversion funnel analytics
│   ├── visualization.py        # 14 chart types
│   └── report_generator.py     # Excel & business reports
│
├── output/
│   ├── *.html                  # Interactive Plotly charts
│   └── *.png                   # Static chart images
│
├── reports/
│   ├── ecommerce_analysis_report.xlsx
│   ├── business_insights.md
│   └── analytical_queries.sql
│
├── main.py                     # Main application
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ecommerce-funnel-analytics.git
cd ecommerce-funnel-analytics

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python main.py
```

### One-Click Complete Analysis

```bash
# Run full pipeline
python main.py
# Select option 11: "Run Complete Analysis"
```

This will:
1. Generate 15,000 realistic session records
2. Load data into SQLite database
3. Run all 15+ SQL queries
4. Create 14 visualizations
5. Generate Excel report
6. Create business insights document

---

## 📊 Key Features

### 1. **Conversion Funnel Analysis**
- Track users through 5 stages: Landing → Product → Cart → Checkout → Purchase
- Identify drop-off points at each stage
- Calculate stage-wise conversion rates
- Visualize funnel with waterfall charts

**Funnel Stages:**
```
Landing Page     → 15,000 users (100%)
Product View     → 9,750 users (65%)
Add to Cart      → 5,250 users (35%)
Checkout Started → 3,000 users (20%)
Purchase         → 2,100 users (14%)
```

### 2. **Cart Abandonment Analysis**
- **65% abandonment rate** identified
- Breakdown by traffic source and device
- Time-based abandonment patterns
- Potential revenue recovery estimation

### 3. **Traffic Source Performance**
15+ metrics per source including:
- Conversion rate
- ROI (Return on Investment)
- Revenue per session
- Bounce rate
- Cost per acquisition

**Top Performers:**
1. Email Campaign: 20% CR, 150% ROI
2. Google Ads: 18% CR, 120% ROI
3. Organic Search: 16% CR, 400% ROI

### 4. **SQL Analytics (15+ Queries)**

#### Query Examples:

**Overall Metrics:**
```sql
SELECT 
    COUNT(*) as total_sessions,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 END) as conversions,
    ROUND(SUM(revenue), 2) as total_revenue
FROM sessions;
```

**Conversion Funnel:**
```sql
SELECT 
    stage,
    COUNT(DISTINCT user_id) as users,
    percentage
FROM funnel_stages
ORDER BY stage;
```

**Cart Abandonment:**
```sql
SELECT 
    COUNT(CASE WHEN added_to_cart = 1 AND completed_purchase = 0 THEN 1 END) * 100.0 /
    COUNT(CASE WHEN added_to_cart = 1 THEN 1 END) as abandonment_rate
FROM sessions;
```

**Complete query list:** `reports/analytical_queries.sql`

### 5. **Interactive Visualizations (14 Charts)**

1. **Conversion Funnel** - Interactive waterfall chart
2. **Traffic Source Breakdown** - Pie chart with drill-down
3. **Cart Abandonment Trend** - Time series
4. **Hourly Heatmap** - Session patterns by day/hour
5. **Device Performance** - Mobile vs Desktop vs Tablet
6. **Revenue by Category** - Bar chart
7. **Traffic ROI Analysis** - Comparative bar chart
8. **Daily Conversion Trends** - Dual-axis chart
9. **Weekday Performance** - Sessions & revenue
10. **Customer Segmentation** - New vs Returning
11. **Revenue Distribution** - Histogram
12. **Location Performance** - Geographic breakdown
13. **Session Duration Analysis** - Box plots
14. **KPI Dashboard** - Summary table

**All charts available in:** `output/` directory

---

## 📈 Key Insights & Findings

### Critical Bottlenecks Identified

1. **Checkout Drop-off (30%)** - CRITICAL
   - Severity: High
   - Impact: ~900 lost conversions
   - Recommendation: Simplify checkout to 2 steps

2. **Cart Abandonment (65%)** - HIGH
   - Severity: High
   - Potential Revenue Loss: ₹2.5M+
   - Recommendation: Implement recovery emails

3. **Product to Cart (46% drop)** - MEDIUM
   - Recommendation: Improve product pages, add reviews

### Performance Highlights

✅ **Best Traffic Source:** Email campaigns (20% CR, 150% ROI)  
✅ **Peak Hours:** 8 PM - 10 PM (highest conversion)  
✅ **Best Day:** Sunday (18% CR)  
✅ **Top Category:** Electronics (₹1.2M revenue)

---

## 💡 Business Recommendations

### Immediate Actions (Week 1-2)

**1. Simplify Checkout**
- Reduce from 4 steps to 2
- Add guest checkout option
- Expected Impact: +15-20% checkout conversion

**2. Cart Recovery Campaign**
- Send email at 1hr and 24hr post-abandonment
- Include 5-10% discount
- Expected Impact: Recover 10-15% of carts

**3. Mobile Optimization**
- Implement Apple Pay/Google Pay
- Expected Impact: +20% mobile conversion

### Short-term (Month 1-2)

**4. Scale Best Channels**
- Increase Email & Google Ads budget by 30%
- Expected Impact: +25-30% revenue

**5. Product Page Enhancement**
- Add customer reviews
- Include product videos
- Expected Impact: +15% product-to-cart rate

### Long-term (Quarter 1-2)

**6. Loyalty Program**
- Points-based rewards
- Expected Impact: +20% CLV

**7. Personalization Engine**
- AI-powered recommendations
- Expected Impact: +15% overall conversion

---

## 📊 Expected Outcomes (3-Month Projection)

If all recommendations implemented:

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Conversion Rate | 14% | 18-20% | +30% |
| Cart Abandonment | 65% | 50% | -23% |
| Revenue | Baseline | +35-40% | +₹5M+ |
| ROI | Current | +25-30% | Significant |

---

## 📁 Generated Reports

### 1. Excel Report (`reports/ecommerce_analysis_report.xlsx`)

10 sheets with comprehensive analysis:
- Executive Summary
- Conversion Funnel
- Traffic Sources
- Device Performance
- Daily Trends
- Category Performance
- Location Analysis
- Cart Abandonment
- Hourly Patterns
- Business Recommendations

### 2. Business Insights (`reports/business_insights.md`)

Markdown document with:
- Executive summary
- KPI dashboard
- Critical bottlenecks
- Detailed recommendations
- Success metrics
- Implementation timeline

### 3. SQL Queries (`reports/analytical_queries.sql`)

All 15+ SQL queries documented with:
- Query purpose
- Expected output
- Business context

---

## 🎓 Academic Value

This project demonstrates:

✅ **Data Engineering** - Generate & structure realistic data  
✅ **Database Design** - SQLite schema & normalization  
✅ **SQL Proficiency** - Complex queries, CTEs, window functions  
✅ **Python Analytics** - Pandas, NumPy, statistical analysis  
✅ **Data Visualization** - 14 chart types (static & interactive)  
✅ **Business Analysis** - Convert data to insights  
✅ **Report Generation** - Professional Excel & PDF reports  
✅ **Documentation** - Clear, comprehensive docs

---

## 🔧 Customization

### Modify Data Generation

Edit `src/data_generator.py`:
```python
# Change number of sessions
generator = EcommerceDataGenerator(num_sessions=20000)

# Adjust conversion rates
self.conversion_rates = {
    'Google Ads': 0.20,  # Increase from 0.18
    # ...
}
```

### Add New SQL Queries

Edit `src/database.py`:
```python
def get_custom_analysis(self):
    query = """
    SELECT ... FROM sessions
    """
    return pd.read_sql_query(query, self.conn)
```

### Create New Visualizations

Edit `src/visualization.py`:
```python
def plot_custom_chart(self, data):
    # Your plotting code
    pass
```

---

## 📊 Sample Output

### Console Output
```
===============================================================
E-COMMERCE FUNNEL & CONVERSION ANALYTICS
===============================================================

📊 Key Performance Indicators:

Total Sessions:        15,000
Unique Users:          10,500
Conversions:           2,100
Conversion Rate:       14.0%
Bounce Rate:           38.5%

💰 Revenue Metrics:

Total Revenue:         ₹4,725,000
Total Ad Spend:        ₹315,000
ROI:                   1,400%

🎯 Conversion Funnel Breakdown:

Landing Page         : 15,000 users (100.0%)
Product View         :  9,750 users ( 65.0%)
  ⚠️  Drop-off: 35.0%
Add to Cart          :  5,250 users ( 35.0%)
  ⚠️  Drop-off: 46.2%
Checkout Started     :  3,000 users ( 20.0%)
  ⚠️  Drop-off: 42.9%
Purchase Complete    :  2,100 users ( 14.0%)
  ⚠️  Drop-off: 30.0%
```

---

## 🤝 Contributing

This is a college academic project, but feedback is welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/Enhancement`)
3. Commit changes (`git commit -m 'Add enhancement'`)
4. Push to branch (`git push origin feature/Enhancement`)
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Developer

**Akshay Tiwari**
- Data Analyst | Python Developer 
- Email: tiwariaksh25@gmail.com

**Ayush patidar**
- Web Developer | Software Tester 
- Email: ayushpatidar@gmail.com

---

## 🎓 Academic Information

**Institution:** Medicaps University
**Program:** Data Analytics / Data Science  
**Year:** 2023-2025
**Project Type:** Final Year Project

---

## 🙏 Acknowledgments

- Python community for amazing libraries
- SQLite for lightweight database
- Plotly for interactive visualizations
- College professors for guidance

---

## 📞 Support

For questions or issues:
- 📧 Email: Medicaps@enquiry.com
- 🐛 GitHub Issues: [Create Issue]
- 📖 Documentation: See setup guides

---

**© 2025 Akshay Tiwari | Aayush Patidar. All Rights Reserved.**

*Built with 💙 for data analytics*
