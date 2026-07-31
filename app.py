import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime

# ==========================================
# PAGE SETUP & STYLING
# ==========================================
st.set_page_config(
    page_title="Cryptid GIS Field Platform",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌲 Cryptid GIS Field Platform")
st.caption("All-Sighting Mapping, Objective Analysis & Field Logging Engine")

# Initialize session state for field logs
if "community_notes" not in st.session_state:
    st.session_state.community_notes = []

# Helper function for text filtering
def parse_witness_report(raw_text):
    if not raw_text.strip(): return None, None
    lines = raw_text.split('\n')
    concrete, conjecture = [], []
    keywords = ["felt", "thought", "believed", "seemed", "appeared", "telepathic", "mindspeak", "intent", "afraid", "scared"]
    for line in lines:
        if not line.strip(): continue
        if any(w in line.lower() for w in keywords):
            conjecture.append(line.strip())
        else:
            concrete.append(line.strip())
    return concrete, conjecture

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.header("📍 Target Coordinates")
lat_input = st.sidebar.number_input("Latitude", value=35.944444, format="%.6f")
lon_input = st.sidebar.number_input("Longitude", value=-82.772333, format="%.6f")

st.sidebar.markdown("---")
st.sidebar.header("🗂️ Active Map Layers")
show_bfro = st.sidebar.checkbox("BFRO Reports (Biological)", value=True)
show_bfm = st.sidebar.checkbox("Bigfoot Mapping Project", value=True)
show_meta = st.sidebar.checkbox("Metaphysical / High-Strangeness", value=True)
show_toponyms = st.sidebar.checkbox("USGS Ominous / Wildman Names", value=True)

st.sidebar.markdown("---")
st.sidebar.header("📂 Data Import")
uploaded_csv = st.sidebar.file_uploader("Upload Sighting CSV Data", type=["csv"])

# ==========================================
# MAIN APP TABS
# ==========================================
tab_map, tab_tribal, tab_media, tab_toponyms, tab_field_entry, tab_parser, tab_export = st.tabs([
    "🗺️ All-Sighting GIS Map",
    "🪶 Tribal Territory & Lore",
    "📰 Historic Media Archives",
    "🏷️ USGS Ominous & Legend Scanner", 
    "📌 Submit Field Report & Media",
    "📄 Witness Report Filter", 
    "📱 onX / GPX Exporter"
])

# ------------------------------------------
# TAB 1: ALL-SIGHTING GIS MAP
# ------------------------------------------
with tab_map:
    st.caption("All known sightings rendered. Pinch to zoom, drag to pan across the map.")
    
    # Initialize Leaflet Map
    m = folium.Map(
        location=[lat_input, lon_input], 
        zoom_start=9,
        tiles="OpenStreetMap",
        control_scale=True,
        touch_zoom=True,
        dragging=True
    )
    
    # Target Location Pin
    folium.Marker(
        [lat_input, lon_input],
        popup=f"Target: {lat_input:.4f}, {lon_input:.4f}",
        icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")
    ).add_to(m)

    # All-Sighting Data Pins (Always Visible)
    if show_bfro:
        folium.Marker(
            [35.9844, -82.8023],
            popup="<b>BFRO Class A</b><br>Wood knocks & rock throwing along creek.",
            icon=folium.Icon(color="blue", icon="tree", prefix="fa")
        ).add_to(m)

    if show_bfm:
        folium.Marker(
            [35.9244, -82.7223],
            popup="<b>BFM Node</b><br>Visual encounter near ridge trail.",
            icon=folium.Icon(color="green", icon="eye", prefix="fa")
        ).add_to(m)

    if show_meta:
        folium.Marker(
            [35.8944, -82.8523],
            popup="<b>Metaphysical Report</b><br>Orb activity & sudden feeling of dread.",
            icon=folium.Icon(color="purple", icon="star", prefix="fa")
        ).add_to(m)

    # Render User Field Notes
    for note in st.session_state.community_notes:
        if note["privacy"] == "Public":
            folium.Marker(
                [note["lat"], note["lon"]],
                popup=f"<b>{note['title']}</b><br>{note['notes']}",
                icon=folium.Icon(color="orange", icon="flag", prefix="fa")
            ).add_to(m)

    # Custom CSV Data
    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv)
            for idx, row in df.iterrows():
                if "latitude" in row and "longitude" in row:
                    folium.Marker(
                        [row["latitude"], row["longitude"]],
                        popup=row.get("title", "Sighting"),
                        icon=folium.Icon(color="darkblue", icon="info-sign")
                    ).add_to(m)
        except:
            pass

    st_folium(m, width=1100, height=600)

