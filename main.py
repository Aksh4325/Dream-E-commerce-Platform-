"""
E-Commerce Funnel Analytics
Main Application
"""

import sys
import os

# Add src to path
sys.path.append('src')

from data_generator import EcommerceDataGenerator
from database import EcommerceDatabase
from funnel_analysis import FunnelAnalyzer
from visualization import EcommerceVisualizer
from report_generator import ReportGenerator


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def print_section(text):
    """Print section header"""
    print("\n" + "-" * 70)
    print(text)
    print("-" * 70)


def display_menu():
    """Display main menu"""
    print("\n" + "=" * 70)
    print("E-COMMERCE FUNNEL & CONVERSION ANALYTICS".center(70))
    print("=" * 70)
    print("\n1. Generate Data (15,000 sessions)")
    print("2. Load Data into Database")
    print("3. View Overall Metrics")
    print("4. Analyze Conversion Funnel")
    print("5. Traffic Source Analysis")
    print("6. Cart Abandonment Analysis")
    print("7. Generate All Visualizations")
    print("8. Create Excel Report")
    print("9. Generate Business Insights")
    print("10. View All SQL Queries")
    print("11. Run Complete Analysis")
    print("12. Exit")
    print("=" * 70)


def generate_data():
    """Generate e-commerce data"""
    print_header("DATA GENERATION")
    
    generator = EcommerceDataGenerator(num_sessions=15000)
    sessions_df = generator.generate_sessions()
    events_df = generator.generate_event_log(sessions_df)
    generator.save_data(sessions_df, events_df)
    
    print("\n✓ Data generation complete!")
    input("\nPress Enter to continue...")
    return sessions_df, events_df


def load_data_to_database():
    """Load data into SQLite database"""
    print_header("DATABASE LOADING")
    
    db = EcommerceDatabase()
    db.connect()
    db.create_tables()
    db.load_data('data/sessions_data.csv', 'data/events_data.csv')
    
    print("\n✓ Data loaded into database successfully!")
    input("\nPress Enter to continue...")
    return db


def view_overall_metrics(db):
    """Display overall metrics"""
    print_header("OVERALL PERFORMANCE METRICS")
    
    metrics = db.get_overall_metrics()
    
    print("\n📊 Key Performance Indicators:\n")
    print(f"Total Sessions:        {metrics['total_sessions'].values[0]:,}")
    print(f"Unique Users:          {metrics['unique_users'].values[0]:,}")
    print(f"Conversions:           {metrics['conversions'].values[0]:,}")
    print(f"Conversion Rate:       {metrics['conversion_rate'].values[0]}%")
    print(f"Bounce Rate:           {metrics['bounce_rate'].values[0]}%")
    print(f"Avg Session Duration:  {metrics['avg_session_duration'].values[0]:.0f} seconds")
    print(f"Avg Pages/Session:     {metrics['avg_pages_per_session'].values[0]:.2f}")
    print(f"\n💰 Revenue Metrics:\n")
    print(f"Total Revenue:         ₹{metrics['total_revenue'].values[0]:,.2f}")
    print(f"Total Ad Spend:        ₹{metrics['total_ad_spend'].values[0]:,.2f}")
    print(f"ROI:                   {metrics['overall_roi'].values[0]}%")
    
    input("\n\nPress Enter to continue...")


def analyze_funnel(db):
    """Analyze conversion funnel"""
    print_header("CONVERSION FUNNEL ANALYSIS")
    
    funnel = db.get_conversion_funnel()
    
    print("\n🎯 Conversion Funnel Breakdown:\n")
    for _, row in funnel.iterrows():
        print(f"{row['stage']:<25}: {row['users']:>7,} users ({row['percentage']:>6}%)")
        if row['drop_off'] > 0:
            print(f"{'':25}  ⚠️  Drop-off: {row['drop_off']}%")
        print()
    
    # Cart abandonment
    cart = db.get_cart_abandonment_rate()
    print("\n🛒 Cart Abandonment Analysis:\n")
    print(f"Carts Created:     {cart['carts_created'].values[0]:,}")
    print(f"Carts Abandoned:   {cart['carts_abandoned'].values[0]:,}")
    print(f"Carts Purchased:   {cart['carts_purchased'].values[0]:,}")
    print(f"Abandonment Rate:  {cart['abandonment_rate'].values[0]}%")
    
    input("\n\nPress Enter to continue...")


