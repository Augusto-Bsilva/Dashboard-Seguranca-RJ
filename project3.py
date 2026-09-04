import pandas as pd 
import streamlit as st
import googlemaps
import requests


API_KEY = 'AIzaSyAUtG2Ady_JEfa3Jd-rz2A20Pi067aEn2Y'


denver_locations = [
    {'location': 'Pikes Peak', 'Address': '515 Ruxton Ave, Manitou Springs, CO 80829'},
    {'location': 'Magnolia Road', 'Address': '45 Peak to Peak Hwy, Nederland, CO 80466'},

    {'location': 'Cors Field', 'Address': '2001 Blake Street, Denver, CO 80205'},
    {'location': 'Denver Card Show', 'Address': '5004 National Western Dr, Denver, CO 80216'},

    {'location': 'Fillmore Auditorium', 'Address': '2001 Blake Street, Denver, CO 80205'},
    {'location': 'Mission Ballroom', 'Address': '4242 Wynkoop St, Denver, CO 80216'},
    {'location': 'Red Rock Amphitheater', 'Address': '18300 W Alameda Pkwy, Morrison, CO 80465'}
]

st.title("House Distance Finder (Routes API)")
st.write("Enter your starting address")

with st.form("address_form"):
    street = st.text_input("Street Address")
    city = st.text_input("City")
    state = st.text_input("State")
    zip_code = st.text_input("Zip Code")
    submitted = st.form_submit_button("Submit")

if submitted:
    user_address = f"{street}, {city}, {state} {zip_code}"
    st.success(f"Calculating distances from: {user_address}")

    def get_distance_miles(origin,destination):
        url = f"https://routes.googleapis.com/directions/v2:computeRoutes?key={API_KEY}"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-FieldMask": "routes.distanceMeters"
        }

        body = {
            "origin": {"address":origin},
            "destination": {"address": destination},
            "travelMode": "DRIVE"
        }

        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

            meters = data["routes"][0]["distanceMeters"]
            miles = round(meters / 1609.34,2)
            return miles
        except Exception as e:
            st.warning(f"Error for {destination}: {e}")
            return None
    results = []
    for loc in denver_locations:
        miles = get_distance_miles(user_address, loc['Address'])
        results.append({
            "Location": loc['location'],
            "Address": loc['Address'],
            "Distance (mi)": miles,
        })

    df = pd.DataFrame(results).set_index('Location')
    df2 = df.sort_values('Distance (mi)')
    st.dataframe(df2)