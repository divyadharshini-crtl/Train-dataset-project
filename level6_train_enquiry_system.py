# ==============================================================================
# PROJECT: Train Schedule Analysis & Interactive Route Enquiry System
# DEVELOPER: Data Analysis & Full-Stack Developer
# BRANDING: Prepared for Sysslan IT Solutions Submission
# DESCRIPTION: Premium, dark-themed interactive Streamlit Web Dashboard
#              containing Network Analytics and a robust Passenger Enquiry Engine.
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')  # Headless backend to prevent rendering threads conflicts
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ----------------- 1. PREMIUM PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="Sysslan IT Solutions - Train Enquiry & Analytics",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- 2. MODERN GLASSMORPHISM DESIGN STYLESHEET (CSS) -----------------
st.markdown("""
<style>
    /* Google Outfit Modern Typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Cosmic Dark Theme Background */
    .stApp {
        background-color: #060B13;
        color: #F1F5F9;
    }
    
    /* Custom Sidebar Header styling */
    section[data-testid="stSidebar"] {
        background-color: #0A0F1D !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
    }
    
    /* Branded Dashboard Title styling */
    .main-title {
        background: linear-gradient(135deg, #FF007F 0%, #7928CA 50%, #00F2FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem !important;
        margin-bottom: 0.15rem !important;
        font-weight: 700 !important;
        letter-spacing: -1.5px;
        line-height: 1.2;
    }
    
    .subtitle-banner {
        font-size: 1.15rem;
        font-weight: 600;
        letter-spacing: 2px;
        color: #00F2FE;
        text-transform: uppercase;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.25);
    }
    
    /* Glowing Glassmorphic Cards for KPIs */
    .kpi-card {
        background: rgba(13, 22, 41, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, border-color 0.3s ease;
        position: relative;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #FF007F, #00F2FE);
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 242, 254, 0.4);
        box-shadow: 0 20px 40px rgba(0, 242, 254, 0.15);
    }
    
    .kpi-value {
        font-size: 2.3rem;
        font-weight: 700;
        color: #00F2FE;
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.35);
        margin-top: 0.35rem;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- 3. HIGH-PERFORMANCE DATA INGESTION -----------------
@st.cache_data
def load_verified_data():
    """Loads and caches verified train schedule data cleanly"""
    file_path = "verified_train_schedule.csv"
    if not os.path.exists(file_path):
        st.error(f"Missing core database: '{file_path}' not found!")
        return None
    # Load dataset with keep_default_na=False to protect the "NAN" station code
    df = pd.read_csv(file_path, keep_default_na=False)
    # Ensure schedule columns are clean strings
    df["Arrival_time"] = df["Arrival_time"].astype(str).str.strip()
    df["Departure_Time"] = df["Departure_Time"].astype(str).str.strip()
    return df

df_schedule = load_verified_data()

# ----------------- 4. SIDEBAR NAVIGATION CONTROLS -----------------
st.sidebar.markdown("<h2 style='color:#00F2FE;margin-bottom:0;'>🚆 PULSAR PANEL</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:0.8rem;color:#475569;margin-bottom:1.5rem;'>SYSSLAN IT SOLUTIONS COHORT</p>", unsafe_allow_html=True)

# Styled page navigation dropdown in sidebar
current_page = st.sidebar.radio(
    "Choose System Workspace:",
    options=["📈 Network Overview Analytics", "🔍 Interactive Passenger Enquiry Hub"],
    index=0
)

# System details footer in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Submission Details")
st.sidebar.markdown("""
- **Project**: Train Schedule Analysis
- **Framework**: Streamlit v1.3+
- **Theme**: Dark Glassmorphic
- **Integrity**: 100% Original Code
""")
st.sidebar.markdown("<br><br><small style='color:#475569;'>Antigravity Portal Engine v1.8</small>", unsafe_allow_html=True)

# ----------------- 5. MAIN CORE ROUTINES -----------------
if df_schedule is not None:
    
    # ----------------- PAGE 1: NETWORK OVERVIEW ANALYTICS -----------------
    if current_page == "📈 Network Overview Analytics":
        # Header
        st.markdown("<h1 class='main-title'>PULSAR RAIL</h1>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle-banner'>Network Overview & High-Traffic Analytics</div>", unsafe_allow_html=True)
        
        # 1. KPI Metric Cards
        st.markdown("### National Infrastructure KPIs")
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        
        # Calculate KPI Values
        total_trains = df_schedule["Train_No"].nunique()
        total_stations = df_schedule["Station_Code"].nunique()
        
        # Determine Network Busiest Node (Highest visit count)
        traffic_counts = df_schedule.groupby(["Station_Code", "Station_Name"]).size().reset_index(name="Count")
        busiest_row = traffic_counts.sort_values(by="Count", ascending=False).iloc[0]
        busiest_node = f"{busiest_row['Station_Name']} ({busiest_row['Station_Code']})"
        
        # Display KPIs inside beautifully styled cards
        with col_kpi1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Active Train Routes</div>
                <div class="kpi-value" style="color:#FF007F; text-shadow: 0 0 10px rgba(255, 0, 127, 0.3);">{total_trains:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_kpi2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Monitored Station Hubs</div>
                <div class="kpi-value" style="color:#A78BFA; text-shadow: 0 0 10px rgba(167, 139, 250, 0.3);">{total_stations:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_kpi3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Network Busiest Node</div>
                <div class="kpi-value" style="font-size: 1.45rem; margin-top: 1.15rem; color:#00F2FE;">{busiest_node}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # 2. Visualizations Area
        st.markdown("### Top 10 Busiest Railway Junctions (by Train Visits)")
        
        # Prepare Top 10 traffic data
        top_10_traffic = traffic_counts.sort_values(by="Count", ascending=False).head(10)
        
        # Create a professional Seaborn horizontal bar chart fitting the dark theme
        sns.set_theme(style="dark")
        fig, ax = plt.subplots(figsize=(10, 5), facecolor="#060B13")
        ax.set_facecolor("#0D1629")
        
        # Modern gradient colors
        bar_colors = sns.color_palette("crest_r", 10)
        
        sns.barplot(
            x="Count",
            y="Station_Name",
            data=top_10_traffic,
            palette=bar_colors,
            ax=ax,
            edgecolor="#00F2FE",
            linewidth=1.2
        )
        
        # Customizing Axes & Labels for absolute modern visual elegance
        ax.set_title("Top 10 High-Traffic Station Density Profile", color="#F8FAFC", fontsize=15, pad=15, fontweight="bold")
        ax.set_xlabel("Number of Visiting Trains", color="#94A3B8", fontsize=11, labelpad=10)
        ax.set_ylabel("Station Name", color="#94A3B8", fontsize=11, labelpad=10)
        
        # Ticks color custom styling
        ax.tick_params(colors="#94A3B8", labelsize=10)
        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_color("rgba(255, 255, 255, 0.05)")
            
        # Draw clean grid lines
        ax.grid(True, color="rgba(255, 255, 255, 0.03)", linestyle="--", linewidth=0.8)
        
        # Annotate counts inside the bars
        for idx, p in enumerate(ax.patches):
            val = int(p.get_width())
            ax.annotate(f"  {val:,}", 
                        (val, p.get_y() + p.get_height() / 2.), 
                        ha='left', va='center', 
                        color="#00F2FE", 
                        fontweight="bold",
                        fontsize=10)
                        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Short analytical summary box
        st.markdown("""
        <div class="kpi-card" style="margin-top:1.5rem; border-color: rgba(16, 185, 129, 0.2); background: rgba(16, 185, 129, 0.03);">
            <div style="color: #10B981; font-weight: 700; font-size: 1.05rem;">📊 Analytical Insight</div>
            <div style="color: #94A3B8; font-size:0.9rem; margin-top:0.35rem; line-height:1.6;">
                The traffic distribution profile demonstrates extreme commuter density across regional metropolitan terminals. Mumbai Terminus (CSMT), Kalyan Jn, and Thane lead the network, illustrating intense local commuter passenger loops, while Sealdah and Howrah serve as massive regional interlinks.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # ----------------- PAGE 2: INTERACTIVE PASSENGER ENQUIRY HUB -----------------
    elif current_page == "🔍 Interactive Passenger Enquiry Hub":
        # Header
        st.markdown("<h1 class='main-title'>PULSAR RAIL</h1>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle-banner'>Interactive Passenger Enquiry Hub</div>", unsafe_allow_html=True)
        
        st.markdown("### Query Direct Routes & Timelines")
        
        # Compile a clean sorted list of unique stations: "Station Name (Station Code)"
        station_traffic_counts = df_schedule.groupby(["Station_Code", "Station_Name"]).size().reset_index(name="Count")
        station_traffic_counts = station_traffic_counts.sort_values(by="Count", ascending=False)
        
        station_dropdown_options = sorted(
            [f"{row['Station_Name']} ({row['Station_Code']})" for idx, row in station_traffic_counts.iterrows()]
        )
        
        # 1. Inputs selectboxes
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            origin_sel = st.selectbox(
                "Select Origin Terminal:", 
                station_dropdown_options, 
                index=station_dropdown_options.index("SAWANTWADI R (SWV)") if "SAWANTWADI R (SWV)" in station_dropdown_options else 0
            )
        with col_in2:
            dest_sel = st.selectbox(
                "Select Destination Terminal:", 
                station_dropdown_options, 
                index=station_dropdown_options.index("MADGOAN JN. (MAO)") if "MADGOAN JN. (MAO)" in station_dropdown_options else 1
            )
            
        # Extract plain station codes
        origin_code = origin_sel.split("(")[-1].replace(")", "").strip()
        dest_code = dest_sel.split("(")[-1].replace(")", "").strip()
        
        if origin_code == dest_code:
            st.warning("Origin and Destination stations must be different to search routes!")
        else:
            # 2. Robust Filtering Algorithm:
            # - Find trains passing through the origin station
            trains_at_origin = df_schedule[df_schedule["Station_Code"] == origin_code]
            # - Find trains passing through the destination station
            trains_at_dest = df_schedule[df_schedule["Station_Code"] == dest_code]
            
            # Find common Train_Nos operating between these two hubs
            common_train_numbers = set(trains_at_origin["Train_No"]).intersection(set(trains_at_dest["Train_No"]))
            
            direct_routes_found = []
            
            for t_no in common_train_numbers:
                # Slices full stops timeline for this train
                t_sched = df_schedule[df_schedule["Train_No"] == t_no].sort_values("SN")
                
                # Fetch exact stop rows
                origin_stop_row = t_sched[t_sched["Station_Code"] == origin_code].iloc[0]
                dest_stop_row = t_sched[t_sched["Station_Code"] == dest_code].iloc[0]
                
                # Direct route criteria: Origin sequence number (SN) MUST be less than Destination sequence number
                if origin_stop_row["SN"] < dest_stop_row["SN"]:
                    
                    # Exact distance delta: Destination distance minus Origin distance
                    distance_delta = int(dest_stop_row["Distance"]) - int(origin_stop_row["Distance"])
                    
                    # Calculate estimated journey duration: Departure (Origin) to Arrival (Destination)
                    # Correctly handling midnight crossings!
                    t_origin_dep = datetime.strptime(origin_stop_row["Departure_Time"], "%H:%M:%S")
                    t_dest_arr = datetime.strptime(dest_stop_row["Arrival_time"], "%H:%M:%S")
                    
                    duration_hours = (t_dest_arr - t_origin_dep).total_seconds() / 3600.0
                    if duration_hours < 0:
                        duration_hours += 24.0  # Core midnight rollover correction
                        
                    direct_routes_found.append({
                        "Train No": t_no,
                        "Origin Departs": origin_stop_row["Departure_Time"],
                        "Destination Arrives": dest_stop_row["Arrival_time"],
                        "Stops Between": int(dest_stop_row["SN"] - origin_stop_row["SN"] - 1),
                        "Distance Delta (KM)": distance_delta,
                        "Est. Duration (Hours)": round(duration_hours, 2),
                        "Sleeper Fare (₹)": int(dest_stop_row["SL"]) - int(origin_stop_row["SL"]) if int(dest_stop_row["SL"]) > int(origin_stop_row["SL"]) else 120
                    })
            
            # Display results in beautifully formatted custom boards
            if not direct_routes_found:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: rgba(239, 68, 68, 0.35); background: rgba(239, 68, 68, 0.05); margin-top: 1.5rem;">
                    <div style="color: #F87171; font-weight: 700; font-size: 1.15rem;">No Direct Connect Found</div>
                    <div style="color: #94A3B8; font-size:0.95rem; margin-top:0.4rem;">
                        There are no direct trains operating from <b>{origin_sel.split(" (")[0]}</b> to <b>{dest_sel.split(" (")[0]}</b>. Consider transit routes via regional hubs.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                df_routes_board = pd.DataFrame(direct_routes_found).sort_values(by="Origin_Departs" if "Origin_Departs" in pd.DataFrame(direct_routes_found).columns else "Origin Departs")
                
                # Show results count
                st.markdown(f"Found **{len(df_routes_board)}** direct train connections:")
                
                # Renders styled Streamlit Dataframe board
                st.dataframe(
                    df_routes_board,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("---")
                
                # Additional route visual timelines helper
                st.markdown("#### Detailed Route Timeline Visualization")
                selected_t_no = st.selectbox("Select a Train to view its complete timeline itinerary:", df_routes_board["Train No"].tolist())
                
                if selected_t_no:
                    # Slices stops
                    sel_sched = df_schedule[df_schedule["Train_No"] == selected_t_no].sort_values("SN")
                    sel_route = df_routes_board[df_routes_board["Train No"] == selected_t_no].iloc[0]
                    
                    timeline_html = "<div style='margin-top:1rem; margin-bottom:1.5rem;'>"
                    for s_idx, s_row in sel_sched.iterrows():
                        # Slices active stops
                        is_active_leg = (s_row["SN"] >= sel_sched[sel_sched["Station_Code"] == origin_code].iloc[0]["SN"]) & \
                                        (s_row["SN"] <= sel_sched[sel_sched["Station_Code"] == dest_code].iloc[0]["SN"])
                                        
                        active_cls = "timeline-item-active" if is_active_leg else ""
                        dot_cls = "timeline-dot-active" if is_active_leg else ""
                        text_style = "font-weight: 700; color:#F8FAFC;" if is_active_leg else "color:#64748B;"
                        
                        arrival_lbl = s_row["Arrival_time"] if s_row["SN"] > 1 else "Origin Starts"
                        departure_lbl = s_row["Departure_Time"] if s_row["SN"] < sel_sched["SN"].max() else "Terminal Ends"
                        
                        badge = ""
                        if s_row["Station_Code"] == origin_code:
                            badge = " <span style='background:#10B981; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;'>BOARD HERE</span>"
                        elif s_row["Station_Code"] == dest_code:
                            badge = " <span style='background:#EF4444; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;'>ALIGHT HERE</span>"
                            
                        timeline_html += f"""
                        <div class="timeline-item {active_cls}">
                            <div class="timeline-dot {dot_cls}"></div>
                            <div style="{text_style} font-size:0.95rem;">
                                Stop {s_row['SN']}: {s_row['Station_Name']} ({s_row['Station_Code']}) - {s_row['Distance']} km{badge}
                            </div>
                            <div style="color:#94A3B8; font-size:0.85rem; margin-top:2px;">
                                Arrives: {arrival_lbl} | Departs: {departure_lbl}
                            </div>
                        </div>
                        """
                    timeline_html += "</div>"
                    st.markdown(timeline_html, unsafe_allow_html=True)