def analyze_traffic_sources(db):
    """Analyze traffic source performance"""
    print_header("TRAFFIC SOURCE PERFORMANCE")
    
    traffic = db.get_traffic_source_performance()
    
    print("\n📈 Performance by Traffic Source:\n")
    print(f"{'Source':<18} {'Sessions':>10} {'Conv Rate':>10} {'Revenue':>15} {'ROI':>8}")
    print("-" * 70)
    
    for _, row in traffic.iterrows():
        print(f"{row['traffic_source']:<18} {row['sessions']:>10,} "
              f"{row['conversion_rate']:>9.2f}% ₹{row['total_revenue']:>13,.0f} "
              f"{row['roi_percent']:>7.1f}%")
    
    # Best performing source
    best = traffic.iloc[0]
    print(f"\n🏆 Best Performing: {best['traffic_source']}")
    print(f"   Conversion Rate: {best['conversion_rate']}%")
    print(f"   ROI: {best['roi_percent']}%")
    
    input("\n\nPress Enter to continue...")


def analyze_cart_abandonment(db, sessions_df):
    """Detailed cart abandonment analysis"""
    print_header("CART ABANDONMENT DEEP DIVE")
    
    analyzer = FunnelAnalyzer(sessions_df)
    insights = analyzer.get_cart_abandonment_insights()
    
    print("\n🛒 Cart Abandonment Insights:\n")
    print(f"Total Carts:         {insights['total_carts']:,}")
    print(f"Abandoned Carts:     {insights['abandoned_carts']:,}")
    print(f"Completed Carts:     {insights['completed_carts']:,}")
    print(f"Abandonment Rate:    {insights['abandonment_rate']:.2f}%")
    
    print("\n📊 Abandonment by Traffic Source:")
    for source, count in sorted(insights['abandonment_by_source'].items(), 
                                key=lambda x: x[1], reverse=True):
        print(f"  {source:<20}: {count:,} abandoned carts")
    
    print("\n📱 Abandonment by Device:")
    for device, count in sorted(insights['abandonment_by_device'].items(), 
                               key=lambda x: x[1], reverse=True):
        print(f"  {device:<20}: {count:,} abandoned carts")
    
    input("\n\nPress Enter to continue...")


def generate_visualizations(db, sessions_df):
    """Generate all visualizations"""
    print_header("GENERATING VISUALIZATIONS")
    
    print("Creating charts... This may take a minute...\n")
    
    visualizer = EcommerceVisualizer(sessions_df)
    
    # Get data
    funnel_data = db.get_conversion_funnel()
    traffic_data = db.get_traffic_source_performance()
    device_data = db.get_device_performance()
    category_data = db.get_category_performance()
    location_data = db.get_location_analysis()
    weekday_data = db.get_weekday_performance()
    returning_data = db.get_returning_vs_new()
    hourly_data = db.get_hourly_patterns()
    daily_data = db.get_daily_trends()
    overall_metrics = db.get_overall_metrics()
    
    # Generate charts
    visualizer.plot_conversion_funnel(funnel_data)
    visualizer.plot_traffic_source_breakdown(traffic_data)
    visualizer.plot_cart_abandonment_trend(daily_data)
    visualizer.plot_hourly_heatmap(hourly_data)
    visualizer.plot_device_performance(device_data)
    visualizer.plot_revenue_by_category(category_data)
    visualizer.plot_traffic_source_roi(traffic_data)
    visualizer.plot_conversion_trends(daily_data)
    visualizer.plot_weekday_performance(weekday_data)
    visualizer.plot_customer_segmentation(returning_data)
    visualizer.plot_revenue_distribution(sessions_df)
    visualizer.plot_location_performance(location_data)
    visualizer.plot_session_duration_analysis(sessions_df)
    visualizer.create_kpi_dashboard(overall_metrics)
    
    print("\n✓ All visualizations created successfully!")
    print(f"📁 Charts saved in: output/")
    input("\nPress Enter to continue...")


def create_excel_report(db, sessions_df):
    """Create Excel report"""
    print_header("EXCEL REPORT GENERATION")
    
    analyzer = FunnelAnalyzer(sessions_df)
    reporter = ReportGenerator()
    
    filename = reporter.create_excel_report(db, sessions_df, analyzer)
    
    print(f"\n✓ Excel report created successfully!")
    print(f"📁 Location: {filename}")
    input("\nPress Enter to continue...")


def generate_business_insights(db, sessions_df):
    """Generate business insights document"""
    print_header("BUSINESS INSIGHTS GENERATION")
    
    analyzer = FunnelAnalyzer(sessions_df)
    reporter = ReportGenerator()
    
    filename = reporter.create_business_insights_doc(db, analyzer)
    sql_file = reporter.create_sql_queries_file()
    
    print(f"\n✓ Business insights document created!")
    print(f"📁 Insights: {filename}")
    print(f"📁 SQL Queries: {sql_file}")
    input("\nPress Enter to continue...")


def view_sql_queries(db):
    """Display SQL queries being used"""
    print_header("SQL ANALYTICAL QUERIES")
    
    print("\n1. Overall Metrics Query")
    print("2. Conversion Funnel Query")
    print("3. Cart Abandonment Query")
    print("4. Traffic Source Performance")
    print("5. Device Performance")
    print("6. Hourly Patterns")
    print("7. Category Performance")
    print("8. Location Analysis")
    print("9. New vs Returning Customers")
    print("10. Revenue Metrics")
    
    print("\n✓ All SQL queries are documented in: reports/analytical_queries.sql")
    input("\nPress Enter to continue...")


