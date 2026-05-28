import pandas as pd
import time

def run_level1_analysis():
    print("=" * 60)
    print("   LEVEL 1: BASIC DATA REVIEW - TRAIN SCHEDULE ANALYSIS   ")
    print("=" * 60)
    
    start_time = time.time()
    
    # Task 1.1: Overview of dataset - total records & attributes
    # We use keep_default_na=False to prevent "NAN" station code from being parsed as NaN/null
    print("\n[Task 1.1] Loading dataset and performing initial overview...")
    df = pd.read_csv("Dataset1.csv", keep_default_na=False)
    
    total_records = len(df)
    total_columns = len(df.columns)
    columns_list = df.columns.tolist()
    
    print(f"-> Total Records (Rows): {total_records:,}")
    print(f"-> Total Attributes (Columns): {total_columns}")
    print(f"-> Attributes: {columns_list}")
    
    print("\n--- Attribute Details & Data Types ---")
    print(df.info())
    
    # Task 1.2: List all trains with their starting and ending stations
    # Task 1.3: Calculate the number of stops per train
    print("\n[Task 1.2 & 1.3] Computing train routes and stop counts...")
    
    # Ensure dataframe is sorted by Train_No and SN (Sequence Number) to find starting/ending stops accurately
    df_sorted = df.sort_values(by=["Train_No", "SN"])
    
    # Group by Train_No
    grouped = df_sorted.groupby("Train_No")
    
    # Start stop is the first stop (minimum SN)
    start_stops = grouped.first().reset_index()
    # End stop is the last stop (maximum SN)
    end_stops = grouped.last().reset_index()
    # Total stops per train is the count of stops
    stop_counts = grouped.size().reset_index(name="Total_Stops")
    
    # Merge starting, ending, and stop count information
    train_summary = pd.merge(
        start_stops[["Train_No", "Station_Code", "Station_Name"]].rename(
            columns={"Station_Code": "Start_Station_Code", "Station_Name": "Start_Station_Name"}
        ),
        end_stops[["Train_No", "Station_Code", "Station_Name"]].rename(
            columns={"Station_Code": "End_Station_Code", "Station_Name": "End_Station_Name"}
        ),
        on="Train_No"
    )
    train_summary = pd.merge(train_summary, stop_counts, on="Train_No")
    
    # Save the train routes summary to CSV
    summary_csv_path = "train_routes_summary.csv"
    train_summary.to_csv(summary_csv_path, index=False)
    print(f"-> Train routes summary saved successfully to '{summary_csv_path}'")
    print(f"-> Total Unique Trains Analyzed: {len(train_summary):,}")
    
    # Show a preview of the train summary
    print("\n--- Preview of Train Routes Summary (First 5 trains) ---")
    print(train_summary.head(5).to_string(index=False))
    
    # Task 1.4: Identify trains with maximum and minimum stops
    print("\n[Task 1.4] Identifying trains with extreme stop counts...")
    
    max_stops = train_summary["Total_Stops"].max()
    min_stops = train_summary["Total_Stops"].min()
    
    trains_max_stops = train_summary[train_summary["Total_Stops"] == max_stops]
    trains_min_stops = train_summary[train_summary["Total_Stops"] == min_stops]
    
    print(f"\n-> MAXIMUM STOPS PER TRAIN: {max_stops}")
    print(f"   Found {len(trains_max_stops)} train(s) with {max_stops} stops:")
    for idx, row in trains_max_stops.iterrows():
        print(f"   * Train No: {row['Train_No']} | Route: {row['Start_Station_Name']} ({row['Start_Station_Code']}) to {row['End_Station_Name']} ({row['End_Station_Code']})")
        
    print(f"\n-> MINIMUM STOPS PER TRAIN: {min_stops}")
    print(f"   Found {len(trains_min_stops)} train(s) with {min_stops} stops:")
    # We will print the first 5 trains if there are many, to keep console output readable
    print_limit = 5
    for i, (idx, row) in enumerate(trains_min_stops.iterrows()):
        if i >= print_limit:
            print(f"   * ... and {len(trains_min_stops) - print_limit} more trains.")
            break
        print(f"   * Train No: {row['Train_No']} | Route: {row['Start_Station_Name']} ({row['Start_Station_Code']}) to {row['End_Station_Name']} ({row['End_Station_Code']})")
    
    # Summary of Stops Statistics
    print("\n--- Summary Stop Statistics across all Trains ---")
    print(train_summary["Total_Stops"].describe())
    
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"   Level 1 Analysis completed successfully in {elapsed_time:.2f} seconds.")
    print("=" * 60)

if __name__ == "__main__":
    run_level1_analysis()
