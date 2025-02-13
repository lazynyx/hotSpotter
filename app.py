from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import folium
from folium.plugins import HeatMap
import os
import json
import webbrowser

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define CSV file for storing accident data
ACCIDENT_DATA_FILE = "accident_data.csv"

# Ensure the CSV file exists and create it if not
if not os.path.exists(ACCIDENT_DATA_FILE):
    df = pd.DataFrame(columns=["Address", "Latitude", "Longitude", "Description"])
    df.to_csv(ACCIDENT_DATA_FILE, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        data = request.json.get('data')  # Get the report data from the frontend
        df = pd.DataFrame(data[1:], columns=data[0])  # Convert to pandas DataFrame
        
        # Add the new data to the CSV file
        df.to_csv(ACCIDENT_DATA_FILE, mode='a', header=False, index=False)
        
        return jsonify({"message": "Data successfully received and stored."})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/view_accidents')
def view_accidents():
    # Load the stored accident data from the CSV file
    df = pd.read_csv(ACCIDENT_DATA_FILE)
    return render_template('view_accidents.html', accidents=df.to_dict(orient='records'))

# @app.route('/generate_heatmap')
# def generate_heatmap():
#     # Load the stored accident data from the CSV file
#     df = pd.read_csv(ACCIDENT_DATA_FILE)
    
#     # Create a map centered around the average location
#     avg_lat = df['Latitude'].mean()
#     avg_lon = df['Longitude'].mean()
#     m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

#     # Add markers for each accident
#     for _, row in df.iterrows():
#         folium.Marker([row['Latitude'], row['Longitude']], 
#                       popup=f"<strong>{row['Address']}</strong><br>{row['Description']}",
#                       icon=folium.Icon(color='red', icon='info-sign')).add_to(m)

#     # Save the heatmap as an HTML file in the static folder
#     heatmap_file = "static/heatmap.html"
#     m.save(heatmap_file)
#     webbrowser.open(heatmap_file)

#     return jsonify({"message": "Heatmap generated.", "file": heatmap_file})

@app.route('/authority')
def authority():
    # Load the stored accident data
    df = pd.read_csv(ACCIDENT_DATA_FILE)
    
    # Create a map centered around the average location
    avg_lat = df['Latitude'].mean()
    avg_lon = df['Longitude'].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Add distinctive markers for each accident (Authority Marking)
    for _, row in df.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], 
                      popup=f"<strong>{row['Address']}</strong><br>{row['Description']}",
                      icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)

    # Save the map for authority
    authority_map_file = "template/authority_map.html"
    m.save(authority_map_file)

    return render_template('authority_map.html', map_file=authority_map_file)

@app.route('/generate_heatmap')
def generate_heatmap():
    # Load the stored accident data from the CSV file
    df = pd.read_csv(ACCIDENT_DATA_FILE)
    
    # Create a map centered around the average location
    avg_lat = df['Latitude'].mean()
    avg_lon = df['Longitude'].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Prepare data for heatmap
    heat_data = [[row['Latitude'], row['Longitude']] for _, row in df.iterrows()]

    # Add HeatMap layer
    from folium.plugins import HeatMap
    HeatMap(heat_data).add_to(m)

    # Save the heatmap as an HTML file in the static folder
    heatmap_file = "static/heatmap.html"
    m.save(heatmap_file)

    # Open the heatmap in the browser
    webbrowser.open(heatmap_file)

    return jsonify({"message": "Heatmap generated.", "file": heatmap_file})

# To see the fake data 
@app.route("/heatmap")
def view_heatmap():
    FakeHeatMap = "templates/heatmap.html"
    return render_template(FakeHeatMap)

if __name__ == '__main__':
    app.run(debug=True)
