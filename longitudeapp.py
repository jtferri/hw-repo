#Create a streamlit app where a user enters longitude and latitude 
# and it creates a map with with a little icon over the spot that you selected

import streamlit as st
import folium


def main():
    st.title("Longitude and Latitude Map")

    st.write("Enter the longitude and latitude to create a map with a marker at the selected location.")

    # Input for longitude and latitude, %.4f formats the number to 4 decimal places
    longitude = st.number_input("Enter longitude:", format="%.4f")
    latitude = st.number_input("Enter latitude:", format="%.4f")

    if st.button("Create Map"):
        if -180 <= longitude <= 180 and -90 <= latitude <= 90:
            # Create a map centered at the entered location
            map = folium.Map(location=[latitude, longitude], zoom_start=10)

            # Add a marker at the entered location
            folium.Marker([latitude, longitude], popup="Selected Location").add_to(map)

            # Display the map
            folium_static(map)
        else:
            st.write("Please enter valid longitude and latitude values.")

if __name__ == "__main__":
    main()