def run_complete_analysis():
    """Run complete end-to-end analysis"""
    print_header("COMPLETE ANALYSIS PIPELINE")
    
    print("This will:\n")
    print("1. Generate 15,000 session records")
    print("2. Load data into SQLite database")
    print("3. Run all analytical queries")
    print("4. Generate all visualizations")
    print("5. Create Excel report")
    print("6. Generate business insights\n")
    
    confirm = input("Continue? (y/n): ")
    
    if confirm.lower() != 'y':
        return
    
    # Step 1: Generate data
    print_section("Step 1/6: Generating Data")
    generator = EcommerceDataGenerator(num_sessions=15000)
    sessions_df = generator.generate_sessions()
    events_df = generator.generate_event_log(sessions_df)
    generator.save_data(sessions_df, events_df)
    
    # Step 2: Load to database
    print_section("Step 2/6: Loading to Database")
    db = EcommerceDatabase()
    db.connect()
    db.create_tables()
    db.load_data('data/sessions_data.csv', 'data/events_data.csv')
    
    # Step 3: Run analytics
    print_section("Step 3/6: Running Analytics")
    analyzer = FunnelAnalyzer(sessions_df)
    funnel_metrics = analyzer.calculate_funnel_metrics()
    bottlenecks = analyzer.identify_bottlenecks()
    print(f"✓ Analyzed {len(sessions_df):,} sessions")
    print(f"✓ Identified {len(bottlenecks)} bottlenecks")
    
    # Step 4: Generate visualizations
    print_section("Step 4/6: Generating Visualizations")
    generate_visualizations(db, sessions_df)
    
    # Step 5: Create Excel report
    print_section("Step 5/6: Creating Excel Report")
    reporter = ReportGenerator()
    reporter.create_excel_report(db, sessions_df, analyzer)
    
    # Step 6: Generate insights
    print_section("Step 6/6: Generating Business Insights")
    reporter.create_business_insights_doc(db, analyzer)
    reporter.create_sql_queries_file()
    
    print_header("ANALYSIS COMPLETE!")
    print("\n📊 Summary:\n")
    print(f"Sessions Analyzed:     {len(sessions_df):,}")
    print(f"Conversion Rate:       {funnel_metrics['overall_conversion_rate']:.2f}%")
    print(f"Cart Abandonment:      {analyzer.get_cart_abandonment_insights()['abandonment_rate']:.2f}%")
    print(f"\n📁 Generated Files:\n")
    print("  - data/sessions_data.csv")
    print("  - data/events_data.csv")
    print("  - database/ecommerce.db")
    print("  - output/*.html (14 interactive charts)")
    print("  - output/*.png (chart images)")
    print("  - reports/ecommerce_analysis_report.xlsx")
    print("  - reports/business_insights.md")
    print("  - reports/analytical_queries.sql")
    
    db.close()
    
    input("\n\nPress Enter to continue...")


def main():
    """Main application"""
    
    db = None
    sessions_df = None
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_menu()
        
        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")
            continue
        
        if choice == 1:
            sessions_df, _ = generate_data()
        
        elif choice == 2:
            db = load_data_to_database()
        
        elif choice == 3:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            view_overall_metrics(db)
        
        elif choice == 4:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            analyze_funnel(db)
        
        elif choice == 5:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            analyze_traffic_sources(db)
        
        elif choice == 6:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            if sessions_df is None:
                import pandas as pd
                sessions_df = pd.read_csv('data/sessions_data.csv')
            analyze_cart_abandonment(db, sessions_df)
        
        elif choice == 7:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            if sessions_df is None:
                import pandas as pd
                sessions_df = pd.read_csv('data/sessions_data.csv')
            generate_visualizations(db, sessions_df)
        
        elif choice == 8:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            if sessions_df is None:
                import pandas as pd
                sessions_df = pd.read_csv('data/sessions_data.csv')
            create_excel_report(db, sessions_df)
        
        elif choice == 9:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            if sessions_df is None:
                import pandas as pd
                sessions_df = pd.read_csv('data/sessions_data.csv')
            generate_business_insights(db, sessions_df)
        
        elif choice == 10:
            if db is None:
                db = EcommerceDatabase()
                db.connect()
            view_sql_queries(db)
        
        elif choice == 11:
            run_complete_analysis()
        
        elif choice == 12:
            if db:
                db.close()
            print("\n" + "=" * 70)
            print("Thank you for using E-Commerce Analytics!")
            print("\nDeveloper: Akshay Tiwari")
            print("Data Analyst: Akshay Tiwari")
            print("Email: akshay.tiwari@example.com")
            print("\n© 2026 College Data Analytics Project")
            print("=" * 70 + "\n")
            break
        
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
