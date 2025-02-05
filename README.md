# India Phone Usage Analytics Dashboard

A comprehensive dashboard that visualizes mobile phone usage trends across India using interactive maps and real-time data analytics.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
---

## Overview

The **India Phone Usage Analytics Dashboard** helps users explore mobile usage patterns across Indian states. The dashboard displays an interactive map that visualizes key metrics such as average screen time, total users, and primary usage trends for each state. It connects to a MySQL database for real-time data and leverages modern Python libraries to ensure smooth data processing and a user-friendly interface.

---

## Features

- **Interactive Map:**  
  Displays a choropleth map of India where states are color-coded based on average screen time.
  
- **Detailed State Data:**  
  Clickable markers on the map reveal additional details for each state, such as total users and top usage trends.
  
- **Real-Time Data Processing:**  
  Uses Pandas and SQLAlchemy to retrieve and process data directly from a MySQL database.
  
- **User-Friendly Interface:**  
  Built with Streamlit and enhanced with custom CSS for a clean, responsive design.
  
- **Additional Analytics:**  
  Provides extra insights with bar charts displaying demographic data and popular device brands.

---

## Technologies Used

- **Python:** The main programming language.
- **Streamlit:** For building the interactive web application.
- **Folium:** For creating interactive maps.
- **Pandas:** For data manipulation and analysis.
- **SQLAlchemy:** For connecting to and querying the MySQL database.
- **MySQL:** The relational database used to store mobile usage data.
- **GeoJSON:** For representing geographical data of Indian states.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/india-phone-usage-analytics.git
   cd india-phone-usage-analytics

2. Set Up a Virtual Environment (Optional but Recommended):

python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate


3. Install Dependencies:

Ensure you have Python 3.7+ installed, then run:

pip install -r requirements.txt


4. Configure Your MySQL Database:

Ensure you have a MySQL server running.

Create a database named phoneusagedata and set up a table (e.g., user_data) with the required schema.

Update the connection string in the code (in app.py) if necessary.





---

## Usage

1. Run the Application:

Start the Streamlit app by running:

streamlit run app.py


2. Open the Dashboard:

Open the local URL provided in the terminal (usually http://localhost:8501) in your web browser to interact with the dashboard.

---


Enjoy exploring mobile usage trends across India with this interactive analytics dashboard!



