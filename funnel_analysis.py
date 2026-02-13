"""
Funnel Analysis Module
Advanced analytics for e-commerce conversion funnel
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class FunnelAnalyzer:
    """Analyze conversion funnel and user behavior"""
    
    def __init__(self, sessions_df):
        self.df = sessions_df
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def calculate_funnel_metrics(self):
        """Calculate comprehensive funnel metrics"""
        
        total_sessions = len(self.df)
        
        metrics = {
            'total_sessions': total_sessions,
            'stage_1_landing': total_sessions,
            'stage_2_product_view': self.df['viewed_product'].sum(),
            'stage_3_add_to_cart': self.df['added_to_cart'].sum(),
            'stage_4_checkout': self.df['started_checkout'].sum(),
            'stage_5_purchase': self.df['completed_purchase'].sum(),
            
            # Conversion rates at each stage
            'landing_to_product_rate': (self.df['viewed_product'].sum() / total_sessions * 100),
            'product_to_cart_rate': (self.df['added_to_cart'].sum() / self.df['viewed_product'].sum() * 100) if self.df['viewed_product'].sum() > 0 else 0,
            'cart_to_checkout_rate': (self.df['started_checkout'].sum() / self.df['added_to_cart'].sum() * 100) if self.df['added_to_cart'].sum() > 0 else 0,
            'checkout_to_purchase_rate': (self.df['completed_purchase'].sum() / self.df['started_checkout'].sum() * 100) if self.df['started_checkout'].sum() > 0 else 0,
            
            # Overall conversion
            'overall_conversion_rate': (self.df['completed_purchase'].sum() / total_sessions * 100),
            
            # Drop-off analysis
            'product_view_dropoff': ((self.df['viewed_product'].sum() - self.df['added_to_cart'].sum()) / self.df['viewed_product'].sum() * 100) if self.df['viewed_product'].sum() > 0 else 0,
            'cart_dropoff': ((self.df['added_to_cart'].sum() - self.df['started_checkout'].sum()) / self.df['added_to_cart'].sum() * 100) if self.df['added_to_cart'].sum() > 0 else 0,
            'checkout_dropoff': ((self.df['started_checkout'].sum() - self.df['completed_purchase'].sum()) / self.df['started_checkout'].sum() * 100) if self.df['started_checkout'].sum() > 0 else 0,
        }
        
        return metrics
    
    def get_cart_abandonment_insights(self):
        """Detailed cart abandonment analysis"""
        
        cart_sessions = self.df[self.df['added_to_cart'] == True]
        abandoned_carts = cart_sessions[cart_sessions['completed_purchase'] == False]
        
        insights = {
            'total_carts': len(cart_sessions),
            'abandoned_carts': len(abandoned_carts),
            'completed_carts': len(cart_sessions[cart_sessions['completed_purchase'] == True]),
            'abandonment_rate': (len(abandoned_carts) / len(cart_sessions) * 100) if len(cart_sessions) > 0 else 0,
            
            # Abandonment by traffic source
            'abandonment_by_source': abandoned_carts.groupby('traffic_source').size().to_dict(),
            
            # Abandonment by device
            'abandonment_by_device': abandoned_carts.groupby('device').size().to_dict(),
            
            # Average cart value (potential lost revenue)
            'potential_lost_revenue': abandoned_carts['revenue'].sum()  # This would be estimated
        }
        
        return insights
    
    def analyze_time_to_conversion(self):
        """Analyze time spent before conversion"""
        
        converted = self.df[self.df['completed_purchase'] == True]
        
        if len(converted) == 0:
            return None
        
        analysis = {
            'avg_time_to_convert': converted['session_duration_seconds'].mean(),
            'median_time_to_convert': converted['session_duration_seconds'].median(),
            'min_time': converted['session_duration_seconds'].min(),
            'max_time': converted['session_duration_seconds'].max(),
            
            # Distribution
            'under_2_min': len(converted[converted['session_duration_seconds'] < 120]) / len(converted) * 100,
            '2_to_5_min': len(converted[(converted['session_duration_seconds'] >= 120) & 
                                       (converted['session_duration_seconds'] < 300)]) / len(converted) * 100,
            '5_to_10_min': len(converted[(converted['session_duration_seconds'] >= 300) & 
                                        (converted['session_duration_seconds'] < 600)]) / len(converted) * 100,
            'over_10_min': len(converted[converted['session_duration_seconds'] >= 600]) / len(converted) * 100,
        }
        
        return analysis
    
    def segment_analysis(self, segment_by='traffic_source'):
        """Detailed segmentation analysis"""
        
        segments = self.df.groupby(segment_by).agg({
            'session_id': 'count',
            'completed_purchase': 'sum',
            'revenue': 'sum',
            'ad_spend': 'sum',
            'session_duration_seconds': 'mean',
            'pages_viewed': 'mean',
            'bounced': 'sum'
        }).reset_index()
        
        segments.columns = [segment_by, 'sessions', 'conversions', 'revenue', 
                           'ad_spend', 'avg_duration', 'avg_pages', 'bounces']
        
        # Calculate rates
        segments['conversion_rate'] = (segments['conversions'] / segments['sessions'] * 100).round(2)
        segments['bounce_rate'] = (segments['bounces'] / segments['sessions'] * 100).round(2)
        segments['roi'] = ((segments['revenue'] - segments['ad_spend']) / segments['ad_spend'] * 100).round(2)
        segments['revenue_per_session'] = (segments['revenue'] / segments['sessions']).round(2)
        
        return segments.sort_values('revenue', ascending=False)
    
    def get_peak_performance_times(self):
        """Identify best performing time periods"""
        
        hourly = self.df.groupby('hour').agg({
            'session_id': 'count',
            'completed_purchase': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        hourly.columns = ['hour', 'sessions', 'conversions', 'revenue']
        hourly['conversion_rate'] = (hourly['conversions'] / hourly['sessions'] * 100).round(2)
        
        # Find peak hours
        peak_traffic_hour = hourly.loc[hourly['sessions'].idxmax(), 'hour']
        peak_conversion_hour = hourly.loc[hourly['conversion_rate'].idxmax(), 'hour']
        peak_revenue_hour = hourly.loc[hourly['revenue'].idxmax(), 'hour']
        
        return {
            'peak_traffic_hour': int(peak_traffic_hour),
            'peak_conversion_hour': int(peak_conversion_hour),
            'peak_revenue_hour': int(peak_revenue_hour),
            'hourly_data': hourly
        }
    
    def cohort_analysis(self):
        """Analyze user cohorts by first visit date"""
        
        # Get first session for each user
        user_first_session = self.df.groupby('user_id')['date'].min().reset_index()
        user_first_session.columns = ['user_id', 'cohort_date']
        
        # Merge back
        cohort_df = self.df.merge(user_first_session, on='user_id')
        
        # Calculate cohort metrics
        cohort_metrics = cohort_df.groupby('cohort_date').agg({
            'user_id': 'nunique',
            'session_id': 'count',
            'completed_purchase': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        cohort_metrics.columns = ['cohort_date', 'users', 'sessions', 'conversions', 'revenue']
        cohort_metrics['conversion_rate'] = (cohort_metrics['conversions'] / cohort_metrics['sessions'] * 100).round(2)
        cohort_metrics['revenue_per_user'] = (cohort_metrics['revenue'] / cohort_metrics['users']).round(2)
        
        return cohort_metrics.sort_values('cohort_date')
    
    def identify_bottlenecks(self):
        """Identify main conversion bottlenecks"""
        
        funnel = self.calculate_funnel_metrics()
        
        bottlenecks = []
        
        # Check each stage
        if funnel['landing_to_product_rate'] < 60:
            bottlenecks.append({
                'stage': 'Landing to Product View',
                'drop_off_rate': 100 - funnel['landing_to_product_rate'],
                'severity': 'High' if (100 - funnel['landing_to_product_rate']) > 40 else 'Medium',
                'recommendation': 'Improve homepage engagement, add featured products, optimize loading speed'
            })
        
        if funnel['product_to_cart_rate'] < 50:
            bottlenecks.append({
                'stage': 'Product View to Add to Cart',
                'drop_off_rate': 100 - funnel['product_to_cart_rate'],
                'severity': 'High' if (100 - funnel['product_to_cart_rate']) > 50 else 'Medium',
                'recommendation': 'Enhance product descriptions, add reviews, show stock availability'
            })
        
        if funnel['cart_to_checkout_rate'] < 60:
            bottlenecks.append({
                'stage': 'Cart to Checkout',
                'drop_off_rate': 100 - funnel['cart_to_checkout_rate'],
                'severity': 'High' if (100 - funnel['cart_to_checkout_rate']) > 40 else 'Medium',
                'recommendation': 'Show shipping costs early, add trust badges, simplify cart view'
            })
        
        if funnel['checkout_to_purchase_rate'] < 70:
            bottlenecks.append({
                'stage': 'Checkout to Purchase',
                'drop_off_rate': 100 - funnel['checkout_to_purchase_rate'],
                'severity': 'Critical' if (100 - funnel['checkout_to_purchase_rate']) > 30 else 'High',
                'recommendation': 'Reduce checkout steps, add guest checkout, show security seals, optimize payment options'
            })
        
        return sorted(bottlenecks, key=lambda x: x['drop_off_rate'], reverse=True)
    
    def calculate_customer_lifetime_metrics(self):
        """Calculate CLV and related metrics"""
        
        user_metrics = self.df.groupby('user_id').agg({
            'session_id': 'count',
            'completed_purchase': 'sum',
            'revenue': 'sum',
            'timestamp': ['min', 'max']
        }).reset_index()
        
        user_metrics.columns = ['user_id', 'total_sessions', 'total_purchases', 
                               'total_revenue', 'first_visit', 'last_visit']
        
        # Calculate days active
        user_metrics['days_active'] = (pd.to_datetime(user_metrics['last_visit']) - 
                                       pd.to_datetime(user_metrics['first_visit'])).dt.days + 1
        
        # Metrics
        avg_sessions_per_user = user_metrics['total_sessions'].mean()
        avg_purchases_per_user = user_metrics['total_purchases'].mean()
        avg_revenue_per_user = user_metrics['total_revenue'].mean()
        avg_days_active = user_metrics['days_active'].mean()
        
        # Customer segments
        segments = {
            'one_time_buyers': len(user_metrics[user_metrics['total_purchases'] == 1]),
            'repeat_buyers': len(user_metrics[user_metrics['total_purchases'] > 1]),
            'high_value_customers': len(user_metrics[user_metrics['total_revenue'] > user_metrics['total_revenue'].quantile(0.75)]),
        }
        
        return {
            'avg_sessions_per_user': round(avg_sessions_per_user, 2),
            'avg_purchases_per_user': round(avg_purchases_per_user, 2),
            'avg_revenue_per_user': round(avg_revenue_per_user, 2),
            'avg_days_active': round(avg_days_active, 2),
            'customer_segments': segments,
            'estimated_clv': round(avg_revenue_per_user * 12, 2)  # Annualized estimate
        }
    
    def get_conversion_trends(self, period='daily'):
        """Analyze conversion trends over time"""
        
        if period == 'daily':
            trends = self.df.groupby('date').agg({
                'session_id': 'count',
                'completed_purchase': 'sum',
                'revenue': 'sum',
                'added_to_cart': 'sum',
                'started_checkout': 'sum'
            }).reset_index()
            
            trends.columns = ['date', 'sessions', 'conversions', 'revenue', 
                            'carts', 'checkouts']
        
        elif period == 'weekly':
            self.df['week'] = self.df['date'].dt.isocalendar().week
            trends = self.df.groupby('week').agg({
                'session_id': 'count',
                'completed_purchase': 'sum',
                'revenue': 'sum'
            }).reset_index()
            
            trends.columns = ['week', 'sessions', 'conversions', 'revenue']
        
        # Calculate rates
        trends['conversion_rate'] = (trends['conversions'] / trends['sessions'] * 100).round(2)
        
        if 'carts' in trends.columns:
            trends['cart_abandonment'] = ((trends['carts'] - trends['conversions']) / 
                                         trends['carts'] * 100).round(2)
        
        return trends
