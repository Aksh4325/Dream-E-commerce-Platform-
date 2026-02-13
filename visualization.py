"""
Visualization Module
Generate all charts and graphs for e-commerce analytics
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import os


class EcommerceVisualizer:
    """Create visualizations for e-commerce analytics"""
    
    def __init__(self, sessions_df, output_dir='output'):
        self.df = sessions_df
        self.output_dir = output_dir
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
        
        # Colors
        self.colors = {
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#9b59b6'
        }
    
    def plot_conversion_funnel(self, funnel_data):
        """Plot conversion funnel waterfall chart"""
        
        fig = go.Figure()
        
        stages = funnel_data['stage'].tolist()
        users = funnel_data['users'].tolist()
        percentages = funnel_data['percentage'].tolist()
        
        # Create funnel
        fig.add_trace(go.Funnel(
            y=stages,
            x=users,
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(
                color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
            ),
            connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}}
        ))
        
        fig.update_layout(
            title={
                'text': 'E-Commerce Conversion Funnel',
                'font': {'size': 24, 'family': 'Arial Black'}
            },
            height=600,
            showlegend=False
        )
        
        filename = f'{self.output_dir}/conversion_funnel.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
        
        # Also save as PNG
        plt.figure(figsize=(12, 8))
        plt.barh(stages, users, color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6'])
        plt.xlabel('Number of Users', fontsize=12)
        plt.title('Conversion Funnel', fontsize=16, fontweight='bold')
        plt.gca().invert_yaxis()
        
        for i, (user, pct) in enumerate(zip(users, percentages)):
            plt.text(user, i, f'  {user:,} ({pct}%)', va='center', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/conversion_funnel.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_traffic_source_breakdown(self, traffic_data):
        """Plot traffic source distribution"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=traffic_data['traffic_source'],
            values=traffic_data['sessions'],
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3),
            textposition='auto',
            textinfo='label+percent'
        ))
        
        fig.update_layout(
            title='Traffic Source Distribution',
            height=500
        )
        
        filename = f'{self.output_dir}/traffic_sources.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def plot_cart_abandonment_trend(self, daily_data):
        """Plot cart abandonment over time"""
        
        daily_data = daily_data.copy()
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        
        # Calculate cart abandonment
        if 'carts' in daily_data.columns:
            daily_data['abandonment_rate'] = ((daily_data['carts'] - daily_data['conversions']) / 
                                              daily_data['carts'] * 100)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data.get('abandonment_rate', []),
            mode='lines+markers',
            name='Cart Abandonment Rate',
            line=dict(color='#e74c3c', width=2),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title='Cart Abandonment Rate Over Time',
            xaxis_title='Date',
            yaxis_title='Abandonment Rate (%)',
            height=500,
            hovermode='x unified'
        )
        
        filename = f'{self.output_dir}/cart_abandonment_trend.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def plot_hourly_heatmap(self, hourly_data):
        """Plot hourly session heatmap"""
        
        # Create day of week data
        self.df['day_of_week'] = pd.to_datetime(self.df['timestamp']).dt.day_name()
        
        heatmap_data = self.df.groupby(['day_of_week', 'hour']).size().reset_index(name='sessions')
        heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='hour', values='sessions')
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex(day_order)
        
        plt.figure(figsize=(16, 6))
        sns.heatmap(heatmap_pivot, cmap='YlOrRd', annot=False, fmt='g', 
                   cbar_kws={'label': 'Sessions'})
        plt.title('Hourly Session Heatmap', fontsize=16, fontweight='bold')
        plt.xlabel('Hour of Day', fontsize=12)
        plt.ylabel('Day of Week', fontsize=12)
        plt.tight_layout()
        
        filename = f'{self.output_dir}/hourly_heatmap.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_device_performance(self, device_data):
        """Plot device-wise performance"""
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Sessions by Device', 'Conversion Rate by Device'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Sessions
        fig.add_trace(
            go.Bar(x=device_data['device'], y=device_data['sessions'], 
                   marker_color='#3498db', name='Sessions'),
            row=1, col=1
        )
        
        # Conversion rate
        fig.add_trace(
            go.Bar(x=device_data['device'], y=device_data['conversion_rate'],
                   marker_color='#2ecc71', name='Conversion Rate'),
            row=1, col=2
        )
        
        fig.update_layout(height=500, showlegend=False, title_text='Device Performance Analysis')
        
        filename = f'{self.output_dir}/device_performance.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def plot_revenue_by_category(self, category_data):
        """Plot revenue by product category"""
        
        plt.figure(figsize=(12, 6))
        plt.bar(category_data['category'], category_data['total_revenue'], 
               color=sns.color_palette('viridis', len(category_data)))
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Revenue (₹)', fontsize=12)
        plt.title('Revenue by Product Category', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        
        for i, v in enumerate(category_data['total_revenue']):
            plt.text(i, v, f'₹{v:,.0f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        filename = f'{self.output_dir}/revenue_by_category.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_traffic_source_roi(self, traffic_data):
        """Plot ROI by traffic source"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=traffic_data['traffic_source'],
            y=traffic_data['roi_percent'],
            marker=dict(
                color=traffic_data['roi_percent'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="ROI %")
            ),
            text=traffic_data['roi_percent'].round(1),
            textposition='outside'
        ))
        
        fig.update_layout(
            title='ROI by Traffic Source',
            xaxis_title='Traffic Source',
            yaxis_title='ROI (%)',
            height=500
        )
        
        filename = f'{self.output_dir}/traffic_roi.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def plot_conversion_trends(self, daily_data):
        """Plot conversion rate trends"""
        
        daily_data = daily_data.copy()
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Sessions
        fig.add_trace(
            go.Scatter(x=daily_data['date'], y=daily_data['sessions'],
                      name='Sessions', line=dict(color='#3498db')),
            secondary_y=False
        )
        
        # Conversion rate
        fig.add_trace(
            go.Scatter(x=daily_data['date'], y=daily_data['conversion_rate'],
                      name='Conversion Rate', line=dict(color='#2ecc71', width=3)),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Sessions', secondary_y=False)
        fig.update_yaxes(title_text='Conversion Rate (%)', secondary_y=True)
        
        fig.update_layout(
            title='Daily Sessions and Conversion Rate',
            height=500,
            hovermode='x unified'
        )
        
        filename = f'{self.output_dir}/conversion_trends.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def plot_weekday_performance(self, weekday_data):
        """Plot performance by day of week"""
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_data['day_of_week'] = pd.Categorical(weekday_data['day_of_week'], 
                                                      categories=day_order, ordered=True)
        weekday_data = weekday_data.sort_values('day_of_week')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Sessions
        ax1.bar(weekday_data['day_of_week'], weekday_data['sessions'], color='#3498db')
        ax1.set_xlabel('Day of Week', fontsize=12)
        ax1.set_ylabel('Sessions', fontsize=12)
        ax1.set_title('Sessions by Day of Week', fontsize=14, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        
        # Revenue
        ax2.bar(weekday_data['day_of_week'], weekday_data['revenue'], color='#2ecc71')
        ax2.set_xlabel('Day of Week', fontsize=12)
        ax2.set_ylabel('Revenue (₹)', fontsize=12)
        ax2.set_title('Revenue by Day of Week', fontsize=14, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        filename = f'{self.output_dir}/weekday_performance.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_customer_segmentation(self, returning_data):
        """Plot new vs returning customers"""
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Sessions Distribution', 'Revenue Distribution'),
            specs=[[{'type': 'pie'}, {'type': 'pie'}]]
        )
        
        # Sessions pie
        fig.add_trace(
            go.Pie(labels=returning_data['customer_type'], values=returning_data['sessions'],
                   hole=0.3, marker=dict(colors=['#3498db', '#2ecc71'])),
            row=1, col=1
        )
        
        # Revenue pie
        fig.add_trace(
            go.Pie(labels=returning_data['customer_type'], values=returning_data['total_revenue'],
                   hole=0.3, marker=dict(colors=['#3498db', '#2ecc71'])),
            row=1, col=2
        )
        
        fig.update_layout(height=500, title_text='New vs Returning Customers')
        
        filename = f'{self.output_dir}/customer_segmentation.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def plot_revenue_distribution(self, sessions_df):
        """Plot revenue distribution"""
        
        purchases = sessions_df[sessions_df['completed_purchase'] == True]['revenue']
        
        plt.figure(figsize=(12, 6))
        plt.hist(purchases, bins=30, color='#2ecc71', edgecolor='black', alpha=0.7)
        plt.xlabel('Order Value (₹)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Revenue Distribution', fontsize=16, fontweight='bold')
        plt.axvline(purchases.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ₹{purchases.mean():.2f}')
        plt.axvline(purchases.median(), color='blue', linestyle='--', linewidth=2, label=f'Median: ₹{purchases.median():.2f}')
        plt.legend()
        plt.tight_layout()
        
        filename = f'{self.output_dir}/revenue_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_location_performance(self, location_data):
        """Plot geographic performance"""
        
        location_data = location_data.sort_values('total_revenue', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=location_data['location'],
            x=location_data['total_revenue'],
            orientation='h',
            marker=dict(
                color=location_data['total_revenue'],
                colorscale='Viridis',
                showscale=True
            ),
            text=location_data['total_revenue'].apply(lambda x: f'₹{x:,.0f}'),
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Revenue by Location',
            xaxis_title='Revenue (₹)',
            yaxis_title='Location',
            height=600
        )
        
        filename = f'{self.output_dir}/location_performance.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def plot_session_duration_analysis(self, sessions_df):
        """Plot session duration vs conversion"""
        
        # Create duration buckets
        sessions_df['duration_minutes'] = sessions_df['session_duration_seconds'] / 60
        
        fig = go.Figure()
        
        # Converted sessions
        converted = sessions_df[sessions_df['completed_purchase'] == True]
        fig.add_trace(go.Box(
            y=converted['duration_minutes'],
            name='Converted',
            marker_color='#2ecc71'
        ))
        
        # Non-converted sessions
        not_converted = sessions_df[sessions_df['completed_purchase'] == False]
        fig.add_trace(go.Box(
            y=not_converted['duration_minutes'],
            name='Not Converted',
            marker_color='#e74c3c'
        ))
        
        fig.update_layout(
            title='Session Duration: Converted vs Non-Converted',
            yaxis_title='Duration (minutes)',
            height=500
        )
        
        filename = f'{self.output_dir}/session_duration_analysis.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
    
    def create_kpi_dashboard(self, overall_metrics):
        """Create KPI summary dashboard"""
        
        fig = go.Figure()
        
        kpis = [
            {'name': 'Total Sessions', 'value': f"{overall_metrics['total_sessions'].values[0]:,}"},
            {'name': 'Conversions', 'value': f"{overall_metrics['conversions'].values[0]:,}"},
            {'name': 'Conversion Rate', 'value': f"{overall_metrics['conversion_rate'].values[0]}%"},
            {'name': 'Bounce Rate', 'value': f"{overall_metrics['bounce_rate'].values[0]}%"},
            {'name': 'Total Revenue', 'value': f"₹{overall_metrics['total_revenue'].values[0]:,.2f}"},
            {'name': 'ROI', 'value': f"{overall_metrics['overall_roi'].values[0]}%"}
        ]
        
        # Create table
        fig = go.Figure(data=[go.Table(
            header=dict(values=['<b>Metric</b>', '<b>Value</b>'],
                       fill_color='#3498db',
                       align='left',
                       font=dict(color='white', size=14)),
            cells=dict(values=[[kpi['name'] for kpi in kpis], 
                              [kpi['value'] for kpi in kpis]],
                      fill_color='lavender',
                      align='left',
                      font=dict(size=12),
                      height=30))
        ])
        
        fig.update_layout(
            title='Key Performance Indicators',
            height=400
        )
        
        filename = f'{self.output_dir}/kpi_dashboard.html'
        fig.write_html(filename)
        print(f"✓ Saved: {filename}")
