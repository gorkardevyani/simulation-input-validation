import streamlit as st
import pandas as pd
import json

st.title("Order-RA-Map Consistency Checker")

st.write("""
Upload:
- **ra_input.xlsx** (customer-to-marker mapping)
- **order_data.xlsx** (order data with storage spaces)
- **map .smap/.json file** (warehouse layout map)
""")

ra_file = st.file_uploader("Upload ra_input.xlsx", type=["xlsx"])
order_file = st.file_uploader("Upload order_data.xlsx", type=["xlsx"])
map_file = st.file_uploader("Upload map .smap/.json file", type=["smap", "json"])

if ra_file and order_file and map_file:
    # Load data
    ra_df = pd.read_excel(ra_file)
    order_df = pd.read_excel(order_file)
    map_json = json.load(map_file)

    order_locations = set(order_df['Storage Space'].dropna().str.strip().unique())
    ra_locations = set(ra_df['Location'].dropna().str.strip().unique())
    ra_markers = set(ra_df['Marker Code'].dropna().str.strip().unique())

    # Extract marker names from advancedPointList
    marker_names = set()
    for marker in map_json.get('advancedPointList', []):
        instance_name = marker.get('instance-name')
        instance_name2 = marker.get('instanceName')
        if instance_name:
            marker_names.add(instance_name.strip())
        if instance_name2:
            marker_names.add(instance_name2.strip())

    # Check 1: Storage Locations vs RA mapping
    cleaned_order_locations = {loc[:-2] for loc in order_locations}
    missing_locations = cleaned_order_locations - ra_locations

    # Check 2: Marker Codes vs Map instances
    missing_markers = ra_markers - marker_names

    st.header("📌 Results Summary")
    st.subheader(f"❗ Missing Storage Locations in ra_input: {len(missing_locations)}")
    st.write(sorted(missing_locations))

    st.subheader(f"❗ Missing Marker Codes in map file: {len(missing_markers)}")
    st.write(sorted(missing_markers))

    # Downloadable reports
    if missing_locations or missing_markers:
        result_df = pd.DataFrame({
            "Missing Storage Locations": list(missing_locations) + [""] * (max(len(missing_markers), len(missing_locations)) - len(missing_locations)),
            "Missing Marker Codes": list(missing_markers) + [""] * (max(len(missing_markers), len(missing_locations)) - len(missing_markers)),
        })
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Report CSV", csv, "missing_report.csv", "text/csv")

else:
    st.info("Please upload all three files to get the consistency report.")
