import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Set page config with modern title and icon
st.set_page_config(
    page_title="Train Enquiry & Analytics System",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using injected CSS (Neon Cyberpunk & Glassmorphism)
st.markdown("""
<style>
    /* Main Background & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background-color: #050B14;
        color: #E2E8F0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #090E17 !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
    }
    
    /* Headers & Text colors */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    .main-title {
        background: linear-gradient(135deg, #FF007F 0%, #7928CA 50%, #00F2FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        margin-bottom: 0.25rem !important;
        font-weight: 700 !important;
        letter-spacing: -1.5px;
        line-height: 1.2;
    }
    
    .branding-sub {
        font-size: 1.25rem;
        font-weight: 600;
        letter-spacing: 2px;
        color: #00F2FE;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.3);
    }
    
    /* Glowing Glassmorphism Cards */
    .premium-card {
        background: rgba(13, 20, 35, 0.65);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #FF007F, #7928CA, #00F2FE);
        opacity: 0.8;
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 242, 254, 0.4);
        box-shadow: 0 25px 45px -15px rgba(0, 242, 254, 0.25);
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00F2FE;
        line-height: 1;
        margin-top: 0.5rem;
        text-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Tabs customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(9, 14, 23, 0.6);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(0, 242, 254, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 600;
        border: none;
        padding: 0 25px;
        transition: all 0.3s;
        font-size: 1rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC;
        background-color: rgba(255, 255, 255, 0.04);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(121, 40, 202, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%);
        color: #00F2FE;
        border: 1px solid rgba(0, 242, 254, 0.3);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.15);
    }
    
    /* Timeline styles */
    .timeline-item {
        border-left: 2px solid #1E293B;
        margin-left: 10px;
        padding-left: 24px;
        padding-bottom: 24px;
        position: relative;
    }
    
    .timeline-item-active {
        border-left: 2px solid #00F2FE;
    }
    
    .timeline-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background-color: #1E293B;
        position: absolute;
        left: -8px;
        top: 6px;
        border: 3px solid #050B14;
    }
    
    .timeline-dot-active {
        background-color: #00F2FE;
        box-shadow: 0 0 10px #00F2FE, 0 0 5px #00F2FE;
    }
    
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING & CACHING -----------------

@st.cache_data
def load_datasets():
    # Clean schedule dataset
    df_clean = pd.read_csv("Dataset1_Clean.csv", keep_default_na=False)
    
    # Train summaries
    df_durations = pd.read_csv("train_duration_summary.csv")
    
    # Station frequencies
    df_traffic = pd.read_csv("station_traffic.csv")
    
    return df_clean, df_durations, df_traffic

try:
    df_clean, df_durations, df_traffic = load_datasets()
    data_loaded = True
except Exception as e:
    data_loaded = False
    st.error(f"Failed to load datasets. Please verify that Level 2 and 3 scripts have been run! Details: {e}")

# ----------------- HELPER FUNCTIONS -----------------

def calculate_leg_duration(df_train_stops, source_sn, dest_sn):
    """Slices stops from source_sn to dest_sn and calculates exact journey duration in minutes"""
    stops = df_train_stops[(df_train_stops['SN'] >= source_sn) & (df_train_stops['SN'] <= dest_sn)].to_dict('records')
    if not stops:
        return 0
    
    total_minutes = 0
    prev_dep = stops[0]['Departure_Time']
    
    for i in range(1, len(stops)):
        arr = stops[i]['Arrival_time']
        dep = stops[i]['Departure_Time']
        
        # 1. Travel Leg: from previous departure to current arrival
        t_prev_dep = datetime.strptime(prev_dep, '%H:%M:%S')
        t_arr = datetime.strptime(arr, '%H:%M:%S')
        diff = (t_arr - t_prev_dep).total_seconds() / 60.0
        if diff < 0:
            diff += 1440 # Account for midnight rollover
        total_minutes += diff
        
        # 2. Halt Leg: intermediate halt at station
        if i < len(stops) - 1:
            t_dep = datetime.strptime(dep, '%H:%M:%S')
            diff_halt = (t_dep - t_arr).total_seconds() / 60.0
            if diff_halt < 0:
                diff_halt += 1440
            total_minutes += diff_halt
            prev_dep = dep
            
    return total_minutes

def estimate_fare(distance_km, source_row, dest_row, cls_col):
    """Subtracts cumulative fares, falls back to distance pricing if negative or base price"""
    try:
        source_val = float(source_row[cls_col])
        dest_val = float(dest_row[cls_col])
        diff = dest_val - source_val
        if diff > 0:
            return max(50.0, diff)
    except:
        pass
        
    # Distance-based fallbacks
    rates = {'SL': 1.2, '3A': 2.5, '2A': 4.0, '1A': 6.5}
    base_fares = {'SL': 60, '3A': 250, '2A': 450, '1A': 750}
    return base_fares[cls_col] + round(distance_km * rates[cls_col])

# ----------------- UI ASSEMBLY -----------------

if data_loaded:
    # Sidebar Network Stats Dashboard
    st.sidebar.markdown("<h3 style='margin-bottom:0.25rem;color:#00F2FE;'>📁 SYSTEM ARCHIVE</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size:0.8rem;color:#64748B;margin-bottom:1.5rem;'>TRAIN METRICS PANEL</p>", unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div class="premium-card" style="padding:1.1rem; margin-bottom:0.75rem; border-color:rgba(255, 0, 127, 0.25);">
        <div class="metric-label" style="color:#FF007F;">Total Train Runs</div>
        <div class="metric-value" style="font-size:1.85rem;color:#FF007F;text-shadow:0 0 10px rgba(255, 0, 127, 0.3);">{len(df_durations):,}</div>
    </div>
    <div class="premium-card" style="padding:1.1rem; margin-bottom:0.75rem; border-color:rgba(121, 40, 202, 0.25);">
        <div class="metric-label" style="color:#A78BFA;">Busiest Transit Hubs</div>
        <div class="metric-value" style="font-size:1.85rem;color:#A78BFA;text-shadow:0 0 10px rgba(121, 40, 202, 0.3);">{len(df_traffic):,}</div>
    </div>
    <div class="premium-card" style="padding:1.1rem; margin-bottom:0.75rem; border-color:rgba(0, 242, 254, 0.25);">
        <div class="metric-label" style="color:#00F2FE;">Total Station Stops</div>
        <div class="metric-value" style="font-size:1.85rem;color:#00F2FE;text-shadow:0 0 10px rgba(0, 242, 254, 0.3);">{len(df_clean):,}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Submission Deliverables")
    st.sidebar.markdown("""
    - [x] Level 1: Basic Review
    - [x] Level 2: Simple Processing
    - [x] Level 3: Data Quality
    - [x] Level 4: Basic Analytics
    - [x] Level 5: Advanced Pivot
    - [x] Level 6: Capstone App
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("<small style='color:#475569;'>Antigravity Portal v1.5<br>© Sysslan IT Solutions</small>", unsafe_allow_html=True)
    
    # Main Header
    st.markdown("<h1 class='main-title'>TRAIN ENQUIRY & ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("<div class='branding-sub'>Sysslan IT Solutions • Data Analysis Capstone</div>", unsafe_allow_html=True)
    
    # Tab Layout
    tab1, tab2, tab3 = st.tabs([
        "🔍 Train Route Finder", 
        "📊 Network Analytics Explorer", 
        "🚉 Station Traffic Explorer"
    ])
    
    # ----------------- TAB 1: TRAIN ROUTE FINDER -----------------
    with tab1:
        st.markdown("<h3 style='margin-top:1rem;'>Search Direct Trains Between Cities</h3>", unsafe_allow_html=True)
        
        # Prepare list of stations: "Station Name (Station Code)"
        station_list = sorted(
            [f"{row['Station_Name']} ({row['Station_Code']})" for idx, row in df_traffic.iterrows()]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            source_input = st.selectbox("Select Origin Station:", station_list, index=station_list.index("SAWANTWADI R (SWV)") if "SAWANTWADI R (SWV)" in station_list else 0)
        with col2:
            dest_input = st.selectbox("Select Destination Station:", station_list, index=station_list.index("MADGOAN JN. (MAO)") if "MADGOAN JN. (MAO)" in station_list else 1)
            
        # Parse station codes
        source_code = source_input.split("(")[-1].replace(")", "").strip()
        dest_code = dest_input.split("(")[-1].replace(")", "").strip()
        
        if source_code == dest_code:
            st.warning("Origin and Destination stations must be different!")
        else:
            # Query direct trains
            trains_at_source = df_clean[df_clean["Station_Code"] == source_code]
            trains_at_dest = df_clean[df_clean["Station_Code"] == dest_code]
            
            # Find common Train_Nos
            common_trains = set(trains_at_source["Train_No"]).intersection(set(trains_at_dest["Train_No"]))
            
            direct_trains = []
            
            for train_no in common_trains:
                train_schedule = df_clean[df_clean["Train_No"] == train_no].sort_values("SN")
                
                source_stop = train_schedule[train_schedule["Station_Code"] == source_code].iloc[0]
                dest_stop = train_schedule[train_schedule["Station_Code"] == dest_code].iloc[0]
                
                # Direct route criteria: departure from source before arrival at destination
                if source_stop["SN"] < dest_stop["SN"]:
                    # Compute duration between the two stations
                    duration_minutes = calculate_leg_duration(train_schedule, source_stop["SN"], dest_stop["SN"])
                    distance_traveled = dest_stop["Distance"] - source_stop["Distance"]
                    
                    # Class-wise fares
                    fare_sl = estimate_fare(distance_traveled, source_stop, dest_stop, 'SL')
                    fare_3a = estimate_fare(distance_traveled, source_stop, dest_stop, '3A')
                    fare_2a = estimate_fare(distance_traveled, source_stop, dest_stop, '2A')
                    fare_1a = estimate_fare(distance_traveled, source_stop, dest_stop, '1A')
                    
                    direct_trains.append({
                        "Train_No": train_no,
                        "Start_Departure": source_stop["Departure_Time"],
                        "End_Arrival": dest_stop["Arrival_time"],
                        "Distance_KM": distance_traveled,
                        "Stops_Count": dest_stop["SN"] - source_stop["SN"] - 1,
                        "Duration_Minutes": duration_minutes,
                        "Duration_Hours": duration_minutes / 60.0,
                        "Fare_SL": fare_sl,
                        "Fare_3A": fare_3a,
                        "Fare_2A": fare_2a,
                        "Fare_1A": fare_1a,
                        "Source_SN": source_stop["SN"],
                        "Dest_SN": dest_stop["SN"]
                    })
            
            if not direct_trains:
                st.markdown(f"""
                <div class="premium-card" style="border-color: rgba(239, 68, 68, 0.35); background: rgba(239, 68, 68, 0.05); margin-top: 1rem;">
                    <div style="color: #F87171; font-weight: 700; font-size: 1.15rem;">No Direct Route Found</div>
                    <div style="color: #94A3B8; font-size:0.95rem; margin-top:0.4rem;">There are no direct train routes operating from <b>{source_input.split(" (")[0]}</b> to <b>{dest_input.split(" (")[0]}</b>. Please check alternate hubs.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"Found **{len(direct_trains)}** direct trains between these stations:")
                
                df_results = pd.DataFrame(direct_trains).sort_values("Start_Departure")
                
                for idx, row in df_results.iterrows():
                    hours_int = int(row['Duration_Hours'])
                    mins_int = int(row['Duration_Minutes'] % 60)
                    duration_str = f"{hours_int} hrs {mins_int} mins" if hours_int > 0 else f"{mins_int} mins"
                    
                    expander_label = f"🚆 Train No: {row['Train_No']} | Departs: {row['Start_Departure']} ➔ Arrives: {row['End_Arrival']} | Duration: {duration_str} | Distance: {row['Distance_KM']} km"
                    
                    with st.expander(expander_label):
                        # Fares and statistics columns
                        col_fa, col_fb, col_fc, col_fd = st.columns(4)
                        with col_fa:
                            st.markdown(f"""
                            <div class="premium-card" style="padding:1rem; border-color: rgba(255, 0, 127, 0.25);">
                                <div class="metric-label">Sleeper Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#FF007F; text-shadow:0 0 10px rgba(255,0,127,0.3);">₹{row['Fare_SL']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_fb:
                            st.markdown(f"""
                            <div class="premium-card" style="padding:1rem; border-color: rgba(121, 40, 202, 0.25);">
                                <div class="metric-label">3 AC Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#A78BFA; text-shadow:0 0 10px rgba(121,40,202,0.3);">₹{row['Fare_3A']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_fc:
                            st.markdown(f"""
                            <div class="premium-card" style="padding:1rem; border-color: rgba(0, 242, 254, 0.25);">
                                <div class="metric-label">2 AC Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#00F2FE; text-shadow:0 0 10px rgba(0,242,254,0.3);">₹{row['Fare_2A']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_fd:
                            st.markdown(f"""
                            <div class="premium-card" style="padding:1rem; border-color: rgba(16, 185, 129, 0.25);">
                                <div class="metric-label">1 AC Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#10B981; text-shadow:0 0 10px rgba(16,185,129,0.3);">₹{row['Fare_1A']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        # Show entire itinerary timeline
                        st.markdown("<h4 style='margin-top:1.5rem;margin-bottom:1rem;'>Full Route Itinerary Timeline</h4>", unsafe_allow_html=True)
                        
                        full_sched = df_clean[df_clean["Train_No"] == row["Train_No"]].sort_values("SN")
                        
                        timeline_html = "<div style='margin-top:0.5rem; margin-bottom:1.5rem;'>"
                        for s_idx, s_row in full_sched.iterrows():
                            is_active = (s_row["SN"] >= row["Source_SN"]) & (s_row["SN"] <= row["Dest_SN"])
                            active_class = "timeline-item-active" if is_active else ""
                            dot_active = "timeline-dot-active" if is_active else ""
                            label_weight = "font-weight: 700; color:#F8FAFC;" if is_active else "color:#64748B;"
                            
                            timing_str = f"Arrives: {s_row['Arrival_time']} | Departs: {s_row['Departure_Time']}"
                            if s_row["SN"] == 1:
                                timing_str = f"Starts (Departure): {s_row['Departure_Time']}"
                            elif s_row["SN"] == full_sched["SN"].max():
                                timing_str = f"Terminates (Arrival): {s_row['Arrival_time']}"
                                
                            badge_html = ""
                            if s_row["SN"] == row["Source_SN"]:
                                badge_html = " <span style='background:#10B981; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;'>DEPART FROM</span>"
                            elif s_row["SN"] == row["Dest_SN"]:
                                badge_html = " <span style='background:#EF4444; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;'>ARRIVE AT</span>"
                                
                            timeline_html += f"""<div class="timeline-item {active_class}">
<div class="timeline-dot {dot_active}"></div>
<div style="{label_weight} font-size:0.95rem;">
Stop {s_row['SN']}: {s_row['Station_Name']} ({s_row['Station_Code']}) - {s_row['Distance']} km{badge_html}
</div>
<div style="color:#94A3B8; font-size:0.85rem; margin-top:2px;">{timing_str}</div>
</div>"""
                        timeline_html += "</div>"
                        st.markdown(timeline_html, unsafe_allow_html=True)
                        
    # ----------------- TAB 2: NETWORK ANALYTICS EXPLORER -----------------
    with tab2:
        st.markdown("<h3 style='margin-top:1rem;'>Exploratory & Advanced Visualizations Center</h3>", unsafe_allow_html=True)
        
        vis_tab1, vis_tab2 = st.tabs(["📈 Basic Network Trends", "🧬 Advanced Corridor Pivot/Crosstabs"])
        
        with vis_tab1:
            st.markdown("#### Operational Overview and Station Traffic Density")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                <div class="premium-card" style="margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 1.15rem; color:#00F2FE;">Top 10 Busiest Junctions</div>
                    <div style="color: #94A3B8; font-size:0.9rem; margin-top:0.25rem;">Visualizes traffic densities. CSMT and suburban junctions represent extreme traffic concentrations.</div>
                </div>
                """, unsafe_allow_html=True)
                if os.path.exists("visualizations/top_stations_traffic.png"):
                    st.image("visualizations/top_stations_traffic.png", use_container_width=True)
                else:
                    st.warning("Visualizations not found. Please run the Level 4 analysis script first!")
                    
            with col_b:
                st.markdown("""
                <div class="premium-card" style="margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 1.15rem; color:#00F2FE;">Overall Train Journey Durations</div>
                    <div style="color: #94A3B8; font-size:0.9rem; margin-top:0.25rem;">Shows skewed distribution curve with a massive peak at low durations, indicating dominant commuter local networks.</div>
                </div>
                """, unsafe_allow_html=True)
                if os.path.exists("visualizations/duration_distribution.png"):
                    st.image("visualizations/duration_distribution.png", use_container_width=True)
                else:
                    st.warning("Visualizations not found!")
                    
            st.markdown("---")
            st.markdown("#### Average Durations across classifications")
            col_x, col_y = st.columns([1, 2])
            with col_x:
                st.markdown("""
                <div class="premium-card" style="margin-top:1rem;">
                    <div style="font-weight: 700; font-size: 1.15rem; color:#FF007F; text-shadow:0 0 10px rgba(255,0,127,0.2);">Route Classifications</div>
                    <div style="color: #E2E8F0; font-size:0.9rem; margin-top:0.5rem; line-height:1.6;">
                        * <b>Short Routes (<= 100 km)</b>: Average duration ~ 1.29 hours, represents high-speed local shuttle networks.
                        <br><br>
                        * <b>Medium Routes (101 - 500 km)</b>: Average duration ~ 5.56 hours, typical inter-city interlinks.
                        <br><br>
                        * <b>Long Routes (> 500 km)</b>: Average duration ~ 25.78 hours, multi-day cross-country sub-continental lines.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_y:
                if os.path.exists("visualizations/avg_duration_by_route.png"):
                    st.image("visualizations/avg_duration_by_route.png", use_container_width=True)
                else:
                    st.warning("Visualization not found!")
                    
        with vis_tab2:
            st.markdown("#### Pivot Matrices & Thermal Density Heatmaps")
            col_c, col_d = st.columns(2)
            with col_c:
                st.markdown("""
                <div class="premium-card" style="margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 1.15rem; color:#00F2FE;">Station Traffic Route Composition</div>
                    <div style="color: #94A3B8; font-size:0.9rem; margin-top:0.25rem;">Heatmap displaying what proportion of traffic in major stations consists of Short, Medium, or Long distance train runs.</div>
                </div>
                """, unsafe_allow_html=True)
                if os.path.exists("visualizations/station_route_composition.png"):
                    st.image("visualizations/station_route_composition.png", use_container_width=True)
                else:
                    st.warning("Visualizations not found. Please run the Level 5 advanced analysis script first!")
                    
            with col_d:
                st.markdown("""
                <div class="premium-card" style="margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 1.15rem; color:#00F2FE;">High-Traffic Origin-Destination Corridors</div>
                    <div style="color: #94A3B8; font-size:0.9rem; margin-top:0.25rem;">Cross-tabulation thermal heatmap mapping train frequencies between major starting and ending metropolitan hubs.</div>
                </div>
                """, unsafe_allow_html=True)
                if os.path.exists("visualizations/origin_destination_corridors.png"):
                    st.image("visualizations/origin_destination_corridors.png", use_container_width=True)
                else:
                    st.warning("Visualizations not found!")
                    
            st.markdown("---")
            st.markdown("#### Stops Density Distribution")
            col_m, col_n = st.columns([2, 1])
            with col_m:
                if os.path.exists("visualizations/stops_distribution_by_route.png"):
                    st.image("visualizations/stops_distribution_by_route.png", use_container_width=True)
                else:
                    st.warning("Visualization not found!")
            with col_n:
                st.markdown("""
                <div class="premium-card" style="margin-top:1rem;">
                    <div style="font-weight: 700; font-size: 1.15rem; color:#00F2FE;">Stop Densities (Violin Plot)</div>
                    <div style="color: #E2E8F0; font-size:0.9rem; margin-top:0.5rem; line-height:1.6;">
                        This violin plot maps the complete density distribution of stops for each route classification:
                        <br><br>
                        * <b>Short</b>: Very tight distribution concentrated at 1-8 stops.
                        <br><br>
                        * <b>Medium</b>: Wider spread, peaking at 10-20 stops.
                        <br><br>
                        * <b>Long</b>: Extremely wide sub-continental spread, with many long-distance services making over 40-80 stops to provide intermediate rural connectivity.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    # ----------------- TAB 3: STATION TRAFFIC EXPLORER -----------------
    with tab3:
        st.markdown("<h3 style='margin-top:1rem;'>Search & Explore Busiest Station Hub Profiles</h3>", unsafe_allow_html=True)
        
        # Station search box
        station_explorer_list = sorted(
            [f"{row['Station_Name']} ({row['Station_Code']})" for idx, row in df_traffic.iterrows()]
        )
        exp_station_input = st.selectbox("Search Station Hub Profile:", station_explorer_list, index=0)
        exp_station_code = exp_station_input.split("(")[-1].replace(")", "").strip()
        
        # Gather station stats
        station_row = df_traffic[df_traffic["Station_Code"] == exp_station_code]
        if not station_row.empty:
            visit_count = station_row.iloc[0]["Train_Count"]
            rank = df_traffic[df_traffic["Train_Count"] >= visit_count]["Station_Code"].nunique()
            
            st_stops = df_clean[df_clean["Station_Code"] == exp_station_code]
            
            # Starting trains (SN == 1)
            starting_trains = st_stops[st_stops["SN"] == 1]
            
            # Terminating trains (SN == Max_SN)
            trains_max_sn = df_clean.groupby('Train_No')['SN'].max().reset_index().rename(columns={'SN':'Max_SN'})
            st_stops_merged = st_stops.merge(trains_max_sn, on='Train_No')
            terminating_trains = st_stops_merged[st_stops_merged["SN"] == st_stops_merged["Max_SN"]]
            
            # Layout statistics cards
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                st.markdown(f"""
                <div class="premium-card">
                    <div class="metric-label">National Traffic Rank</div>
                    <div class="metric-value">#{rank}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_s2:
                st.markdown(f"""
                <div class="premium-card">
                    <div class="metric-label">Total Visiting Trains</div>
                    <div class="metric-value" style="color:#00F2FE;">{visit_count}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_s3:
                st.markdown(f"""
                <div class="premium-card">
                    <div class="metric-label">Originates Here</div>
                    <div class="metric-value" style="color:#10B981;">{len(starting_trains)}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_s4:
                st.markdown(f"""
                <div class="premium-card">
                    <div class="metric-label">Terminates Here</div>
                    <div class="metric-value" style="color:#EF4444;">{len(terminating_trains)}</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Passing schedule table
            st.markdown(f"#### Complete Schedule Board for {exp_station_input.split(' (')[0]}")
            
            schedule_list = []
            for idx, row in st_stops_merged.iterrows():
                train_det = df_durations[df_durations["Train_No"] == row["Train_No"]]
                route_desc = "Unknown"
                if not train_det.empty:
                    route_desc = f"{train_det.iloc[0]['Start_Station_Name']} ➔ {train_det.iloc[0]['End_Station_Name']}"
                    
                status = "Passing Stop"
                if row["SN"] == 1:
                    status = "Originates Here"
                elif row["SN"] == row["Max_SN"]:
                    status = "Terminates Here"
                    
                schedule_list.append({
                    "Train No": row["Train_No"],
                    "National Route Corridor": route_desc,
                    "Stop No (SN)": row["SN"],
                    "Arrival": row["Arrival_time"] if row["SN"] > 1 else "---",
                    "Departure": row["Departure_Time"] if row["SN"] < row["Max_SN"] else "---",
                    "Cumulative Distance": f"{row['Distance']} km",
                    "Service Status": status
                })
                
            df_board = pd.DataFrame(schedule_list).sort_values("Departure")
            st.dataframe(df_board, use_container_width=True, hide_index=True)
            
else:
    st.info("Please complete data review and processing stages to unlock the Train Enquiry Web App.")
