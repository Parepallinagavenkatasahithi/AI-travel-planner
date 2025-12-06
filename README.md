# 🎒 AI Travel Planner for Students

An AI-powered travel planner designed to help students plan
**affordable, personalized, and efficient trips** with ease.\
Built using **Streamlit**, **OpenAI GPT models**, and public APIs for
location and weather data.

*🧠 Developed during my internship at **Edunet Foundation** as part of
an AI and Cloud Computing project.*

## 🚀 Features

-   ✈️ **AI-generated itineraries** -- Personalized trip plans based on
    destination, budget, and interests\
-   ☁️ **Weather insights** -- Real-time weather summaries from
    OpenWeather API\
-   📍 **Location mapping** -- Fetches coordinates & nearby attractions
    using OpenCage API\
-   💰 **Budget optimization** -- Smart expense allocation for students\
-   🧳 **Packing checklist** -- AI-suggested essentials based on climate
    & trip duration\
-   🎯 **Student-focused tips** -- Affordable recommendations for stay,
    food, and activities

## 🛠️ Tech Stack

  Category        Technology
  --------------- -----------------------------------------------------
  Frontend        Streamlit
  Backend         Python
  APIs            OpenAI API, OpenWeather API, OpenCage Geocoding API
  Environment     dotenv
  Data Handling   Pandas
  Hosting         Streamlit Cloud

## 🧩 Project Structure

    AI-travel_planner/
    │
    ├── AI-travel_planner.py      # Main Streamlit app
    ├── .env                      # API keys for local setup
    └── requirements.txt          # Dependencies

## 🔑 Environment Setup

Create a `.env` file in the project root:

    OPENAI_API_KEY=your_openai_api_key
    OPENWEATHER_API_KEY=your_openweather_api_key
    OPENCAGE_API_KEY=your_opencage_api_key

If using **Streamlit Cloud**, store keys under Settings → Secrets.

## ▶️ How to Run the App

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/Parepallinagavenkatasahithi/AI-travel-planner.git
cd AI-travel-planner
```

### 2️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit app

``` bash
streamlit run AI-travel_planner.py
```

### 4️⃣ Open your browser

The app will be available at:\
https://ai-travel--planner.streamlit.app/

## 💡 How It Works

1.  🏙️ Enter destination, dates, budget, and interests\
2.  🌦️ App fetches real-time weather & nearby attractions\
3.  🤖 AI generates:
    -   Day-wise schedule\
    -   Student-friendly tips\
    -   Budget breakdown\
    -   Smart packing list\
4.  🗺️ Interactive map with markers

## 🧭 Example Output

### 🎯 3-Day Student Trip to Goa, India

**Weather:** Sunny, \~30°C\
**Budget:** ₹5000

#### 🏖️ Day 1: Beach Day

-   Morning: Calangute Beach + breakfast\
-   Afternoon: Explore Fort Aguada & markets\
-   Evening: Street food at Baga Beach

#### 💸 Budget Breakdown

Stay ₹2000 \| Food ₹1000 \| Transport ₹800 \| Activities ₹1200

#### 🎒 Packing List

Light clothes, sunscreen, slippers, reusable bottle, camera

## 🎓 Internship Acknowledgment

This project was developed during my internship at **Edunet
Foundation**, focusing on AI and Cloud Computing applications.

## 📚 Future Enhancements

-   Live hotel & transport API integration\
-   Multi-destination planning\
-   Downloadable PDF itineraries\
-   AI chatbot assistant

## 👨‍💻 Author

**Parepalli Naga Venkata Sahithi**\
📧 sahithiparepalli11@gmail.com\
🔗 https://www.linkedin.com/in/naga-venkata-sahithi-parepalli-59a844298/
