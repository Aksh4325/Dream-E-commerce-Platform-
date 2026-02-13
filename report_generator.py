"""
Report Generator
Generate Excel and PDF reports with insights
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from datetime import datetime
import os


class ReportGenerator:
    """Generate comprehensive Excel and PDF reports"""
    
    def __init__(self, output_dir='reports'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def create_excel_report(self, db, sessions_df, funnel_analyzer):
        """Create comprehensive Excel report"""
        
        print("\n📊 Generating Excel Report...")
        
        filename = f'{self.output_dir}/ecommerce_analysis_report.xlsx'
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # Sheet 1: Executive Summary
            summary_data = self._create_executive_summary(db, sessions_df, funnel_analyzer)
            summary_data.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Sheet 2: Conversion Funnel
            funnel_data = db.get_conversion_funnel()
            funnel_data.to_excel(writer, sheet_name='Conversion Funnel', index=False)
            
            # Sheet 3: Traffic Source Performance
            traffic_data = db.get_traffic_source_performance()
            traffic_data.to_excel(writer, sheet_name='Traffic Sources', index=False)
            
            # Sheet 4: Device Performance
            device_data = db.get_device_performance()
            device_data.to_excel(writer, sheet_name='Device Performance', index=False)
            
            # Sheet 5: Daily Trends
            daily_data = db.get_daily_trends()
            daily_data.to_excel(writer, sheet_name='Daily Trends', index=False)
            
            # Sheet 6: Category Performance
            category_data = db.get_category_performance()
            category_data.to_excel(writer, sheet_name='Category Performance', index=False)
            
            # Sheet 7: Location Analysis
            location_data = db.get_location_analysis()
            location_data.to_excel(writer, sheet_name='Location Analysis', index=False)
            
            # Sheet 8: Cart Abandonment
            cart_data = db.get_cart_abandonment_rate()
            cart_data.to_excel(writer, sheet_name='Cart Abandonment', index=False)
            
            # Sheet 9: Hourly Patterns
            hourly_data = db.get_hourly_patterns()
            hourly_data.to_excel(writer, sheet_name='Hourly Patterns', index=False)
            
            # Sheet 10: Business Recommendations
            recommendations = self._generate_recommendations(db, funnel_analyzer)
            recommendations.to_excel(writer, sheet_name='Recommendations', index=False)
        
        print(f"✓ Excel report saved: {filename}")
        return filename
    
    def _create_executive_summary(self, db, sessions_df, funnel_analyzer):
        """Create executive summary data"""
        
        overall = db.get_overall_metrics()
        funnel_metrics = funnel_analyzer.calculate_funnel_metrics()
        
        summary = {
            'Metric': [
                'Analysis Period',
                'Total Sessions',
                'Unique Users',
                'Total Conversions',
                'Overall Conversion Rate',
                'Bounce Rate',
                'Cart Abandonment Rate',
                'Total Revenue',
                'Average Order Value',
                'Total Ad Spend',
                'Return on Investment (ROI)',
                'Revenue per Session',
                '',
                'Funnel Performance',
                'Landing → Product View',
                'Product View → Add to Cart',
                'Cart → Checkout',
                'Checkout → Purchase',
            ],
            'Value': [
                f"{sessions_df['date'].min()} to {sessions_df['date'].max()}",
                f"{overall['total_sessions'].values[0]:,}",
                f"{overall['unique_users'].values[0]:,}",
                f"{overall['conversions'].values[0]:,}",
                f"{overall['conversion_rate'].values[0]}%",
                f"{overall['bounce_rate'].values[0]}%",
                f"{funnel_analyzer.get_cart_abandonment_insights()['abandonment_rate']:.2f}%",
                f"₹{overall['total_revenue'].values[0]:,.2f}",
                f"₹{overall['total_revenue'].values[0] / overall['conversions'].values[0]:,.2f}",
                f"₹{overall['total_ad_spend'].values[0]:,.2f}",
                f"{overall['overall_roi'].values[0]}%",
                f"₹{overall['total_revenue'].values[0] / overall['total_sessions'].values[0]:.2f}",
                '',
                '',
                f"{funnel_metrics['landing_to_product_rate']:.2f}%",
                f"{funnel_metrics['product_to_cart_rate']:.2f}%",
                f"{funnel_metrics['cart_to_checkout_rate']:.2f}%",
                f"{funnel_metrics['checkout_to_purchase_rate']:.2f}%",
            ]
        }
        
        return pd.DataFrame(summary)
    
    def _generate_recommendations(self, db, funnel_analyzer):
        """Generate business recommendations"""
        
        bottlenecks = funnel_analyzer.identify_bottlenecks()
        traffic_data = db.get_traffic_source_performance()
        
        recommendations = []
        
        # Priority 1: Address major bottlenecks
        for i, bottleneck in enumerate(bottlenecks[:3], 1):
            recommendations.append({
                'Priority': f'P{i}',
                'Category': 'Conversion Optimization',
                'Issue': f"High drop-off at {bottleneck['stage']}",
                'Current Rate': f"{bottleneck['drop_off_rate']:.1f}% drop-off",
                'Recommendation': bottleneck['recommendation'],
                'Expected Impact': 'High' if bottleneck['severity'] in ['Critical', 'High'] else 'Medium'
            })
        
        # Priority 2: Optimize best performing channels
        best_channel = traffic_data.iloc[0]
        recommendations.append({
            'Priority': 'P4',
            'Category': 'Marketing Optimization',
            'Issue': 'Maximize high-performing channels',
            'Current Rate': f"{best_channel['conversion_rate']}% CR",
            'Recommendation': f"Increase budget for {best_channel['traffic_source']} (best ROI: {best_channel['roi_percent']}%)",
            'Expected Impact': 'High'
        })
        
        # Priority 3: Cart recovery
        cart_metrics = db.get_cart_abandonment_rate()
        abandonment = cart_metrics['abandonment_rate'].values[0]
        recommendations.append({
            'Priority': 'P5',
            'Category': 'Cart Recovery',
            'Issue': 'High cart abandonment',
            'Current Rate': f"{abandonment:.1f}% abandonment",
            'Recommendation': 'Implement cart recovery email campaigns within 1 hour and 24 hours of abandonment',
            'Expected Impact': 'High'
        })
        
        # Priority 4: Mobile optimization
        device_data = db.get_device_performance()
        mobile_data = device_data[device_data['device'] == 'Mobile']
        if len(mobile_data) > 0:
            mobile_cr = mobile_data['conversion_rate'].values[0]
            recommendations.append({
                'Priority': 'P6',
                'Category': 'Mobile Optimization',
                'Issue': 'Mobile conversion gap',
                'Current Rate': f"{mobile_cr}% mobile CR",
                'Recommendation': 'Optimize mobile checkout flow, implement one-click payment options',
                'Expected Impact': 'Medium'
            })
        
        # Priority 5: Customer retention
        recommendations.append({
            'Priority': 'P7',
            'Category': 'Customer Retention',
            'Issue': 'Increase repeat purchases',
            'Current Rate': 'Variable',
            'Recommendation': 'Launch loyalty program, send personalized product recommendations',
            'Expected Impact': 'Medium'
        })
        
        return pd.DataFrame(recommendations)
    
    def create_business_insights_doc(self, db, funnel_analyzer):
        """Create markdown document with business insights"""
        
        print("\n📄 Generating Business Insights Document...")
        
        filename = f'{self.output_dir}/business_insights.md'
        
        overall = db.get_overall_metrics()
        funnel_data = db.get_conversion_funnel()
        traffic_data = db.get_traffic_source_performance()
        bottlenecks = funnel_analyzer.identify_bottlenecks()
        
        content = f"""# E-Commerce Funnel Analysis - Business Insights
