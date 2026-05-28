import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')  # Headless backend to prevent window rendering issues
import matplotlib.pyplot as plt
import seaborn as sns
import time

def run_level4_analysis():
    print("=" * 60)
    print("   LEVEL 4: BASIC ANALYSIS & VISUALIZATION - TRAIN SCHEDULES   ")
    print("=" * 60)
    
    start_time = time.time()
    
    # Ensure visualizations directory exists
    os.makedirs("visualizations", exist_ok=True)
    
    # Load duration summary and station traffic
    print("\n[Task 4.1] Comparing average journey durations across route types...")
    if not os.path.exists("train_duration_summary.csv"):
        print("Error: train_duration_summary.csv not found! Run Level 2 first.")
        return
        
    df_durations = pd.read_csv("train_duration_summary.csv")
    
    # Group by Route_Type and compute descriptive stats for Duration_Hours
    duration_stats = df_durations.groupby("Route_Type")["Duration_Hours"].agg(
        Count="count",
        Mean="mean",
        Median="median",
        Std_Dev="std",
        Min="min",
        Max="max"
    ).reindex(["Short", "Medium", "Long"])
    
    print("\n--- Descriptive Statistics: Journey Duration (Hours) by Route Type ---")
    print(duration_stats.to_string())
    
    # Task 4.2: Identify high-traffic stations
    print("\n[Task 4.2] Identifying top 20 busiest railway hubs...")
    if not os.path.exists("station_traffic.csv"):
        print("Error: station_traffic.csv not found! Run Level 2 first.")
        return
        
    df_traffic = pd.read_csv("station_traffic.csv")
    top_20_stations = df_traffic.head(20)
    
    print("\n--- Top 20 Busiest Stations by Train Frequency ---")
    print(top_20_stations.to_string(index=False))
    
    # Task 4.3: Create basic visualizations
    print("\n[Task 4.3] Generating and saving high-resolution plots...")
    
    # Set style for professional charts
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'figure.titlesize': 18
    })
    
    # Plot 1: Route Type vs. Average Journey Duration
    plt.figure(figsize=(8, 6))
    ax1 = sns.barplot(
        x="Route_Type", 
        y="Duration_Hours", 
        data=df_durations, 
        order=["Short", "Medium", "Long"],
        palette="viridis",
        errorbar="ci",
        edgecolor="0.2",
        linewidth=1
    )
    plt.title("Average Train Journey Duration by Route Type", pad=15)
    plt.xlabel("Route Classification", labelpad=10)
    plt.ylabel("Average Duration (Hours)", labelpad=10)
    
    # Add values on top of bars
    for p in ax1.patches:
        val = p.get_height()
        if not np.isnan(val):
            ax1.annotate(f"{val:.2f} hrs", 
                         (p.get_x() + p.get_width() / 2., val), 
                         ha='center', va='center', 
                         xytext=(0, 8), 
                         textcoords='offset points',
                         fontweight='bold',
                         fontsize=11)
                         
    plt.tight_layout()
    plot1_path = "visualizations/avg_duration_by_route.png"
    plt.savefig(plot1_path, dpi=300)
    plt.close()
    print(f"-> Saved: '{plot1_path}'")
    
    # Plot 2: Journey Duration Distribution
    plt.figure(figsize=(10, 6))
    # Filter extremely long outliers if any, to keep plot clean
    duration_cap = df_durations["Duration_Hours"].quantile(0.99)
    df_filtered_dur = df_durations[df_durations["Duration_Hours"] <= duration_cap]
    
    sns.histplot(
        df_filtered_dur["Duration_Hours"], 
        kde=True, 
        color="#1E3A8A", 
        bins=40,
        edgecolor="w",
        alpha=0.85
    )
    plt.title("Overall Distribution of Train Journey Durations (99th Percentile Cap)", pad=15)
    plt.xlabel("Journey Duration (Hours)", labelpad=10)
    plt.ylabel("Number of Trains", labelpad=10)
    plt.axvline(df_durations["Duration_Hours"].mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: {df_durations['Duration_Hours'].mean():.2f} hrs")
    plt.axvline(df_durations["Duration_Hours"].median(), color="orange", linestyle=":", linewidth=2, label=f"Median: {df_durations['Duration_Hours'].median():.2f} hrs")
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    plot2_path = "visualizations/duration_distribution.png"
    plt.savefig(plot2_path, dpi=300)
    plt.close()
    print(f"-> Saved: '{plot2_path}'")
    
    # Plot 3: Top 10 High-Traffic Stations
    plt.figure(figsize=(10, 6))
    top_10_stations = df_traffic.head(10)
    sns.barplot(
        x="Train_Count", 
        y="Station_Name", 
        data=top_10_stations, 
        palette="crest_r",
        edgecolor="0.2",
        linewidth=1
    )
    plt.title("Top 10 Busiest Railway Stations (by Train Frequency)", pad=15)
    plt.xlabel("Number of Visiting Trains", labelpad=10)
    plt.ylabel("Station Name", labelpad=10)
    
    # Add counts to bars
    for i, v in enumerate(top_10_stations["Train_Count"]):
        plt.text(v + 10, i, f" {v}", va='center', fontweight='bold', fontsize=11)
        
    plt.tight_layout()
    plot3_path = "visualizations/top_stations_traffic.png"
    plt.savefig(plot3_path, dpi=300)
    plt.close()
    print(f"-> Saved: '{plot3_path}'")
    
    # Task 4.4: Summarize key observations and export report
    print("\n[Task 4.4] Summarizing observations and exporting level4_report.md...")
    
    report_content = f"""# Level 4: Basic Analysis and Visualization Report

This report summarizes the key insights derived from the basic exploratory analysis of train schedule journey durations and station traffic patterns using `Dataset1_Clean.csv`.

---

## 1. Journey Durations by Route Type

Train routes were classified into three categories based on their total travel distance:
* **Short Routes** (<= 100 km)
* **Medium Routes** (101 km to 500 km)
* **Long Routes** (> 500 km)

### Summary Statistics Table

| Route Category | Train Count | Average Duration (Hours) | Median Duration (Hours) | Std Dev (Hours) | Min Duration (Hours) | Max Duration (Hours) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Short** | {duration_stats.loc["Short", "Count"]:,} | {duration_stats.loc["Short", "Mean"]:.2f} | {duration_stats.loc["Short", "Median"]:.2f} | {duration_stats.loc["Short", "Std_Dev"]:.2f} | {duration_stats.loc["Short", "Min"]:.2f} | {duration_stats.loc["Short", "Max"]:.2f} |
| **Medium** | {duration_stats.loc["Medium", "Count"]:,} | {duration_stats.loc["Medium", "Mean"]:.2f} | {duration_stats.loc["Medium", "Median"]:.2f} | {duration_stats.loc["Medium", "Std_Dev"]:.2f} | {duration_stats.loc["Medium", "Min"]:.2f} | {duration_stats.loc["Medium", "Max"]:.2f} |
| **Long** | {duration_stats.loc["Long", "Count"]:,} | {duration_stats.loc["Long", "Mean"]:.2f} | {duration_stats.loc["Long", "Median"]:.2f} | {duration_stats.loc["Long", "Std_Dev"]:.2f} | {duration_stats.loc["Long", "Min"]:.2f} | {duration_stats.loc["Long", "Max"]:.2f} |

### Key Duration Insights
1. **Short-Distance Domination**: Out of {len(df_durations):,} unique trains, **{duration_stats.loc["Short", "Count"]:,} trains ({duration_stats.loc["Short", "Count"]/len(df_durations)*100:.1f}%)** operate on routes under 100 km. These short-haul services represent suburban, local, and passenger networks operating in metropolitan and surrounding zones.
2. **Predictable Scalability**: Average durations scale very logically with distance:
   - Short routes averages **{duration_stats.loc["Short", "Mean"]:.2f} hours** (typically local runs with multiple close stops).
   - Medium routes averages **{duration_stats.loc["Medium", "Mean"]:.2f} hours**.
   - Long routes averages **{duration_stats.loc["Long", "Mean"]:.2f} hours** (with the longest route taking **{duration_stats.loc["Long", "Max"]:.2f} hours**).

---

## 2. Station Traffic Analysis

Traffic is calculated as the frequency of unique train visits to a given station. The analysis reveals a heavily concentrated hub-and-spoke infrastructure.

### Busiest Railway Hubs (Top 10)

| Rank | Station Code | Station Name | Train Frequency (Visits) |
|:---:|:---:|:---|:---:|
| 1 | CSMT | CST-MUMBAI | {top_10_stations.iloc[0]["Train_Count"]} |
| 2 | KYN | KALYAN JN | {top_10_stations.iloc[1]["Train_Count"]} |
| 3 | TNA | THANE | {top_10_stations.iloc[2]["Train_Count"]} |
| 4 | SDAH | SEALDAH | {top_10_stations.iloc[3]["Train_Count"]} |
| 5 | MSB | CHENNAI BEAC | {top_10_stations.iloc[4]["Train_Count"]} |
| 6 | HWH | HOWRAH JN. | {top_10_stations.iloc[5]["Train_Count"]} |
| 7 | DR | DADAR | {top_10_stations.iloc[6]["Train_Count"]} |
| 8 | DDJ | DUM DUM JN. | {top_10_stations.iloc[7]["Train_Count"]} |
| 9 | CLA | KURLA | {top_10_stations.iloc[8]["Train_Count"]} |
| 10 | TBM | TAMBARAM | {top_10_stations.iloc[9]["Train_Count"]} |

### Key Traffic Insights
1. **Mumbai Metropolitan Domination**: Major stations in the Mumbai suburban network represent the absolute busiest locations, led by **Chhatrapati Shivaji Maharaj Terminus (CSMT)** with **{top_10_stations.iloc[0]["Train_Count"]:,} visiting trains**, followed closely by critical suburban junctions **Kalyan (KYN)** and **Thane (TNA)**.
2. **Regional Metro Hubs**: Regional passenger terminals in other major cities, such as **Sealdah (SDAH)** & **Howrah (HWH)** in Kolkata, and **Chennai Beach (MSB)** & **Tambaram (TBM)** in Chennai, are the key pillars of railway operations, handling intense local and express traffic daily.

---

## 3. Visualization Directory

The following professional, high-fidelity visualizations have been generated and saved:
1. **Average Duration Bar Plot**: [avg_duration_by_route.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/avg_duration_by_route.png) - Highlights the comparative mean travel hours between short, medium, and long-distance trains.
2. **Journey Duration Distribution Histogram**: [duration_distribution.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/duration_distribution.png) - Shows a skewed distribution curve with a massive peak at low travel durations, highlighting a network optimized for local transport.
3. **Busiest Stations Horizontal Bar Plot**: [top_stations_traffic.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/top_stations_traffic.png) - Displays a visually clear ranking of train density across the nation's key junctions.
"""
    
    with open("level4_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("-> Level 4 Report saved successfully to 'level4_report.md'")
    
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"   Level 4 Analysis completed successfully in {elapsed_time:.2f} seconds.")
    print("=" * 60)

if __name__ == "__main__":
    run_level4_analysis()
