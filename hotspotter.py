# Import dependencies
from geopy.geocoders import Nominatim
import folium
import webbrowser
import os

# Call the Nomination tool
loc = Nominatim(user_agent="GetLoc")

# Get the input of the location
Loc = input("Input the location\n > ")
getLoc = loc.geocode(Loc)

# Print the location to check if it works
print(getLoc.address)
print("Latitude =", getLoc.latitude, "\n")
print("Longitude =", getLoc.longitude, "\n")

# Now plot it
m = folium.Map([getLoc.latitude, getLoc.longitude], zoom_start=11)

# Add a red marker
folium.Marker(
    location=[getLoc.latitude, getLoc.longitude],
    tooltip="Accident Location",
    popup=getLoc.address,
    icon=folium.Icon(color="red", icon="cloud"),  # Set marker color to red
).add_to(m)

# Save the map to an HTML file
output_file = "output.html"
m.save(output_file)

# Get the absolute file path and open in the browser
webbrowser.open_new_tab(f"file://{os.path.abspath(output_file)}")
