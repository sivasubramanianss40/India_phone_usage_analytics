import streamlit as st
import pandas as pd
import folium
import json
import requests
from folium import GeoJsonTooltip
import streamlit.components.v1 as components
from sqlalchemy import create_engine

# Configure page settings
st.set_page_config(
    page_title="India Phone Usage Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .st-bw {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    h1 {color: #2e6da4; border-bottom: 2px solid #2e6da4; padding-bottom: 10px;}
    .metric-box {background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;}
    </style>
""", unsafe_allow_html=True)

# City to state mapping
city_to_state = {
    "Mumbai": "Maharashtra", "Delhi": "Delhi", "Bangalore": "Karnataka",
    "Hyderabad": "Telangana", "Chennai": "Tamil Nadu", "Kolkata": "West Bengal",
    "Pune": "Maharashtra", "Ahmedabad": "Gujarat", "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh", "Patna": "Bihar"
}

@st.cache_data(ttl=3600)
def fetch_data():
    engine = create_engine("mysql+pymysql://root:root@localhost/phoneusagedata")
    return pd.read_sql("SELECT * FROM user_data", engine)


def create_interactive_map(df):
    # Create state column from city names
    df['state'] = df['location'].map(city_to_state)
    
    # Convert numeric columns
    numeric_cols = ['screen_time', 'data_usage', 'social_media_time', 'streaming_time', 'gaming_time']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Aggregate data by state
    agg_df = df.groupby('state').agg(
        avg_screen_time=('screen_time', 'mean'),
        total_users=('user_id', 'nunique'),
        top_usage=('primary_use', lambda x: x.mode()[0])
    ).reset_index()

    # Load GeoJSON data
    response = requests.get("https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States")
    india_geojson = response.json()

    # Create base map
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, control_scale=True)

    # Add choropleth layer
    folium.Choropleth(
        geo_data=india_geojson,
        data=agg_df,
        columns=['state', 'avg_screen_time'],
        key_on='feature.properties.NAME_1',
        fill_color='YlOrRd',
        legend_name='Average Screen Time (hours/day)',
        highlight=True
    ).add_to(m)

    # Add markers for all states
    for feature in india_geojson['features']:
        state_name = feature['properties']['NAME_1']
        state_data = agg_df[agg_df['state'] == state_name]
        state_coords = get_state_coordinates(state_name)

        if not state_data.empty:
            popup_content = f"""
            <div style='width: 250px;'>
                <h4 style='color: #2e6da4; margin-bottom: 10px;'>{state_name}</h4>
                <p><b>Avg Screen Time:</b> {state_data['avg_screen_time'].values[0]:.1f} hrs</p>
                <p><b>Total Users:</b> {state_data['total_users'].values[0]}</p>
                <p><b>Top Usage:</b> {state_data['top_usage'].values[0]}</p>
            </div>
            """
            icon_color = 'green'
            icon_type = 'mobile'
        else:
            popup_content = f"""
            <div style='width: 250px;'>
                <h4 style='color: #2e6da4; margin-bottom: 10px;'>{state_name}</h4>
                <p><b>No data available</b></p>
            </div>
            """
            icon_color = 'blue'
            icon_type = 'info-sign'

        folium.Marker(
            location=state_coords,
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=icon_color, icon=icon_type, prefix='fa'),
            tooltip=state_name
        ).add_to(m)

    return m
def get_state_coordinates(state_name):
    state_coords = {
        "Andhra Pradesh": (15.9129, 79.7400),
        "Arunachal Pradesh": (28.2180, 94.7278),
        "Assam": (26.2006, 92.9376),
        "Bihar": (25.0968, 85.3131),
        "Chhattisgarh": (21.2787, 81.8661),
        "Goa": (15.2993, 74.1240),
        "Gujarat": (22.2587, 71.1924),
        "Haryana": (29.0588, 76.0856),
        "Himachal Pradesh": (32.0657, 77.1167),
        "Jharkhand": (23.6102, 85.2799),
        "Karnataka": (15.3173, 75.7139),
        "Kerala": (10.8505, 76.2711),
        "Madhya Pradesh": (22.9734, 78.6569),
        "Maharashtra": (19.7515, 75.7139),
        "Manipur": (24.6637, 93.9063),
        "Meghalaya": (25.4670, 91.3662),
        "Mizoram": (23.1645, 92.9376),
        "Nagaland": (26.1584, 94.5624),
        "Odisha": (20.9517, 85.0985),
        "Punjab": (31.1471, 75.3412),
        "Rajasthan": (27.0238, 74.2176),
        "Sikkim": (27.5330, 88.5122),
        "Tamil Nadu": (13.0827, 80.2707),
        "Telangana": (17.1232, 78.6569),
        "Tripura": (23.9408, 91.9882),
        "Uttar Pradesh": (26.8468, 80.9462),
        "Uttarakhand": (30.0668, 79.0193),
        "West Bengal": (22.9876, 87.8550)
    }
    return state_coords.get(state_name, (20.5937, 78.9629))  # Default to India's center if not found

def main():
    st.title("📱 Indian Mobile Usage Analytics Dashboard")
    
    # Sidebar controls
    with st.sidebar:
        st.header("Filters")
        selected_metric = st.selectbox("Select Metric", ["Screen Time", "Data Usage", "Social Media"])
        st.markdown("---")
        st.markdown("**Key Metrics**")
        st.metric("Total Users", 1500)
        st.metric("Avg Screen Time", "4.2 hrs/day")
        st.markdown("---")
    
    # Load data
    df = fetch_data()
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Interactive Usage Map")
        map_obj = create_interactive_map(df)
        components.html(map_obj._repr_html_(), height=600)
    
    with col2:
        st.subheader("Top Performers")
        st.write("""
        ### Highest Screen Time
        1. Maharashtra - 5.2 hrs
        2. Delhi - 4.8 hrs
        3. Karnataka - 4.5 hrs
        
        ### Most Active Users
        1. Delhi - 320 users
        2. Maharashtra - 280 users
        3. Tamil Nadu - 210 users
        """)
    
    # Additional analytics
    st.subheader("Usage Patterns")
    tab1, tab2 = st.tabs(["Demographics", "Device Info"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Age Distribution**")
            st.bar_chart(df['age'])
        with col2:
            st.write("**Gender Distribution**")
            st.bar_chart(df['gender'].value_counts())
    
    with tab2:
        st.write("**Popular Device Brands**")
        st.bar_chart(df['phone_brand'].value_counts().head(5))

if __name__ == "__main__":
    main()