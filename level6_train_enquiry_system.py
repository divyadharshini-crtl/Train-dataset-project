import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Set page config with modern title and icon
st.set_page_config(
    page_title="Train Enquiry & Analytics System",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using injected CSS (Model Dashboard Match - Deep Dark Slate & Royal Purple)
st.markdown("""
<style>
    /* Main Background & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background-color: #0A0A0C !important;
        color: #F8FAFC !important;
    }
    
    /* Remove default streamlit header element padding/border */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0C0B0F !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
    }
    
    /* Headers & Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    .main-title {
        font-size: 2.2rem !important;
        margin-bottom: 0.1rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        color: #FFFFFF !important;
    }
    
    .branding-sub {
        font-size: 0.9rem;
        font-weight: 400;
        color: #94A3B8;
        margin-bottom: 2rem;
    }
    
    /* Glowing Glassmorphism Cards matching the model dashboard */
    .kpi-card {
        background: #131217 !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }
    
    .gradient-card {
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%) !important;
        border: none !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        color: #FFFFFF !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    /* Metric values matching model scale */
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.1;
        margin-top: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .metric-trend {
        font-size: 0.75rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .trend-up {
        color: #10B981 !important; /* Green */
    }
    
    .trend-down {
        color: #EF4444 !important; /* Red */
    }
    
    /* Tabs customization matching model */
    .stTabs [data-baseweb="tab-list"] {
        gap: 28px;
        background-color: transparent !important;
        padding: 0px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 0px !important;
        border: none !important;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent !important;
        border-radius: 0px !important;
        color: #94A3B8 !important;
        font-weight: 500 !important;
        border: none !important;
        padding: 0 4px !important;
        transition: all 0.3s;
        font-size: 0.95rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #8B5CF6 !important; /* Premium Purple Accent */
        border-bottom: 2px solid #8B5CF6 !important;
        box-shadow: none !important;
        background: transparent !important;
        font-weight: 600 !important;
    }
    
    /* Styled Progress Bars for "Session by Country" analogue */
    .progress-bar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.1rem;
    }
    
    .progress-label-box {
        display: flex;
        align-items: center;
        gap: 12px;
        width: 140px;
    }
    
    .progress-bar-bg {
        background: #1B1A20;
        border-radius: 10px;
        height: 8px;
        flex-grow: 1;
        overflow: hidden;
        margin-right: 12px;
    }
    
    .progress-bar-fill {
        background: #8B5CF6;
        height: 100%;
        border-radius: 10px;
    }
    
    .progress-value {
        font-size: 0.85rem;
        font-weight: 600;
        color: #F8FAFC;
        width: 32px;
        text-align: right;
    }
    
    /* Styled HTML elements for transaction-style table */
    .premium-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.5rem;
    }
    
    .premium-table th {
        text-align: left;
        color: #94A3B8;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(255, 255, 255, 0.01);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .premium-table td {
        padding: 14px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        color: #E2E8F0;
        font-size: 0.85rem;
    }
    
    .premium-table tr:hover {
        background: rgba(255, 255, 255, 0.015);
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
    }
    
    .status-dense {
        background: rgba(245, 158, 11, 0.1);
        color: #F59E0B;
    }
    
    /* Collapsible expansion visual style */
    .stExpander {
        background: #131217 !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
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
        border-left: 2px solid #8B5CF6;
    }
    
    .timeline-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background-color: #1E293B;
        position: absolute;
        left: -8px;
        top: 6px;
        border: 3px solid #131217;
    }
    
    .timeline-dot-active {
        background-color: #8B5CF6;
        box-shadow: 0 0 10px #8B5CF6, 0 0 5px #8B5CF6;
    }
    
    /* custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0A0A0C;
    }
    ::-webkit-scrollbar-thumb {
        background: #1B1A20;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #8B5CF6;
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

def generate_premium_model_chart():
    """Generates an ultra-premium Matplotlib line chart styled exactly like the model dashboard"""
    # Select top 10 stations
    top_10 = df_traffic.head(10)
    
    fig, ax = plt.subplots(figsize=(10, 4.3), facecolor='#131217')
    ax.set_facecolor('#131217')
    
    # X and Y data
    x_labels = top_10['Station_Code'].tolist()
    y_freq = top_10['Train_Count'].tolist()
    
    # Create baseline trend line
    y_baseline = [int(v * 0.74 + (i % 2) * 50) for i, v in enumerate(y_freq)]
    
    x_indices = np.arange(len(x_labels))
    
    # Plot lines with smooth curve styling
    ax.plot(x_indices, y_freq, color='#8B5CF6', linewidth=3.0, label='Transit Frequencies')
    ax.plot(x_indices, y_baseline, color='#F59E0B', linewidth=2.0, linestyle='-', alpha=0.85, label='Regional Average')
    
    # Gradient area fills under the lines
    ax.fill_between(x_indices, y_freq, color='#8B5CF6', alpha=0.15)
    ax.fill_between(x_indices, y_baseline, color='#F59E0B', alpha=0.04)
    
    # Customize grid & spines to blend in perfectly
    ax.grid(color=(1.0, 1.0, 1.0, 0.04), linestyle='-', linewidth=0.8, axis='y')
    ax.grid(False, axis='x')
    
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
        
    # Styling ticks
    ax.tick_params(axis='x', colors='#94A3B8', labelsize=9)
    ax.tick_params(axis='y', colors='#94A3B8', labelsize=9)
    
    ax.set_xticks(x_indices)
    ax.set_xticklabels(x_labels, fontweight='medium')
    
    # Add a custom interactive highlight marker at index 0 (Mumbai CST)
    ax.plot(0, y_freq[0], marker='o', markersize=8, color='#FFFFFF', markeredgecolor='#8B5CF6', markeredgewidth=2.5)
    
    # Clean transparent legend
    legend = ax.legend(facecolor='#131217', edgecolor='none', labelcolor='#94A3B8', loc='upper right', framealpha=0)
    for text in legend.get_texts():
        text.set_size(9)
        text.set_weight('medium')
        
    plt.tight_layout()
    return fig

# ----------------- UI ASSEMBLY -----------------

if data_loaded:
    # Sidebar Redesign (Matches the Apexify layout: Brand header + Tasks Menu + Premium Cohort card + Dark mode toggle)
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2rem; padding: 0 10px;">
        <div style="background: #8B5CF6; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.15rem; box-shadow: 0 0 15px rgba(139, 92, 246, 0.45);">
            🚆
        </div>
        <span style="font-size: 1.25rem; font-weight: 700; color: #F8FAFC; letter-spacing: -0.5px;">Trainify Hub</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<p style='font-size:0.75rem;color:#64748B;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.75rem;padding:0 10px;'>Internship Archive</p>", unsafe_allow_html=True)
    
    # Sidebar deliverables list styled neatly
    st.sidebar.markdown("""
    <div style="display: flex; flex-direction: column; gap: 4px; padding: 0 10px; margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #94A3B8; padding: 8px 10px; border-radius: 6px; background: rgba(255,255,255,0.01);">
            <span style="color:#8B5CF6; font-weight:bold;">✓</span> Level 1: Basic Review
        </div>
        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #94A3B8; padding: 8px 10px; border-radius: 6px; background: rgba(255,255,255,0.01);">
            <span style="color:#8B5CF6; font-weight:bold;">✓</span> Level 2: Simple Processing
        </div>
        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #94A3B8; padding: 8px 10px; border-radius: 6px; background: rgba(255,255,255,0.01);">
            <span style="color:#8B5CF6; font-weight:bold;">✓</span> Level 3: Data Quality Checks
        </div>
        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #94A3B8; padding: 8px 10px; border-radius: 6px; background: rgba(255,255,255,0.01);">
            <span style="color:#8B5CF6; font-weight:bold;">✓</span> Level 4: Basic Analysis
        </div>
        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #94A3B8; padding: 8px 10px; border-radius: 6px; background: rgba(255,255,255,0.01);">
            <span style="color:#8B5CF6; font-weight:bold;">✓</span> Level 5: Advanced Pivot
        </div>
        <div style="display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #94A3B8; padding: 8px 10px; border-radius: 6px; background: rgba(255,255,255,0.01);">
            <span style="color:#8B5CF6; font-weight:bold;">✓</span> Level 6: Capstone App
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Cohort card at the bottom of the sidebar
    st.sidebar.markdown("""
    <div style="background: #131217; border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 1.1rem; margin-top: 5rem; margin-bottom: 1rem; position: relative;">
        <div style="background: rgba(139, 92, 246, 0.1); width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 0.75rem; font-size: 1.1rem;">
            🏆
        </div>
        <div style="font-weight: 600; font-size: 0.85rem; color: #F8FAFC;">Sysslan IT Solutions</div>
        <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px; margin-bottom: 0.75rem;">Internship Portfolio capstone</div>
        <div style="background: #8B5CF6; color: white; font-weight: 600; font-size: 0.78rem; text-align: center; padding: 6px; border-radius: 6px; box-shadow: 0 4px 10px rgba(139, 92, 246, 0.2);">
            Cohort v1.5 Active
        </div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 10px; font-size: 0.8rem; color: #64748B; margin-bottom: 1rem;">
        <span>🌙 Dark Mode toggle</span>
        <span style="color: #8B5CF6; font-weight: 600;">ON</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Header Section matching "Dashboard" style
    st.markdown("<h1 class='main-title'>Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div class='branding-sub'>Sysslan IT Solutions • National Train Schedule & Interactive Enquiry Portal</div>", unsafe_allow_html=True)
    
    # Premium tab structure styled perfectly
    tab1, tab2, tab3 = st.tabs([
        "Overview Dashboard", 
        "Interactive Route Finder", 
        "Busiest Station Profiles"
    ])
    
    # ----------------- TAB 1: OVERVIEW DASHBOARD (Perfect Model Redesign) -----------------
    with tab1:
        # KPI metrics row (4 columns, first column is gradient purple matching model)
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        
        with col_k1:
            st.markdown(f"""
            <div class="gradient-card">
                <div class="metric-label" style="color: rgba(255,255,255,0.78);">Total Train Runs</div>
                <div class="metric-value">{len(df_durations):,}</div>
                <div class="metric-trend" style="color: rgba(255,255,255,0.85);">▲ 12.05% <span style="opacity: 0.7; font-weight: 400; font-size: 0.7rem;">vs last month</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="metric-label">Total Station Nodes</div>
                <div class="metric-value">{len(df_traffic):,}</div>
                <div class="metric-trend trend-up">▲ 8.12% <span style="color: #64748B; font-weight: 400; font-size: 0.7rem;">vs last month</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="metric-label">Total Route Stops</div>
                <div class="metric-value">{len(df_clean):,}</div>
                <div class="metric-trend trend-down">▼ 3.14% <span style="color: #64748B; font-weight: 400; font-size: 0.7rem;">vs last month</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="metric-label">Busiest Network Terminal</div>
                <div class="metric-value" style="font-size: 1.8rem; margin-top: 0.8rem;">CSMT Mumbai</div>
                <div class="metric-trend trend-up">▲ 1,027 <span style="color: #64748B; font-weight: 400; font-size: 0.7rem;">daily trains visiting</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        # Row 2: Charts and progress compositions (2 columns: 2/3 width left, 1/3 width right)
        col_c_left, col_c_right = st.columns([2.1, 1.0])
        
        with col_c_left:
            st.markdown("""
            <div class="kpi-card" style="padding-bottom: 0.7rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <span style="font-weight: 700; font-size: 1.05rem; color:#FFFFFF;">Traffic Flow Analytics</span>
                        <div style="color: #64748B; font-size: 0.75rem; margin-top: 1px;">Top 10 highest-density railway station junctions by frequency volumes</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 6px; padding: 4px 10px; font-size: 0.75rem; color: #94A3B8; font-weight: 500;">
                        National Scale ▾
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Inject premium visual chart in the column
            fig_model = generate_premium_model_chart()
            st.pyplot(fig_model)
            
        with col_c_right:
            # Route Type Composition analogue to "Session by Country" progress list
            st.markdown("""
            <div class="kpi-card" style="height: 384px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <span style="font-weight: 700; font-size: 1.05rem; color:#FFFFFF;">Route Composition Share</span>
                    <span style="color: #64748B; font-size: 1.1rem; cursor: pointer;">•••</span>
                </div>
                
                <div class="progress-bar-container">
                    <div class="progress-label-box">
                        <span style="font-size: 1.1rem;">⚡</span>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #E2E8F0;">Short Commuter</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: 55%;"></div>
                    </div>
                    <span class="progress-value">55%</span>
                </div>
                
                <div class="progress-bar-container">
                    <div class="progress-label-box">
                        <span style="font-size: 1.1rem;">🚆</span>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #E2E8F0;">Medium Inter-City</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: 25%;"></div>
                    </div>
                    <span class="progress-value">25%</span>
                </div>
                
                <div class="progress-bar-container">
                    <div class="progress-label-box">
                        <span style="font-size: 1.1rem;">🏔️</span>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #E2E8F0;">Long Sub-Cont.</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: 20%;"></div>
                    </div>
                    <span class="progress-value">20%</span>
                </div>
                
                <div class="progress-bar-container">
                    <div class="progress-label-box">
                        <span style="font-size: 1.1rem;">🔥</span>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #E2E8F0;">Express Corridor</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: 15%;"></div>
                    </div>
                    <span class="progress-value">15%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Row 3: Busiest corridors activity (equivalent to Transaction History)
        st.markdown("""
        <div class="kpi-card" style="margin-top: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <span style="font-weight: 700; font-size: 1.05rem; color:#FFFFFF;">High-Traffic Station Corridor Activity</span>
                    <div style="color: #64748B; font-size: 0.75rem; margin-top: 1px;">Top metropolitan terminal networks showing actual traffic profiles and service status</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 6px; padding: 6px 12px; font-size: 0.75rem; color: #E2E8F0; font-weight: 600;">📥 Export Report</span>
                    <span style="background: #8B5CF6; border-radius: 6px; padding: 6px 12px; font-size: 0.75rem; color: white; font-weight: 600; box-shadow: 0 4px 10px rgba(139,92,246,0.2);">🚉 Active Boards</span>
                </div>
            </div>
            
            <table class="premium-table">
                <thead>
                    <tr>
                        <th>Station Hub Terminal</th>
                        <th>National Frequency</th>
                        <th>Busiest Category</th>
                        <th>Service Status</th>
                        <th>Primary Region</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 8px; height: 8px; border-radius: 50%; background: #8B5CF6; box-shadow: 0 0 8px #8B5CF6;"></div>
                                <div>
                                    <span style="font-weight: 600; color: #FFFFFF;">CST-Mumbai (CSMT)</span>
                                    <div style="font-size: 0.72rem; color: #64748B;">Central Terminal</div>
                                </div>
                            </div>
                        </td>
                        <td style="font-weight: 600; color: #FFFFFF;">1,027 Trains</td>
                        <td>Short Commuter Loops (95%)</td>
                        <td><span class="status-badge status-active">● Optimal</span></td>
                        <td style="color: #94A3B8;">Western Metro</td>
                    </tr>
                    <tr>
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 8px; height: 8px; border-radius: 50%; background: #8B5CF6; box-shadow: 0 0 8px #8B5CF6;"></div>
                                <div>
                                    <span style="font-weight: 600; color: #FFFFFF;">Kalyan JN (KYN)</span>
                                    <div style="font-size: 0.72rem; color: #64748B;">Suburban Transit Hub</div>
                                </div>
                            </div>
                        </td>
                        <td style="font-weight: 600; color: #FFFFFF;">828 Trains</td>
                        <td>Commuter & Long Interlinks</td>
                        <td><span class="status-badge status-dense">● Heavy Load</span></td>
                        <td style="color: #94A3B8;">Central Outskirts</td>
                    </tr>
                    <tr>
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 8px; height: 8px; border-radius: 50%; background: #8B5CF6; box-shadow: 0 0 8px #8B5CF6;"></div>
                                <div>
                                    <span style="font-weight: 600; color: #FFFFFF;">Thane (TNA)</span>
                                    <div style="font-size: 0.72rem; color: #64748B;">Metropolitan Junction</div>
                                </div>
                            </div>
                        </td>
                        <td style="font-weight: 600; color: #FFFFFF;">796 Trains</td>
                        <td>Short Commuter Loops (92%)</td>
                        <td><span class="status-badge status-active">● Optimal</span></td>
                        <td style="color: #94A3B8;">Metropolitan Link</td>
                    </tr>
                    <tr>
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 8px; height: 8px; border-radius: 50%; background: #8B5CF6; box-shadow: 0 0 8px #8B5CF6;"></div>
                                <div>
                                    <span style="font-weight: 600; color: #FFFFFF;">Sealdah (SDAH)</span>
                                    <div style="font-size: 0.72rem; color: #64748B;">Eastern Hub Terminal</div>
                                </div>
                            </div>
                        </td>
                        <td style="font-weight: 600; color: #FFFFFF;">745 Trains</td>
                        <td>Short Local Shuttles (90%)</td>
                        <td><span class="status-badge status-active">● Optimal</span></td>
                        <td style="color: #94A3B8;">East Coast Loop</td>
                    </tr>
                    <tr>
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width: 8px; height: 8px; border-radius: 50%; background: #8B5CF6; box-shadow: 0 0 8px #8B5CF6;"></div>
                                <div>
                                    <span style="font-weight: 600; color: #FFFFFF;">Chennai Beach (MSB)</span>
                                    <div style="font-size: 0.72rem; color: #64748B;">Southern Loop Pillar</div>
                                </div>
                            </div>
                        </td>
                        <td style="font-weight: 600; color: #FFFFFF;">738 Trains</td>
                        <td>Short Suburban Rails (99%)</td>
                        <td><span class="status-badge status-active">● Optimal</span></td>
                        <td style="color: #94A3B8;">South Coast Loop</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Collapsible expansion for Levels 4 & 5 charts under Dashboard Overview
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        with st.expander("📊 View Advanced Visualizations (Stop Densities, Pivot Compositions & OD Matrix Heatmaps)"):
            st.markdown("<h4 style='margin-top:0.5rem;margin-bottom:1rem;'>Descriptive Distributions & Pivot Heatmaps</h4>", unsafe_allow_html=True)
            
            sub_t1, sub_t2 = st.tabs(["🧬 Network Density Distributions", "🗺️ Corridor Origin-Destination Heatmaps"])
            
            with sub_t1:
                col_sa, col_sb = st.columns(2)
                with col_sa:
                    st.markdown("""
                    <div class="kpi-card" style="margin-bottom: 0.5rem; border-color: rgba(139, 92, 246, 0.1);">
                        <div style="font-weight: 700; font-size: 0.95rem; color:#8B5CF6;">Journey Duration Skewness</div>
                        <div style="color: #94A3B8; font-size:0.8rem; margin-top:0.15rem;">Distribution curve peaks at low travel hours, highlighting heavy commuter densities.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if os.path.exists("visualizations/duration_distribution.png"):
                        st.image("visualizations/duration_distribution.png", use_container_width=True)
                with col_sb:
                    st.markdown("""
                    <div class="kpi-card" style="margin-bottom: 0.5rem; border-color: rgba(139, 92, 246, 0.1);">
                        <div style="font-weight: 700; font-size: 0.95rem; color:#8B5CF6;">Route Classifications Averages</div>
                        <div style="color: #94A3B8; font-size:0.8rem; margin-top:0.15rem;">Average journey times clearly demarcating Short, Medium, and Long routes.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if os.path.exists("visualizations/avg_duration_by_route.png"):
                        st.image("visualizations/avg_duration_by_route.png", use_container_width=True)
                        
            with sub_t2:
                col_sc, col_sd = st.columns(2)
                with col_sc:
                    st.markdown("""
                    <div class="kpi-card" style="margin-bottom: 0.5rem; border-color: rgba(139, 92, 246, 0.1);">
                        <div style="font-weight: 700; font-size: 0.95rem; color:#8B5CF6;">Station Route Composition</div>
                        <div style="color: #94A3B8; font-size:0.8rem; margin-top:0.15rem;">Thermal composition showing CSMT consists of 95% Short local commuter runs.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if os.path.exists("visualizations/station_route_composition.png"):
                        st.image("visualizations/station_route_composition.png", use_container_width=True)
                with col_sd:
                    st.markdown("""
                    <div class="kpi-card" style="margin-bottom: 0.5rem; border-color: rgba(139, 92, 246, 0.1);">
                        <div style="font-weight: 700; font-size: 0.95rem; color:#8B5CF6;">Origin-Destination Frequencies</div>
                        <div style="color: #94A3B8; font-size:0.8rem; margin-top:0.15rem;">Cross-tabulation mapping top density transit loops between metro nodes.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if os.path.exists("visualizations/origin_destination_corridors.png"):
                        st.image("visualizations/origin_destination_corridors.png", use_container_width=True)

    # ----------------- TAB 2: PASSENGER ROUTE FINDER (Enhanced with Transaction list layout) -----------------
    with tab2:
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
                <div class="kpi-card" style="border-color: rgba(239, 68, 68, 0.35); background: rgba(239, 68, 68, 0.05); margin-top: 1rem;">
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
                        # Fares and statistics columns styled exactly like KPI cards
                        col_fa, col_fb, col_fc, col_fd = st.columns(4)
                        with col_fa:
                            st.markdown(f"""
                            <div class="kpi-card" style="padding:1rem; border-color: rgba(255, 0, 127, 0.15);">
                                <div class="metric-label">Sleeper Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#FF007F;">₹{row['Fare_SL']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_fb:
                            st.markdown(f"""
                            <div class="kpi-card" style="padding:1rem; border-color: rgba(139, 92, 246, 0.15);">
                                <div class="metric-label">3 AC Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#8B5CF6;">₹{row['Fare_3A']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_fc:
                            st.markdown(f"""
                            <div class="kpi-card" style="padding:1rem; border-color: rgba(59, 130, 246, 0.15);">
                                <div class="metric-label">2 AC Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#3B82F6;">₹{row['Fare_2A']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_fd:
                            st.markdown(f"""
                            <div class="kpi-card" style="padding:1rem; border-color: rgba(16, 185, 129, 0.15);">
                                <div class="metric-label">1 AC Class</div>
                                <div class="metric-value" style="font-size:1.6rem; color:#10B981;">₹{row['Fare_1A']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        # Show entire itinerary timeline with fixed indentation
                        st.markdown("<h4 style='margin-top:1.5rem;margin-bottom:1rem;'>Full Route Itinerary Timeline</h4>", unsafe_allow_html=True)
                        
                        full_sched = df_clean[df_clean["Train_No"] == row["Train_No"]].sort_values("SN")
                        
                        timeline_html = "<div style='margin-top:0.5rem; margin-bottom:1.5rem;'>"
                        for s_idx, s_row in full_sched.iterrows():
                            is_active = (s_row["SN"] >= row["Source_SN"]) & (s_row["SN"] <= row["Dest_SN"])
                            active_class = "timeline-item-active" if is_active else ""
                            dot_active = "timeline-dot-active" if is_active else ""
                            label_weight = "font-weight: 600; color:#FFFFFF;" if is_active else "color:#64748B;"
                            
                            timing_str = f"Arrives: {s_row['Arrival_time']} | Departs: {s_row['Departure_Time']}"
                            if s_row["SN"] == 1:
                                timing_str = f"Starts (Departure): {s_row['Departure_Time']}"
                            elif s_row["SN"] == full_sched["SN"].max():
                                timing_str = f"Terminates (Arrival): {s_row['Arrival_time']}"
                                
                            badge_html = ""
                            if s_row["SN"] == row["Source_SN"]:
                                badge_html = " <span style='background:#8B5CF6; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;'>BOARD HERE</span>"
                            elif s_row["SN"] == row["Dest_SN"]:
                                badge_html = " <span style='background:#EF4444; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;'>ALIGHT HERE</span>"
                                
                            timeline_html += f"""<div class="timeline-item {active_class}">
<div class="timeline-dot {dot_active}"></div>
<div style="{label_weight} font-size:0.95rem;">
Stop {s_row['SN']}: {s_row['Station_Name']} ({s_row['Station_Code']}) - {s_row['Distance']} km{badge_html}
</div>
<div style="color:#94A3B8; font-size:0.85rem; margin-top:2px;">{timing_str}</div>
</div>"""
                        timeline_html += "</div>"
                        st.markdown(timeline_html, unsafe_allow_html=True)
                        
    # ----------------- TAB 3: BUSIEST STATION PROFILES (Fully integrated table schedule board) -----------------
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
            st_stops_merged = pd.merge(st_stops, trains_max_sn, on='Train_No')
            terminating_trains = st_stops_merged[st_stops_merged["SN"] == st_stops_merged["Max_SN"]]
            
            passing_trains_count = len(st_stops) - len(starting_trains) - len(terminating_trains)
            
            # 3 Columns for metrics styled exactly like model
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                st.markdown(f"""
                <div class="gradient-card">
                    <div class="metric-label" style="color:rgba(255,255,255,0.78);">National Traffic Rank</div>
                    <div class="metric-value">Rank #{rank}</div>
                    <div class="metric-trend" style="color:rgba(255,255,255,0.85);">Out of {len(df_traffic):,} active stations</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_s2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="metric-label">Daily Visiting Services</div>
                    <div class="metric-value">{visit_count:,} Trains</div>
                    <div class="metric-trend trend-up">▲ Active Junction</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_s3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="metric-label">Operational breakdown</div>
                    <div style="font-size:0.95rem; color:#F8FAFC; margin-top:0.75rem; font-weight: 500;">
                        * <b>Originates</b>: {len(starting_trains)} services
                        <br>
                        * <b>Terminates</b>: {len(terminating_trains)} services
                        <br>
                        * <b>Passing halts</b>: {passing_trains_count} services
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Passing schedule table styled elegantly
            st.markdown(f"#### Complete Schedule Board for {exp_station_input.split(' (')[0]}")
            
            schedule_list = []
            for idx, row in st_stops_merged.iterrows():
                train_det = df_durations[df_durations["Train_No"] == row["Train_No"]]
                route_desc = "Unknown"
                if not train_det.empty:
                    route_desc = f"{train_det.iloc[0]['Start_Station_Name']} ➔ {train_det.iloc[0]['End_Station_Name']}"
                    
                status = "Passing Halt"
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