# ------------------------------------------
# TAB 2: TRIBAL TERRITORY & LORE
# ------------------------------------------
with tab_tribal:
    st.subheader("🪶 Indigenous Ethno-Historical Context & Tribal Oral Lore")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏛️ Tribal Jurisdiction")
        st.info("**Primary Tribal Nation:** Cherokee Nation / EBCI")
        st.markdown("* **Nearest Cultural Center:** Museum of the Cherokee People\n* **Research Contact:** EBCI Tribal Historic Preservation Office (THPO)")
    with col2:
        st.markdown("### 📜 Indexed Oral Entities")
        st.markdown("* **Tsul 'Kalu (Judaculla):** Mountain giant controlling wild game.\n* **Nunne'hi:** Invisible mountain/cavern spirit race.")

# ------------------------------------------
# TAB 3: HISTORIC MEDIA ARCHIVES
# ------------------------------------------
with tab_media:
    st.subheader("📰 Local Media Coverage & Historical News Archives")
    st.markdown("**Search Keywords:** `wild man`, `wildman`, `hairy giant`, `ape man`, `mountain devil`")
    news_records = [
        {"Date": "1888-04-12", "Publication": "WNC Democrat", "Headline": "'Hairy Giant' Terrorizes Local Ridge Farmers", "Keyword": "hairy giant"},
        {"Date": "1923-11-14", "Publication": "Asheville Citizen-Times", "Headline": "'Wild Man' Reported in Unaka Mountains", "Keyword": "wild man"},
    ]
    st.dataframe(pd.DataFrame(news_records), use_container_width=True)

# ------------------------------------------
# TAB 4: USGS TOPONYM SCANNER
# ------------------------------------------
with tab_toponyms:
    st.subheader("🏷️ USGS GNIS Ominous, Legend & Feature Scanner")
    gnis_data = [
        {"Feature Name": "Giant Knob", "Type": "Summit", "Match": "Giant"},
        {"Feature Name": "Devil's Fork", "Type": "Stream", "Match": "Devil"},
        {"Feature Name": "Wildman Branch", "Type": "Stream", "Match": "Wildman"},
    ]
    st.table(gnis_data)

# ------------------------------------------
# TAB 5: FIELD REPORT SUBMISSION
# ------------------------------------------
with tab_field_entry:
    st.subheader("📌 Submit In-Field Observation & Attach Media")
    col1, col2 = st.columns(2)
    with col1:
        e_title = st.text_input("Title", "Field Log")
        e_lat = st.number_input("Lat", value=lat_input, format="%.6f")
        e_lon = st.number_input("Lon", value=lon_input, format="%.6f")
        e_cat = st.selectbox("Type", ["Biological", "Metaphysical", "Environmental"])
        e_priv = st.radio("Privacy", ["Public", "Private"])
    with col2:
        e_notes = st.text_area("Notes", height=100)
        st.file_uploader("Photo", type=["jpg", "png"])
        st.file_uploader("Audio", type=["mp3", "wav"])
        st.file_uploader("Video", type=["mp4"])
    if st.button("💾 Save Observation"):
        st.session_state.community_notes.append({"title": e_title, "lat": e_lat, "lon": e_lon, "category": e_cat, "privacy": e_priv, "notes": e_notes})
        st.success("Saved!")

# ------------------------------------------
# TAB 6: WITNESS REPORT PARSER
# ------------------------------------------
with tab_parser:
    st.subheader("Witness Report Objective Data Extractor")
    raw = st.text_area("Raw Witness Statement", height=120)
    if st.button("Parse Report"):
        concrete, conjecture = parse_witness_report(raw)
        c1, c2 = st.columns(2)
        with c1:
            st.success("🟢 Concrete Observations")
            for c in (concrete or []): st.markdown(f"- {c}")
        with c2:
            st.warning("🟡 Witness Conjecture")
            for c in (conjecture or []): st.markdown(f"- {c}")

# ------------------------------------------
# TAB 7: ONX / GPX EXPORTER
# ------------------------------------------
with tab_export:
    st.subheader("Export Targets to onX Maps")
    gpx = f"""<?xml version="1.0"?><gpx version="1.1"><wpt lat="{lat_input}" lon="{lon_input}"><name>Target</name></wpt></gpx>"""
    st.code(gpx, language="xml")
    st.download_button("📥 Download .GPX File", data=gpx, file_name="target.gpx")
