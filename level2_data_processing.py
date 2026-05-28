import pandas as pd
import numpy as np
import time

def run_level2_processing():
    print("=" * 60)
    print("   LEVEL 2: SIMPLE DATA PROCESSING - TRAIN SCHEDULE ANALYSIS   ")
    print("=" * 60)
    
    start_time = time.time()
    
    # Load dataset
    print("\n[Task 2.1] Loading and standardizing schedule fields...")
    df = pd.read_csv("Dataset1.csv", keep_default_na=False)
    
    # Ensure times are clean, stripping any whitespace
    df["Arrival_time"] = df["Arrival_time"].astype(str).str.strip()
    df["Departure_Time"] = df["Departure_Time"].astype(str).str.strip()
    
    # Sort data by Train_No and SN to ensure correct sequence progression
    df_sorted = df.sort_values(by=["Train_No", "SN"])
    
    # Convert HH:MM:SS to seconds from midnight for vectorized datetime operations
    def time_to_seconds_vectorized(series):
        # Split HH:MM:SS and convert to total seconds
        parts = series.str.split(":")
        return parts.str[0].astype(int) * 3600 + parts.str[1].astype(int) * 60 + parts.str[2].astype(int)
    
    print("-> Standardizing Arrival and Departure times...")
    arrival_secs = time_to_seconds_vectorized(df_sorted["Arrival_time"])
    departure_secs = time_to_seconds_vectorized(df_sorted["Departure_Time"])
    
    # Task 2.2: Compute total journey duration for each train using cumulative rollover logic
    print("\n[Task 2.2] Computing total journey durations with rollover handling...")
    
    # 1. Travel Legs: Shift departure seconds within the same train to get prev_dep_secs
    df_sorted["prev_dep_secs"] = df_sorted.groupby("Train_No")["Departure_Time"].shift(1)
    # Convert prev_dep_secs to seconds (handle NaN for starting stops)
    has_prev = df_sorted["prev_dep_secs"].notna()
    prev_dep_secs = np.zeros(len(df_sorted))
    prev_dep_secs[has_prev] = time_to_seconds_vectorized(df_sorted["prev_dep_secs"][has_prev])
    
    # Travel duration = Arrival_time - prev_dep_secs
    travel_diff = np.zeros(len(df_sorted))
    travel_diff[has_prev] = arrival_secs[has_prev] - prev_dep_secs[has_prev]
    # If travel_diff < 0, a midnight rollover occurred during the leg
    travel_diff[has_prev & (travel_diff < 0)] += 86400
    
    # 2. Halt Legs: Halt duration = Departure_Time - Arrival_time
    # Find the maximum SN for each train to identify terminal stations
    df_sorted["Max_SN"] = df_sorted.groupby("Train_No")["SN"].transform("max")
    
    # Halt is only valid for intermediate stops (1 < SN < Max_SN)
    is_intermediate = (df_sorted["SN"] > 1) & (df_sorted["SN"] < df_sorted["Max_SN"])
    halt_diff = np.zeros(len(df_sorted))
    halt_diff[is_intermediate] = departure_secs[is_intermediate] - arrival_secs[is_intermediate]
    # If halt_diff < 0, a midnight rollover occurred during the station halt
    halt_diff[is_intermediate & (halt_diff < 0)] += 86400
    
    # Total seconds elapsed at/before this stop
    df_sorted["leg_duration_secs"] = travel_diff + halt_diff
    
    # Aggregate total journey duration per train in minutes
    journey_mins = df_sorted.groupby("Train_No")["leg_duration_secs"].sum() / 60.0
    journey_mins = journey_mins.reset_index(name="Duration_Minutes")
    journey_mins["Duration_Hours"] = journey_mins["Duration_Minutes"] / 60.0
    
    # Task 2.3: Classify routes as short, medium, or long
    print("\n[Task 2.3] Classifying routes based on total distance...")
    
    # Find total distance and stations at min and max SN
    grouped = df_sorted.groupby("Train_No")
    start_stops = grouped.first().reset_index()
    end_stops = grouped.last().reset_index()
    
    # Combine train route details
    train_routes = pd.merge(
        start_stops[["Train_No", "Station_Code", "Station_Name"]].rename(
            columns={"Station_Code": "Start_Station_Code", "Station_Name": "Start_Station_Name"}
        ),
        end_stops[["Train_No", "Station_Code", "Station_Name", "Distance"]].rename(
            columns={"Station_Code": "End_Station_Code", "Station_Name": "End_Station_Name", "Distance": "Total_Distance"}
        ),
        on="Train_No"
    )
    
    # Merge computed duration information
    train_summary = pd.merge(train_routes, journey_mins, on="Train_No")
    
    # Classification rules:
    # Short: <= 100 km
    # Medium: 101 - 500 km
    # Long: > 500 km
    def classify_distance(dist):
        if dist <= 100:
            return "Short"
        elif dist <= 500:
            return "Medium"
        else:
            return "Long"
            
    train_summary["Route_Type"] = train_summary["Total_Distance"].apply(classify_distance)
    
    # Save the train duration and classification metadata to CSV
    duration_csv_path = "train_duration_summary.csv"
    train_summary.to_csv(duration_csv_path, index=False)
    print(f"-> Train duration and classification saved to '{duration_csv_path}'")
    
    # Preview route types distribution
    print("\n--- Route Types Distribution ---")
    print(train_summary["Route_Type"].value_counts())
    
    # Task 2.4: Generate station-wise train frequency counts
    print("\n[Task 2.4] Generating station-wise train frequency counts...")
    
    # Count visits of trains at each station
    station_counts = df_sorted.groupby(["Station_Code", "Station_Name"]).size().reset_index(name="Train_Count")
    # Sort by frequency descending
    station_counts = station_counts.sort_values(by="Train_Count", ascending=False)
    
    # Save to CSV
    station_traffic_path = "station_traffic.csv"
    station_counts.to_csv(station_traffic_path, index=False)
    print(f"-> Station traffic counts saved to '{station_traffic_path}'")
    
    print("\n--- Top 10 Busiest Stations (by Train Frequency) ---")
    print(station_counts.head(10).to_string(index=False))
    
    # Double check some well-known trains
    print("\n--- Validation Check on Known Trains ---")
    t107 = train_summary[train_summary["Train_No"] == 107]
    if not t107.empty:
        print(f"Train 107: Distance = {t107.iloc[0]['Total_Distance']} km | Duration = {t107.iloc[0]['Duration_Minutes']:.1f} mins ({t107.iloc[0]['Duration_Hours']:.2f} hrs) | Class = {t107.iloc[0]['Route_Type']}")
        
    t53041 = train_summary[train_summary["Train_No"] == 53041]
    if not t53041.empty:
        print(f"Train 53041: Distance = {t53041.iloc[0]['Total_Distance']} km | Duration = {t53041.iloc[0]['Duration_Minutes']:.1f} mins ({t53041.iloc[0]['Duration_Hours']:.2f} hrs) | Class = {t53041.iloc[0]['Route_Type']}")
        
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"   Level 2 Processing completed successfully in {elapsed_time:.2f} seconds.")
    print("=" * 60)

if __name__ == "__main__":
    run_level2_processing()