## Executive Summary Report
**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

## 📊 Key Performance Indicators

| Metric | Value |
|--------|-------|
| **Total Sessions** | {overall['total_sessions'].values[0]:,} |
| **Conversions** | {overall['conversions'].values[0]:,} |
| **Conversion Rate** | {overall['conversion_rate'].values[0]}% |
| **Bounce Rate** | {overall['bounce_rate'].values[0]}% |
| **Total Revenue** | ₹{overall['total_revenue'].values[0]:,.2f} |
| **ROI** | {overall['overall_roi'].values[0]}% |

---

## 🎯 Conversion Funnel Analysis

### Funnel Performance
"""
        
        for _, row in funnel_data.iterrows():
            content += f"- **{row['stage']}**: {row['users']:,} users ({row['percentage']}%)\n"
            if row['drop_off'] > 0:
                content += f"  - Drop-off: {row['drop_off']}%\n"
        
        content += f"""

### Overall Conversion Rate: {overall['conversion_rate'].values[0]}%

---

## ⚠️ Critical Bottlenecks Identified

"""
        
        for i, bottleneck in enumerate(bottlenecks, 1):
            content += f"""
### {i}. {bottleneck['stage']}
- **Drop-off Rate:** {bottleneck['drop_off_rate']:.1f}%
- **Severity:** {bottleneck['severity']}
- **Recommendation:** {bottleneck['recommendation']}

