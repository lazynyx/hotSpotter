import pandas as pd
import folium
from folium.plugins import HeatMap
import webbrowser

def generate_heatmap(csv_file):
    # Load CSV file
    df = pd.read_csv(csv_file)
    
    # Standardize column names
    df.rename(columns={"Latitude": "lat", "Longitude": "lon", "Description": "des"}, inplace=True)
    
    # Check if required columns exist
    required_columns = {'lat', 'lon'}
    if not required_columns.issubset(df.columns):
        raise ValueError("CSV file must contain 'Latitude' and 'Longitude' columns")
    
    # Convert lat/lon to numeric values
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df.dropna(subset=['lat', 'lon'], inplace=True)
    
    # Create map centered at Bengaluru
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)
    
    # Add heatmap
    heat_data = df[['lat', 'lon']].values.tolist()
    HeatMap(heat_data).add_to(m)
    
    # Save map
    heatmap_file = "heatmap.html"
    m.save(heatmap_file)
    print(f"Heatmap saved as {heatmap_file}")
    
    # Open in browser
    webbrowser.open(heatmap_file)

# Run the function
generate_heatmap("fake_data.csv")
