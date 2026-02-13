"""
E-Commerce Data Generator
Generates realistic session and user behavior data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


class EcommerceDataGenerator:
    """Generate realistic e-commerce session data"""
    
    def __init__(self, num_sessions=15000):
        self.num_sessions = num_sessions
        self.traffic_sources = ['Google Ads', 'Facebook Ads', 'Organic Search', 
                                'Direct', 'Email Campaign', 'Referral']
        self.devices = ['Desktop', 'Mobile', 'Tablet']
        self.categories = ['Electronics', 'Fashion', 'Home & Kitchen', 
                          'Sports', 'Books', 'Beauty', 'Toys']
        self.locations = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
                         'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
        
        # Conversion probabilities by traffic source
        self.conversion_rates = {
            'Google Ads': 0.18,
            'Facebook Ads': 0.15,
            'Organic Search': 0.16,
            'Direct': 0.12,
            'Email Campaign': 0.20,
            'Referral': 0.14
        }
        
        # Ad spend per session by source
        self.ad_costs = {
            'Google Ads': 2.5,
            'Facebook Ads': 1.8,
            'Organic Search': 0.3,
            'Direct': 0,
            'Email Campaign': 0.5,
            'Referral': 0.2
        }
    
    def generate_timestamp(self):
        """Generate realistic timestamps over last 3 months"""
        start_date = datetime.now() - timedelta(days=90)
        end_date = datetime.now()
        
        # Random date
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)
        random_date = start_date + timedelta(days=random_days)
        
        # Weight towards business hours (9 AM - 9 PM)
        hour_weights = [1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 6, 7, 8, 7, 5, 3, 2, 1]
        hour = random.choices(range(24), weights=hour_weights)[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        return random_date.replace(hour=hour, minute=minute, second=second)
    
    def simulate_user_journey(self, traffic_source, device):
        """Simulate realistic user journey through funnel"""
        
        # Base conversion rate
        base_conversion = self.conversion_rates.get(traffic_source, 0.14)
        
        # Device adjustment
        device_multiplier = {
            'Desktop': 1.2,
            'Mobile': 0.85,
            'Tablet': 1.0
        }
        conversion_prob = base_conversion * device_multiplier.get(device, 1.0)
        
        # Funnel stages
        landed = True
        viewed_product = random.random() < 0.65  # 65% view products
        added_to_cart = viewed_product and random.random() < 0.54  # 54% of viewers add to cart
        started_checkout = added_to_cart and random.random() < 0.57  # 57% proceed to checkout
        completed_purchase = started_checkout and random.random() < (conversion_prob * 2.8)
        
        # Session metrics
        if not viewed_product:
            # Bounced
            session_duration = random.randint(5, 30)  # seconds
            pages_viewed = 1
            bounced = True
        elif viewed_product and not added_to_cart:
            session_duration = random.randint(60, 300)
            pages_viewed = random.randint(2, 5)
            bounced = False
        elif added_to_cart and not started_checkout:
            session_duration = random.randint(120, 480)
            pages_viewed = random.randint(3, 8)
            bounced = False
        elif started_checkout and not completed_purchase:
            session_duration = random.randint(180, 600)
            pages_viewed = random.randint(4, 10)
            bounced = False
        else:
            # Completed purchase
            session_duration = random.randint(300, 900)
            pages_viewed = random.randint(5, 15)
            bounced = False
        
        # Revenue if purchased
        if completed_purchase:
            revenue = round(random.uniform(500, 5000), 2)
        else:
            revenue = 0
        
        return {
            'landed': landed,
            'viewed_product': viewed_product,
            'added_to_cart': added_to_cart,
            'started_checkout': started_checkout,
            'completed_purchase': completed_purchase,
            'session_duration': session_duration,
            'pages_viewed': pages_viewed,
            'bounced': bounced,
            'revenue': revenue
        }
    
    def generate_sessions(self):
        """Generate complete session dataset"""
        
        print(f"Generating {self.num_sessions} e-commerce sessions...")
        
        sessions = []
        
        for i in range(self.num_sessions):
            # Basic info
            session_id = f"SES_{i+1:06d}"
            user_id = f"USER_{random.randint(1, int(self.num_sessions * 0.7)):06d}"  # Some returning users
            timestamp = self.generate_timestamp()
            
            # Random attributes
            traffic_source = random.choices(
                self.traffic_sources,
                weights=[30, 25, 20, 10, 10, 5]  # Weighted distribution
            )[0]
            
            device = random.choices(
                self.devices,
                weights=[35, 45, 20]  # Mobile dominant
            )[0]
            
            location = random.choice(self.locations)
            category = random.choice(self.categories)
            
            # Simulate journey
            journey = self.simulate_user_journey(traffic_source, device)
            
            # Ad spend
            ad_spend = self.ad_costs.get(traffic_source, 0)
            
            # Is returning customer?
            is_returning = random.random() < 0.3  # 30% returning
            
            session_data = {
                'session_id': session_id,
                'user_id': user_id,
                'timestamp': timestamp,
                'date': timestamp.date(),
                'hour': timestamp.hour,
                'day_of_week': timestamp.strftime('%A'),
                'traffic_source': traffic_source,
                'device': device,
                'location': location,
                'category': category,
                'is_returning': is_returning,
                'landed': journey['landed'],
                'viewed_product': journey['viewed_product'],
                'added_to_cart': journey['added_to_cart'],
                'started_checkout': journey['started_checkout'],
                'completed_purchase': journey['completed_purchase'],
                'session_duration_seconds': journey['session_duration'],
                'pages_viewed': journey['pages_viewed'],
                'bounced': journey['bounced'],
                'revenue': journey['revenue'],
                'ad_spend': ad_spend
            }
            
            sessions.append(session_data)
            
            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1} sessions...")
        
        df = pd.DataFrame(sessions)
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        print(f"✓ Generated {len(df)} sessions successfully!")
        return df
    
    def generate_event_log(self, sessions_df):
        """Generate detailed event log from sessions"""
        
        print("\nGenerating event-level data...")
        
        events = []
        
        for _, session in sessions_df.iterrows():
            session_id = session['session_id']
            user_id = session['user_id']
            timestamp = session['timestamp']
            
            # Landing event
            events.append({
                'event_id': f"EVT_{len(events)+1:08d}",
                'session_id': session_id,
                'user_id': user_id,
                'timestamp': timestamp,
                'event_type': 'page_view',
                'page': 'homepage'
            })
            
            current_time = timestamp
            
            # Product view
            if session['viewed_product']:
                current_time += timedelta(seconds=random.randint(10, 60))
                events.append({
                    'event_id': f"EVT_{len(events)+1:08d}",
                    'session_id': session_id,
                    'user_id': user_id,
                    'timestamp': current_time,
                    'event_type': 'page_view',
                    'page': 'product_page'
                })
            
            # Add to cart
            if session['added_to_cart']:
                current_time += timedelta(seconds=random.randint(30, 120))
                events.append({
                    'event_id': f"EVT_{len(events)+1:08d}",
                    'session_id': session_id,
                    'user_id': user_id,
                    'timestamp': current_time,
                    'event_type': 'add_to_cart',
                    'page': 'product_page'
                })
            
            # Checkout
            if session['started_checkout']:
                current_time += timedelta(seconds=random.randint(20, 90))
                events.append({
                    'event_id': f"EVT_{len(events)+1:08d}",
                    'session_id': session_id,
                    'user_id': user_id,
                    'timestamp': current_time,
                    'event_type': 'checkout_start',
                    'page': 'checkout'
                })
            
            # Purchase
            if session['completed_purchase']:
                current_time += timedelta(seconds=random.randint(60, 180))
                events.append({
                    'event_id': f"EVT_{len(events)+1:08d}",
                    'session_id': session_id,
                    'user_id': user_id,
                    'timestamp': current_time,
                    'event_type': 'purchase',
                    'page': 'confirmation'
                })
        
        events_df = pd.DataFrame(events)
        print(f"✓ Generated {len(events_df)} events!")
        
        return events_df
    
    def save_data(self, sessions_df, events_df, output_dir='data'):
        """Save generated data to CSV"""
        
        sessions_path = f'{output_dir}/sessions_data.csv'
        events_path = f'{output_dir}/events_data.csv'
        
        sessions_df.to_csv(sessions_path, index=False)
        events_df.to_csv(events_path, index=False)
        
        print(f"\n✓ Data saved:")
        print(f"  - {sessions_path}")
        print(f"  - {events_path}")
        
        return sessions_path, events_path


if __name__ == "__main__":
    # Generate data
    generator = EcommerceDataGenerator(num_sessions=15000)
    sessions_df = generator.generate_sessions()
    events_df = generator.generate_event_log(sessions_df)
    generator.save_data(sessions_df, events_df)
    
    # Quick stats
    print("\n" + "="*60)
    print("QUICK STATISTICS")
    print("="*60)
    print(f"Total Sessions: {len(sessions_df):,}")
    print(f"Total Events: {len(events_df):,}")
    print(f"Unique Users: {sessions_df['user_id'].nunique():,}")
    print(f"Conversions: {sessions_df['completed_purchase'].sum():,}")
    print(f"Conversion Rate: {sessions_df['completed_purchase'].mean()*100:.2f}%")
    print(f"Total Revenue: ₹{sessions_df['revenue'].sum():,.2f}")
    print("="*60)