"""
        
        content += """---

## 📈 Traffic Source Performance

"""
        
        for _, row in traffic_data.iterrows():
            content += f"""
### {row['traffic_source']}
- Sessions: {row['sessions']:,}
- Conversion Rate: {row['conversion_rate']}%
- ROI: {row['roi_percent']}%
- Revenue: ₹{row['total_revenue']:,.2f}

"""
        
        content += """---

## 💡 Strategic Recommendations

### Immediate Actions (Week 1-2)

1. **Simplify Checkout Process**
   - Reduce checkout steps from current flow to 2-step process
   - Implement guest checkout option
   - Add trust badges and security indicators
   - **Expected Impact:** 15-20% improvement in checkout conversion

2. **Launch Cart Recovery Campaign**
   - Set up automated emails at 1 hour and 24 hours post-abandonment
   - Include discount incentive (5-10%)
   - Highlight items left in cart with product images
   - **Expected Impact:** Recover 10-15% of abandoned carts

3. **Optimize Mobile Experience**
   - A/B test mobile checkout flow
   - Implement mobile-friendly payment options (Apple Pay, Google Pay)
   - Reduce form fields on mobile
   - **Expected Impact:** 20-25% improvement in mobile conversion

### Short-term Actions (Month 1-2)

4. **Increase Investment in Best Channels**
"""
        
        best_channel = traffic_data.iloc[0]
        content += f"""   - Scale up {best_channel['traffic_source']} (Current CR: {best_channel['conversion_rate']}%, ROI: {best_channel['roi_percent']}%)
   - Reallocate budget from underperforming channels
   - **Expected Impact:** 25-30% revenue increase

5. **Implement Personalization**
   - Product recommendations based on browsing history
   - Personalized email campaigns
   - Dynamic homepage content
   - **Expected Impact:** 10-15% increase in conversion rate

### Long-term Actions (Quarter 1-2)

6. **Launch Loyalty Program**
   - Points-based rewards system
   - Exclusive offers for repeat customers
   - Referral incentives
   - **Expected Impact:** 20% increase in customer lifetime value

7. **Enhance Product Pages**
   - Add customer reviews and ratings
   - Include detailed product videos
   - Implement AR/Virtual try-on where applicable
   - **Expected Impact:** 15-20% reduction in product page bounce rate

---

## 📊 Success Metrics to Track

### Weekly KPIs
- Conversion Rate (Target: >16%)
- Cart Abandonment Rate (Target: <60%)
- Checkout Completion Rate (Target: >75%)
- Revenue per Session (Target: Increase by 20%)

### Monthly KPIs
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Return on Ad Spend (ROAS)
- Repeat Purchase Rate

---

## 🎯 Expected Outcomes (3-Month Projection)

If all recommendations are implemented:

1. **Conversion Rate:** 14% → 18-20% (+30% improvement)
2. **Cart Abandonment:** 65% → 50% (-23% reduction)
3. **Revenue:** Current → +35-40% increase
4. **ROI:** Current → +25-30% improvement

---

## 📞 Next Steps

1. **Week 1:** Implement checkout simplification
2. **Week 2:** Launch cart recovery emails
3. **Week 3:** Mobile optimization rollout
4. **Week 4:** Increase top channel budget
5. **Month 2:** Full personalization launch
6. **Month 3:** Review results and iterate

---

**Report Prepared By:** Data Analytics Team  
**Contact:** analytics@ecommerce.com  
**Review Date:** {datetime.now().strftime('%B %d, %Y')}

---

