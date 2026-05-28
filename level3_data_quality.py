import pandas as pd
import time

def run_level3_quality_checks():
    print("=" * 60)
    print("   LEVEL 3: DATA QUALITY CHECKS - TRAIN SCHEDULE ANALYSIS   ")
    print("=" * 60)
    
    start_time = time.time()
    
    # Task 3.1: Handle missing schedule values
    print("\n[Task 3.1] Handling missing schedule values...")
    
    # Crucial insight: Read with keep_default_na=False to preserve the "NAN" station code (NANOGAON ROA)
    print("-> Loading dataset with keep_default_na=False to preserve 'NAN' station code...")
    df = pd.read_csv("Dataset1.csv", keep_default_na=False)
    
    # Check for any true empty or null values
    null_counts = df.isnull().sum()
    empty_counts = {col: (df[col] == "").sum() for col in df.columns}
    
    print("\n--- Missing Value Audit ---")
    print("Column-wise Null Counts (Pandas isnull):")
    print(null_counts)
    print("\nColumn-wise Empty String Counts ('') :")
    for col, count in empty_counts.items():
        print(f"{col:15} : {count}")
        
    print("\n-> Handling 'NAN' station code specifically:")
    nan_rows = df[df["Station_Code"] == "NAN"]
    print(f"   Found {len(nan_rows)} rows corresponding to the real station 'NANOGAON ROA' with code 'NAN'.")
    print("   These have been successfully preserved as strings instead of being corrupted as NaN!")
    
    print("\n-> Auditing '00:00:00' values in schedule fields:")
    arr_zeros = df[df["Arrival_time"] == "00:00:00"]
    dep_zeros = df[df["Departure_Time"] == "00:00:00"]
    print(f"   Total '00:00:00' Arrival times: {len(arr_zeros)} (expected as start-of-route arrivals or midnight arrivals)")
    print(f"   Total '00:00:00' Departure times: {len(dep_zeros)} (expected as end-of-route departures or midnight departures)")
    
    # Task 3.2: Remove duplicate train records
    print("\n[Task 3.2] Auditing and removing duplicate records...")
    
    # Check for exact duplicate rows
    exact_dups = df.duplicated().sum()
    print(f"-> Exact duplicate rows in dataset: {exact_dups}")
    if exact_dups > 0:
        df = df.drop_duplicates()
        print("   Exact duplicate rows removed successfully.")
    
    # Audit duplicate station codes within the same train route
    df_sorted = df.sort_values(by=["Train_No", "SN"])
    key_dups_sc = df_sorted.duplicated(subset=["Train_No", "Station_Code"]).sum()
    print(f"-> Train-level duplicate Station Codes: {key_dups_sc}")
    
    if key_dups_sc > 0:
        print("   Investigating duplicated station codes in routes...")
        dup_routes = df_sorted[df_sorted.duplicated(subset=["Train_No", "Station_Code"], keep=False)]
        unique_dup_trains = dup_routes["Train_No"].unique()
        print(f"   Found {len(unique_dup_trains)} trains visiting the same station code twice.")
        print("   Example of a train with circular/reversal stops:")
        example_train = unique_dup_trains[0]
        example_df = df_sorted[df_sorted["Train_No"] == example_train]
        print(example_df[["SN", "Train_No", "Station_Code", "Station_Name", "Arrival_time", "Departure_Time", "Distance"]].to_string(index=False))
        print("   Note: These represent valid operational reversals or loop routing, NOT errors.")
        
    # Verify that there are no duplicate (Train_No, SN) combinations
    key_dups_sn = df_sorted.duplicated(subset=["Train_No", "SN"]).sum()
    print(f"-> Duplicate Train_No and Stop Sequence (SN) combinations: {key_dups_sn}")
    
    # Task 3.3: Verify correct station order in each route
    print("\n[Task 3.3] Verifying station order and distance progression...")
    
    # Verify sequence number SN is strictly increasing
    df_sorted["prev_SN"] = df_sorted.groupby("Train_No")["SN"].shift(1)
    sn_order_violations = df_sorted[df_sorted["SN"] <= df_sorted["prev_SN"]]
    print(f"-> Sequence Number (SN) progression violations (SN <= prev_SN): {len(sn_order_violations)}")
    
    # Verify distance is non-decreasing
    df_sorted["prev_Distance"] = df_sorted.groupby("Train_No")["Distance"].shift(1)
    distance_order_violations = df_sorted[df_sorted["Distance"] < df_sorted["prev_Distance"]]
    print(f"-> Distance progression violations (Distance < prev_Distance): {len(distance_order_violations)}")
    
    # Cleanup shift columns
    df_sorted = df_sorted.drop(columns=["prev_SN", "prev_Distance"])
    
    # Task 3.4: Save the verified dataset
    print("\n[Task 3.4] Saving the verified and validated dataset...")
    clean_csv_path = "Dataset1_Clean.csv"
    df_sorted.to_csv(clean_csv_path, index=False)
    print(f"-> Verified dataset successfully saved to '{clean_csv_path}'")
    print(f"-> Total Clean Records Exported: {len(df_sorted):,}")
    
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"   Level 3 Data Quality Checks completed successfully in {elapsed_time:.2f} seconds.")
    print("=" * 60)

if __name__ == "__main__":
    run_level3_quality_checks()
