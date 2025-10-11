import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
from openai import OpenAI  # ✅ NEW SDK import

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
    load_dotenv(dotenv_path)
    st.info("✅ Loaded local .env file.")
else:
    st.info("☁️ Using Streamlit Cloud secrets (no local .env found).")

# ------------------- Load API keys -------------------
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or st.secrets.get("OPENWEATHER_API_KEY")
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY") or st.secrets.get("OPENCAGE_API_KEY")

if not OPENAI_KEY:
    st.error("⚠️ OpenAI API key not found. Please set it in Streamlit Secrets or .env file.")
    st.stop()

# ✅ Initialize the new OpenAI client
client = OpenAI(api_key=OPENAI_KEY)

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

# ======================================================================================
# Helper: Fetch Places using OpenCage API (instead of OSM)
# ======================================================================================
def fetch_osm_places(destination, radius_km=5, limit=20):
    """Use OpenCage API to find coordinates and generate mock nearby POIs."""
    try:
        if not OPENCAGE_API_KEY:
            st.warning("No OpenCage API key found — skipping map lookup.")
            return None, []

        geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={destination}&key={OPENCAGE_API_KEY}"
        geo_data = requests.get(geo_url, timeout=10).json()

        if not geo_data.get("results"):
            st.warning("Could not find destination location via OpenCage.")
            return None, []

        lat = geo_data["results"][0]["geometry"]["lat"]
        lon = geo_data["results"][0]["geometry"]["lng"]

        # Generate a few sample nearby points for map display
        places = []
        for i in range(min(limit, 10)):
            places.append({
                "name": f"Point of Interest {i+1}",
                "lat": lat + (i * 0.01 * (1 if i % 2 == 0 else -1)),
                "lon": lon + (i * 0.01 * (1 if i % 3 == 0 else -1))
            })

        return (lat, lon), places

    except Exception as e:
        st.warning(f"⚠️ Location fetch failed: {e}")
        return None, []

# ======================================================================================
# Helper: Weather Info
# ======================================================================================
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

# ======================================================================================
# Helper: AI Itinerary Generation
# ======================================================================================
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

    # ✅ Use new OpenAI client call syntax
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI travel planner for students."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_output_tokens=900
    )

    return response.choices[0].message.content.strip()

# ======================================================================================
# Main Application Logic
# ======================================================================================
if st.button("✨ Generate My Plan"):
    try:
        with st.spinner("Getting weather data..."):
            weather_summary = get_weather_summary(destination)

        with st.spinner("Fetching nearby places..."):
            coords, places = fetch_osm_places(destination, radius_km, max_pois)
            if not coords:
                st.warning("⚠️ Could not fetch live map data — continuing without map.")
                coords = (0, 0)
                places = [{"name": destination, "lat": 0, "lon": 0}]

        with st.spinner("Generating AI Itinerary..."):
            itinerary_text = generate_itinerary(destination, start_date, end_date, budget, interests, places, weather_summary)

        # Display itinerary
        st.subheader("🧭 Your Personalized Itinerary")
        st.markdown(itinerary_text)

        st.download_button("📥 Download Itinerary (TXT)", itinerary_text, file_name=f"{destination}_itinerary.txt")

        # Display map
        st.markdown("---")
        st.subheader("🗺️ Explore the Destination")
        st.success(f"Found {len(places)} nearby places for {destination}!")
        st.map(pd.DataFrame(places))

    except Exception as e:
        st.error(f"An error occurred: {e}")
