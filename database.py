"""
Database Module
Handles SQLite operations and analytical queries
"""

import sqlite3
import pandas as pd


class EcommerceDatabase:
    """Manage SQLite database for e-commerce analytics"""
    
    def __init__(self, db_path='database/ecommerce.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"✓ Connected to database: {self.db_path}")
            return True
        except Exception as e:
            print(f"✗ Database connection error: {e}")
            return False
    
    def create_tables(self):
        """Create database schema"""
        
        # Sessions table
        sessions_table = """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            date DATE NOT NULL,
            hour INTEGER,
            day_of_week TEXT,
            traffic_source TEXT,
            device TEXT,
            location TEXT,
            category TEXT,
            is_returning BOOLEAN,
            landed BOOLEAN,
            viewed_product BOOLEAN,
            added_to_cart BOOLEAN,
            started_checkout BOOLEAN,
            completed_purchase BOOLEAN,
            session_duration_seconds INTEGER,
            pages_viewed INTEGER,
            bounced BOOLEAN,
            revenue REAL,
            ad_spend REAL
        )
        """
        
        # Events table
        events_table = """
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            event_type TEXT,
            page TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
        """
        
        self.cursor.execute(sessions_table)
        self.cursor.execute(events_table)
        self.conn.commit()
        print("✓ Database tables created")
    
    def load_data(self, sessions_path, events_path):
        """Load CSV data into database"""
        
        # Load sessions
        sessions_df = pd.read_csv(sessions_path)
        sessions_df.to_sql('sessions', self.conn, if_exists='replace', index=False)
        print(f"✓ Loaded {len(sessions_df)} sessions")
        
        # Load events
        events_df = pd.read_csv(events_path)
        events_df.to_sql('events', self.conn, if_exists='replace', index=False)
        print(f"✓ Loaded {len(events_df)} events")
    
    # ==================== ANALYTICAL QUERIES ====================
    
    def get_overall_metrics(self):
        """Query 1: Overall key metrics"""
        query = """
        SELECT 
            COUNT(DISTINCT session_id) as total_sessions,
            COUNT(DISTINCT user_id) as unique_users,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(CASE WHEN bounced = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as bounce_rate,
            ROUND(AVG(session_duration_seconds), 2) as avg_session_duration,
            ROUND(AVG(pages_viewed), 2) as avg_pages_per_session,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(SUM(ad_spend), 2) as total_ad_spend,
            ROUND((SUM(revenue) - SUM(ad_spend)) / SUM(ad_spend) * 100, 2) as overall_roi
        FROM sessions
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_conversion_funnel(self):
        """Query 2: Conversion funnel stages"""
        query = """
        SELECT 
            'Landing Page' as stage,
            1 as stage_order,
            COUNT(*) as users,
            100.0 as percentage,
            0 as drop_off
        FROM sessions
        
        UNION ALL
        
        SELECT 
            'Product View' as stage,
            2 as stage_order,
            SUM(CASE WHEN viewed_product = 1 THEN 1 ELSE 0 END) as users,
            ROUND(SUM(CASE WHEN viewed_product = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage,
            ROUND((COUNT(*) - SUM(CASE WHEN viewed_product = 1 THEN 1 ELSE 0 END)) * 100.0 / COUNT(*), 2) as drop_off
        FROM sessions
        
        UNION ALL
        
        SELECT 
            'Add to Cart' as stage,
            3 as stage_order,
            SUM(CASE WHEN added_to_cart = 1 THEN 1 ELSE 0 END) as users,
            ROUND(SUM(CASE WHEN added_to_cart = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage,
            ROUND((SUM(CASE WHEN viewed_product = 1 THEN 1 ELSE 0 END) - 
                   SUM(CASE WHEN added_to_cart = 1 THEN 1 ELSE 0 END)) * 100.0 / 
                   SUM(CASE WHEN viewed_product = 1 THEN 1 ELSE 0 END), 2) as drop_off
        FROM sessions
        
        UNION ALL
        
        SELECT 
            'Checkout Started' as stage,
            4 as stage_order,
            SUM(CASE WHEN started_checkout = 1 THEN 1 ELSE 0 END) as users,
            ROUND(SUM(CASE WHEN started_checkout = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage,
            ROUND((SUM(CASE WHEN added_to_cart = 1 THEN 1 ELSE 0 END) - 
                   SUM(CASE WHEN started_checkout = 1 THEN 1 ELSE 0 END)) * 100.0 / 
                   SUM(CASE WHEN added_to_cart = 1 THEN 1 ELSE 0 END), 2) as drop_off
        FROM sessions
        
        UNION ALL
        
        SELECT 
            'Purchase Complete' as stage,
            5 as stage_order,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as users,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentage,
            ROUND((SUM(CASE WHEN started_checkout = 1 THEN 1 ELSE 0 END) - 
                   SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END)) * 100.0 / 
                   SUM(CASE WHEN started_checkout = 1 THEN 1 ELSE 0 END), 2) as drop_off
        FROM sessions
        
        ORDER BY stage_order
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_cart_abandonment_rate(self):
        """Query 3: Cart abandonment analysis"""
        query = """
        SELECT 
            COUNT(CASE WHEN added_to_cart = 1 THEN 1 END) as carts_created,
            COUNT(CASE WHEN added_to_cart = 1 AND completed_purchase = 0 THEN 1 END) as carts_abandoned,
            COUNT(CASE WHEN completed_purchase = 1 THEN 1 END) as carts_purchased,
            ROUND(COUNT(CASE WHEN added_to_cart = 1 AND completed_purchase = 0 THEN 1 END) * 100.0 / 
                  COUNT(CASE WHEN added_to_cart = 1 THEN 1 END), 2) as abandonment_rate
        FROM sessions
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_traffic_source_performance(self):
        """Query 4: Traffic source analysis"""
        query = """
        SELECT 
            traffic_source,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(CASE WHEN bounced = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as bounce_rate,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(SUM(ad_spend), 2) as total_ad_spend,
            ROUND((SUM(revenue) - SUM(ad_spend)) / NULLIF(SUM(ad_spend), 0) * 100, 2) as roi_percent,
            ROUND(SUM(revenue) / COUNT(*), 2) as revenue_per_session
        FROM sessions
        GROUP BY traffic_source
        ORDER BY conversions DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_device_performance(self):
        """Query 5: Device-wise performance"""
        query = """
        SELECT 
            device,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(AVG(session_duration_seconds), 2) as avg_duration,
            ROUND(AVG(pages_viewed), 2) as avg_pages,
            ROUND(SUM(revenue), 2) as total_revenue
        FROM sessions
        GROUP BY device
        ORDER BY sessions DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_hourly_patterns(self):
        """Query 6: Hourly traffic and conversion patterns"""
        query = """
        SELECT 
            hour,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(revenue), 2) as revenue
        FROM sessions
        GROUP BY hour
        ORDER BY hour
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_daily_trends(self):
        """Query 7: Daily trends over time"""
        query = """
        SELECT 
            date,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(revenue), 2) as revenue,
            ROUND(AVG(session_duration_seconds), 2) as avg_duration
        FROM sessions
        GROUP BY date
        ORDER BY date
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_weekday_performance(self):
        """Query 8: Day of week analysis"""
        query = """
        SELECT 
            day_of_week,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(revenue), 2) as revenue
        FROM sessions
        GROUP BY day_of_week
        ORDER BY 
            CASE day_of_week
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
            END
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_category_performance(self):
        """Query 9: Product category analysis"""
        query = """
        SELECT 
            category,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(AVG(CASE WHEN completed_purchase = 1 THEN revenue ELSE NULL END), 2) as avg_order_value
        FROM sessions
        GROUP BY category
        ORDER BY total_revenue DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_returning_vs_new(self):
        """Query 10: Returning vs new customer performance"""
        query = """
        SELECT 
            CASE WHEN is_returning = 1 THEN 'Returning' ELSE 'New' END as customer_type,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(AVG(CASE WHEN completed_purchase = 1 THEN revenue ELSE NULL END), 2) as avg_order_value
        FROM sessions
        GROUP BY is_returning
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_location_analysis(self):
        """Query 11: Geographic performance"""
        query = """
        SELECT 
            location,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(revenue), 2) as total_revenue
        FROM sessions
        GROUP BY location
        ORDER BY total_revenue DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_checkout_drop_off_analysis(self):
        """Query 12: Detailed checkout drop-off"""
        query = """
        SELECT 
            'Reached Checkout' as stage,
            COUNT(CASE WHEN started_checkout = 1 THEN 1 END) as users,
            100.0 as percentage
        FROM sessions
        
        UNION ALL
        
        SELECT 
            'Completed Purchase' as stage,
            COUNT(CASE WHEN completed_purchase = 1 THEN 1 END) as users,
            ROUND(COUNT(CASE WHEN completed_purchase = 1 THEN 1 END) * 100.0 / 
                  COUNT(CASE WHEN started_checkout = 1 THEN 1 END), 2) as percentage
        FROM sessions
        WHERE started_checkout = 1
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_revenue_metrics(self):
        """Query 13: Revenue breakdown"""
        query = """
        SELECT 
            COUNT(CASE WHEN completed_purchase = 1 THEN 1 END) as total_orders,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(AVG(CASE WHEN completed_purchase = 1 THEN revenue END), 2) as avg_order_value,
            ROUND(MIN(CASE WHEN completed_purchase = 1 THEN revenue END), 2) as min_order_value,
            ROUND(MAX(CASE WHEN completed_purchase = 1 THEN revenue END), 2) as max_order_value,
            ROUND(SUM(revenue) / COUNT(DISTINCT session_id), 2) as revenue_per_session,
            ROUND(SUM(revenue) / COUNT(DISTINCT user_id), 2) as revenue_per_user
        FROM sessions
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_session_quality_metrics(self):
        """Query 14: Session quality indicators"""
        query = """
        SELECT 
            CASE 
                WHEN session_duration_seconds < 30 THEN '< 30 sec'
                WHEN session_duration_seconds < 120 THEN '30 sec - 2 min'
                WHEN session_duration_seconds < 300 THEN '2 - 5 min'
                WHEN session_duration_seconds < 600 THEN '5 - 10 min'
                ELSE '> 10 min'
            END as duration_bucket,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate
        FROM sessions
        GROUP BY duration_bucket
        ORDER BY 
            CASE duration_bucket
                WHEN '< 30 sec' THEN 1
                WHEN '30 sec - 2 min' THEN 2
                WHEN '2 - 5 min' THEN 3
                WHEN '5 - 10 min' THEN 4
                ELSE 5
            END
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_top_converting_segments(self):
        """Query 15: Best performing segments"""
        query = """
        SELECT 
            traffic_source,
            device,
            COUNT(*) as sessions,
            SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) as conversions,
            ROUND(SUM(CASE WHEN completed_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(*), 2) as conversion_rate,
            ROUND(SUM(revenue), 2) as revenue
        FROM sessions
        GROUP BY traffic_source, device
        HAVING COUNT(*) > 100
        ORDER BY conversion_rate DESC
        LIMIT 10
        """
        return pd.read_sql_query(query, self.conn)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")
