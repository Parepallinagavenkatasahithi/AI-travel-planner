import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
import openai

# ======================================================================================
# SAFE PAGE CONFIG (works on Streamlit Cloud reloads)
# ======================================================================================
if "page_configured" not in st.session_state:
    st.set_page_config(
        page_title="AI Travel Planner for Students",
        page_icon="🎒",
        layout="wide"
    )
    st.session_state["page_configured"] = True
# ======================================================================================

# ------------------- Load environment variables -------------------
dotenv_path = Path(__file__).parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)  # Local development
    st.info("✅ Loaded local .env file.")
else:
    st.info("☁️ Using Streamlit Cloud secrets (no local .env found).")

# Load keys from environment or Streamlit secrets
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or st.secrets.get("OPENWEATHER_API_KEY")

if not OPENAI_KEY:
    st.error("⚠️ OpenAI API key not found. Please set it in Streamlit Secrets or .env file.")
    st.stop()

openai.api_key = OPENAI_KEY

# ------------------- App Header -------------------
st.title("🎒 AI Travel Planner for Students")
st.caption("Plan efficient, budget-friendly trips with AI-powered itineraries — perfect for students!")


# ------------------- Sidebar inputs -------------------
with st.sidebar:
    st.header("✈️ Trip Details")
    destination = st.text_input("Destination City", "Goa, India")
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date", datetime.today() + timedelta(days=2))
    budget = st.number_input("Total Budget (₹)", min_value=1000, step=500, value=5000)
    interests = st.multiselect(
        "Your Interests",
        ["Beaches", "Museums", "Nightlife", "Shopping", "Food", "Nature", "Adventure", "Culture"],
        default=["Beaches", "Food"]
    )
    radius_km = st.slider("Search radius (km)", 1, 20, 5)
    max_pois = st.slider("Max POIs to fetch", 5, 50, 20)
    st.markdown("---")

# ------------------- Helper: Fetch OSM POIs -------------------
def fetch_osm_places(destination, radius_km=5, limit=20):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": destination, "format": "json", "limit": 1}
    r = requests.get(url, params=params, headers={"User-Agent": "ai-travel-planner/1.0"}, timeout=10)
    data = r.json()
    if not data:
        return None, []
    lat, lon = float(data[0]["lat"]), float(data[0]["lon"])

    overpass_query = f"""
    [out:json][timeout:25];
    (
      node(around:{radius_km*1000},{lat},{lon})["name"];
      way(around:{radius_km*1000},{lat},{lon})["name"];
    );
    out center {limit};
    """
    res = requests.post("https://overpass-api.de/api/interpreter", data={"data": overpass_query}, timeout=25)
    pois_data = res.json().get("elements", [])
    places = []
    for p in pois_data:
        name = p.get("tags", {}).get("name")
        if not name:
            continue
        latp = p.get("lat") or p.get("center", {}).get("lat")
        lonp = p.get("lon") or p.get("center", {}).get("lon")
        if latp and lonp:
            places.append({"name": name, "lat": latp, "lon": lonp})
    return (lat, lon), places[:limit]

# ------------------- Weather Helper -------------------
def get_weather_summary(destination):
    if not WEATHER_API_KEY:
        return "Weather info not available (missing key)."
    try:
        geo = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={destination}&limit=1&appid={WEATHER_API_KEY}"
        ).json()
        if not geo:
            return "Could not find city."
        lat, lon = geo[0]["lat"], geo[0]["lon"]
        weather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        ).json()
        desc = weather["weather"][0]["description"].capitalize()
        temp = weather["main"]["temp"]
        return f"{desc}, around {temp}°C"
    except Exception as e:
        return f"Error: {e}"

# ------------------- AI Itinerary -------------------
def generate_itinerary(destination, start_date, end_date, budget, interests, places, weather_summary):
    days = (end_date - start_date).days + 1
    place_names = ", ".join([p["name"] for p in places]) if places else "local attractions"

    prompt = f"""
    You are a student travel planner AI.
    Create a {days}-day itinerary for {destination}.
    Weather: {weather_summary}.
    Focus on fun, low-cost, student-friendly experiences.
    Total budget: ₹{budget}.
    Traveler interests: {', '.join(interests)}.
    Suggested local spots: {place_names}.

    Include:
    1. Day-wise itinerary (Morning, Afternoon, Evening)
    2. Budget breakdown by category (Stay, Food, Transport, Activities)
    3. Smart packing list based on weather and trip length
    4. Student travel tips
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI travel planner for students."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=900
    )

    return response.choices[0].message.content.strip()

# ------------------- Main -------------------
if st.button("✨ Generate My Plan"):
    try:
        with st.spinner("Getting weather data..."):
            weather_summary = get_weather_summary(destination)

        with st.spinner("Fetching nearby places..."):
            coords, places = fetch_osm_places(destination, radius_km, max_pois)
            if not coords:
                st.error("Could not find destination on map.")
                st.stop()

        with st.spinner("Generating AI Itinerary..."):
            itinerary_text = generate_itinerary(destination, start_date, end_date, budget, interests, places, weather_summary)

        # Display itinerary
        st.subheader("🧭 Your Personalized Itinerary")
        st.markdown(itinerary_text)

        st.download_button("📥 Download Itinerary (TXT)", itinerary_text, file_name=f"{destination}_itinerary.txt")

        # Display map
        st.markdown("---")
        st.subheader("🗺️ Explore the Destination")
        st.success(f"Found {len(places)} nearby places in {destination}!")
        st.map(pd.DataFrame(places))

    except Exception as e:
        st.error(f"An error occurred: {e}")
