# Level 4: Basic Analysis and Visualization Report

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
| **Short** | 6,082 | 1.29 | 1.17 | 0.74 | 0.08 | 7.17 |
| **Medium** | 2,827 | 5.56 | 4.92 | 2.77 | 1.67 | 18.37 |
| **Long** | 2,204 | 25.78 | 23.33 | 13.07 | 6.08 | 152.00 |

### Key Duration Insights
1. **Short-Distance Domination**: Out of 11,113 unique trains, **6,082 trains (54.7%)** operate on routes under 100 km. These short-haul services represent suburban, local, and passenger networks operating in metropolitan and surrounding zones.
2. **Predictable Scalability**: Average durations scale very logically with distance:
   - Short routes averages **1.29 hours** (typically local runs with multiple close stops).
   - Medium routes averages **5.56 hours**.
   - Long routes averages **25.78 hours** (with the longest route taking **152.00 hours**).

---

## 2. Station Traffic Analysis

Traffic is calculated as the frequency of unique train visits to a given station. The analysis reveals a heavily concentrated hub-and-spoke infrastructure.

### Busiest Railway Hubs (Top 10)

| Rank | Station Code | Station Name | Train Frequency (Visits) |
|:---:|:---:|:---|:---:|
| 1 | CSMT | CST-MUMBAI | 1027 |
| 2 | KYN | KALYAN JN | 828 |
| 3 | TNA | THANE | 796 |
| 4 | SDAH | SEALDAH | 745 |
| 5 | MSB | CHENNAI BEAC | 738 |
| 6 | HWH | HOWRAH JN. | 699 |
| 7 | DR | DADAR | 567 |
| 8 | DDJ | DUM DUM JN. | 463 |
| 9 | CLA | KURLA | 462 |
| 10 | TBM | TAMBARAM | 434 |

### Key Traffic Insights
1. **Mumbai Metropolitan Domination**: Major stations in the Mumbai suburban network represent the absolute busiest locations, led by **Chhatrapati Shivaji Maharaj Terminus (CSMT)** with **1,027 visiting trains**, followed closely by critical suburban junctions **Kalyan (KYN)** and **Thane (TNA)**.
2. **Regional Metro Hubs**: Regional passenger terminals in other major cities, such as **Sealdah (SDAH)** & **Howrah (HWH)** in Kolkata, and **Chennai Beach (MSB)** & **Tambaram (TBM)** in Chennai, are the key pillars of railway operations, handling intense local and express traffic daily.

---

## 3. Visualization Directory

The following professional, high-fidelity visualizations have been generated and saved:
1. **Average Duration Bar Plot**: [avg_duration_by_route.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/avg_duration_by_route.png) - Highlights the comparative mean travel hours between short, medium, and long-distance trains.
2. **Journey Duration Distribution Histogram**: [duration_distribution.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/duration_distribution.png) - Shows a skewed distribution curve with a massive peak at low travel durations, highlighting a network optimized for local transport.
3. **Busiest Stations Horizontal Bar Plot**: [top_stations_traffic.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/top_stations_traffic.png) - Displays a visually clear ranking of train density across the nation's key junctions.