*This analysis is based on {overall['total_sessions'].values[0]:,} sessions over the analysis period. All recommendations are data-driven and based on industry best practices.*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Business insights saved: {filename}")
        return filename
    
    def create_sql_queries_file(self):
        """Save all SQL queries to a file"""
        
        filename = f'{self.output_dir}/analytical_queries.sql'
        
        queries = """-- E-Commerce Analytics SQL Queries
-- Database: SQLite
-- Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

-- =====================================================
-- QUERY 1: Overall Metrics
-- =====================================================
SELECT 
    COUNT(DISTINCT session_id) as total_sessions,
    COUNT(DISTINCT user_id) as unique_users,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate,
    ROUND(SUM(CASE WHEN bounced = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as bounce_rate,
    ROUND(SUM(revenue), 2) as total_revenue
FROM sessions;

-- =====================================================
-- QUERY 2: Conversion Funnel
-- =====================================================
SELECT 
    'Landing Page' as stage,
    COUNT(*) as users,
    100.0 as percentage
FROM sessions

UNION ALL

SELECT 
    'Product View' as stage,
    SUM(CASE WHEN viewed_product = 1 THEN 1 ELSE 0 END) as users,
    ROUND(SUM(CASE WHEN viewed_product = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage
FROM sessions

UNION ALL

SELECT 
    'Add to Cart' as stage,
    SUM(CASE WHEN added_to_cart = 1 THEN 1 ELSE 0 END) as users,
    ROUND(SUM(CASE WHEN added_to_cart = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage
FROM sessions

UNION ALL

SELECT 
    'Checkout Started' as stage,
    SUM(CASE WHEN started_checkout = 1 THEN 1 ELSE 0 END) as users,
    ROUND(SUM(CASE WHEN started_checkout = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage
FROM sessions

UNION ALL

SELECT 
    'Purchase Complete' as stage,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as users,
    ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage
FROM sessions;

-- =====================================================
-- QUERY 3: Cart Abandonment Rate
-- =====================================================
SELECT 
    COUNT(CASE WHEN added_to_cart = 1 THEN 1 END) as carts_created,
    COUNT(CASE WHEN added_to_cart = 1 AND completed_purchase = 0 THEN 1 END) as carts_abandoned,
    ROUND(COUNT(CASE WHEN added_to_cart = 1 AND completed_purchase = 0 THEN 1 END) * 100.0 / 
          COUNT(CASE WHEN added_to_cart = 1 THEN 1 END), 2) as abandonment_rate
FROM sessions;

-- =====================================================
-- QUERY 4: Traffic Source Performance
-- =====================================================
SELECT 
    traffic_source,
    COUNT(*) as sessions,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND((SUM(revenue) - SUM(ad_spend)) / NULLIF(SUM(ad_spend), 0) * 100, 2) as roi_percent
FROM sessions
GROUP BY traffic_source
ORDER BY total_revenue DESC;

-- =====================================================
-- QUERY 5: Device Performance
-- =====================================================
SELECT 
    device,
    COUNT(*) as sessions,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate,
    ROUND(SUM(revenue), 2) as total_revenue
FROM sessions
GROUP BY device
ORDER BY sessions DESC;

-- =====================================================
-- QUERY 6: Hourly Traffic Patterns
-- =====================================================
SELECT 
    hour,
    COUNT(*) as sessions,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate
FROM sessions
GROUP BY hour
ORDER BY hour;

-- =====================================================
-- QUERY 7: Category Performance
-- =====================================================
SELECT 
    category,
    COUNT(*) as sessions,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND(AVG(CASE WHEN completed_purchase = 1 THEN revenue ELSE NULL END), 2) as avg_order_value
FROM sessions
GROUP BY category
ORDER BY total_revenue DESC;

-- =====================================================
-- QUERY 8: New vs Returning Customers
-- =====================================================
SELECT 
    CASE WHEN is_returning = 1 THEN 'Returning' ELSE 'New' END as customer_type,
    COUNT(*) as sessions,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate,
    ROUND(SUM(revenue), 2) as total_revenue
FROM sessions
GROUP BY is_returning;

-- =====================================================
-- QUERY 9: Daily Trends
-- =====================================================
SELECT 
    date,
    COUNT(*) as sessions,
    SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(revenue), 2) as revenue
FROM sessions
GROUP BY date
ORDER BY date;

-- =====================================================
-- QUERY 10: Checkout Drop-off Analysis
-- =====================================================
SELECT 
    'Reached Checkout' as stage,
    COUNT(CASE WHEN started_checkout = 1 THEN 1 END) as users
FROM sessions

UNION ALL

SELECT 
    'Completed Purchase' as stage,
    COUNT(CASE WHEN completed_purchase = 1 THEN 1 END) as users
FROM sessions;
"""
        
        with open(filename, 'w') as f:
            f.write(queries)
        
        print(f"✓ SQL queries saved: {filename}")
        return filename
