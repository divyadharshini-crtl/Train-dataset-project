# Level 5: Advanced Analysis and Visualization Report

This report presents advanced insights derived from multi-dimensional analyses (pivot tables, cross-tabulations, and thermal density heatmaps) of the train schedule dataset.

---

## 1. Hub Traffic Composition Profiles

Our pivot analysis of the top 15 busiest railway stations reveals two distinct operational profiles across India's rail network:

1. **Suburban-Heavy Commuter Hubs**:
   - Stations such as **CST-Mumbai (CSMT)**, **Kalyan Jn (KYN)**, **Thane (TNA)**, **Chennai Beach (MSB)**, and **Tambaram (TBM)** exhibit traffic consisting of **over 95% Short-distance routes**. 
   - For example, CSMT CST-Mumbai has a traffic profile dominated by short suburban shuttle loops, displaying the intense daily reliance on commuter local rail.
   
2. **Integrated Multi-Modal Transit Hubs**:
   - Major cross-country junctions like **Howrah Jn (HWH)** and **Vijayawada Jn (BZA)** exhibit highly diversified profiles.
   - For example, **Howrah Jn** handles a healthy mix of Short commuter services, Medium inter-city express lines, and Long-distance sub-continental expresses.

---

## 2. Corridor and Stopping Characteristics

### Route Type vs. Stop Count Cross-Tabulation

| Route Type | 1-5 Stops (Commuter) | 6-15 Stops (Express/Local) | 16-30 Stops (Long Express) | 31+ Stops (Sub-continental) |
|:---|:---:|:---:|:---:|:---:|
| **Short** | 2,014 | 2,339 | 1,720 | 9 |
| **Medium** | 90 | 808 | 1,372 | 557 |
| **Long** | 49 | 507 | 988 | 660 |

### Key Structural Insights
1. **Commuter Run Efficiency**: **33.1%** of all Short-distance routes have 5 stops or fewer. These are highly streamlined commuter lines running point-to-point in urban clusters.
2. **Sub-continental Stop Densities**: Among Long-distance routes (> 500 km), **29.9%** of the trains make **over 31 stops** along their journey. This illustrates the dual purpose of long-distance trains: serving as national transport corridors while providing critical local connectivity to intermediate towns and rural stations.
3. **High-Density City Pairs**: The origin-destination heatmap highlights dense corridors such as commuter runs between CST-Mumbai (CSMT) and Kalyan/Thane, which represents the dense flow of commuter transit.

---

## 3. Advanced Visualization Directory

The following advanced, publication-quality visualizations have been generated and saved:
1. **Station Route Composition Heatmap**: [station_route_composition.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/station_route_composition.png) - Illustrates the percent traffic composition for the 15 busiest hubs.
2. **Origin-Destination City Corridor Heatmap**: [origin_destination_corridors.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/origin_destination_corridors.png) - Highlights the density of direct train runs between top national cities.
3. **Stops Distribution Violin Plot**: [stops_distribution_by_route.png](file:///c:/Users/divya/OneDrive/Desktop/ssylan%20internship/visualizations/stops_distribution_by_route.png) - Demonstrates the distribution of stop frequencies across route classes, revealing clear quartiles and density modes.
