🎒 AI Travel Planner for Students

An AI-powered travel planner designed to help students plan affordable, personalized, and efficient trips with ease.
Built using Streamlit, OpenAI GPT models, and public APIs for location and weather data.

_🧠 Developed during my internship at Edunet Foundation as part of an AI and Cloud Computing project._
________________________________________________________________________________________________________
**🚀 Features**
->✈️ AI-generated itineraries – Personalized trip plans based on destination, budget, and interests.
->☁️ Weather insights – Real-time weather summaries from OpenWeather API.
->📍 Location mapping – Fetches coordinates and nearby points of interest using OpenCage API.
->💰 Budget optimization – Smart allocation of expenses for students.
->🧳 Packing checklist – AI-suggested essentials based on climate and trip duration.
->🎯 Student-focused travel tips – Affordable recommendations for accommodation, food, and activities.
_______________________________________________________________________________________________________
**🛠️ Tech Stack**
Category	Technology
Frontend	Streamlit
Backend	Python
APIs	OpenAI API, OpenWeather API, OpenCage Geocoding API
Environment	dotenv
Data Handling	Pandas
Hosting	Streamlit Cloud
_______________________________________________________________________________________________________
**🧩 Project Structure**
AI-travel_planner/
│
├── AI-travel_planner.py   # Main Streamlit application
├── .env                   # (Optional) API keys for local setup
└── requirements.txt        # Dependencies (Streamlit, openai, requests, pandas, python-dotenv)
_________________________________________________________________________________________________________
**🔑 Environment Setup**
Create a .env file in the project root (same directory as the Python script):
OPENAI_API_KEY=your_openai_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
OPENCAGE_API_KEY=your_opencage_api_key

If deploying on Streamlit Cloud, you can securely store these keys under
Settings → Secrets.
__________________________________________________________________________________________________________
**▶️ How to Run the App
Clone this repository:**
git clone https://github.com/Parepallinagavenkatasahithi/AI-travel-planner.git
cd AI-travel-planner

**Install dependencies:**
->pip install -r requirements.txt
->Run the Streamlit app:
-streamlit run AI-travel_planner.py

**Open your browser:**
The app will run at https://ai-travel--planner.streamlit.app/
______________________________________________________________________________________________
**💡 How It Works**
->🏙️ Enter destination, dates, budget, and interests.
->🌦️ The app fetches real-time weather and nearby attractions.
->🤖 AI generates a custom itinerary, including:
->Day-wise schedule (morning, afternoon, evening)
->Student-friendly travel tips
->Budget breakdown
->Smart packing list
->🗺️ The app then displays an interactive map with color-coded markers.
_______________________________________________________________________________________________
_🧭 Example Output_
**🎯 3-Day Student Trip to Goa, India**
Weather: Sunny, around 30°C
Budget: ₹5000

**Day 1: Beach Day 🏖️**
- Morning: Visit Calangute Beach, breakfast at local café
- Afternoon: Explore Fort Aguada and markets
- Evening: Street food at Baga Beach

**💸 Budget Breakdown:**
Stay ₹2000 | Food ₹1000 | Transport ₹800 | Activities ₹1200

**🎒 Packing List:**
Light clothes, sunscreen, slippers, reusable bottle, camera

**🎓 Internship Acknowledgment**
This project was developed as part of my internship at Edunet Foundation,
focusing on applying AI and Cloud Computing to real-world applications.
It demonstrates how AI can enhance student travel planning through personalization, automation, and data integration.
_____________________________________________________________________________________________________________________________
**📚 Future Enhancements**
->Integration with live hotel and transport APIs.
->Multi-destination trip planning.
->Downloadable itineraries in PDF format.
->AI chatbot assistant for travel FAQs.
_______________________________________________________________________________________________________________________________
**👨‍💻 Author**
Parepalli Naga Venkata Sahithi,
**Intern at Edunet Foundation**
📧 sahithiparepalli11@gmail.com
🔗 https://www.linkedin.com/in/naga-venkata-sahithi-parepalli-59a844298/
