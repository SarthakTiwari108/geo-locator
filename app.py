from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)  # allow all origins

geolocator = Nominatim(user_agent="geo_app")

@app.route("/api", methods=["POST"])
def geo_api():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"message": "No query provided"}), 400

    query = data["query"]

    # Check if input is coordinates (lat,lon) or address
    if "," in query:
        try:
            lat, lon = map(float, query.split(","))
            location = geolocator.reverse((lat, lon), language="en")
            if location:
                return jsonify({"address": location.address})
            else:
                return jsonify({"message": "Address not found"}), 404
        except:
            return jsonify({"message": "Invalid coordinates"}), 400
    else:
        location = geolocator.geocode(query, language="en")
        if location:
            return jsonify({"latitude": location.latitude, "longitude": location.longitude})
        else:
            return jsonify({"message": "Location not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
