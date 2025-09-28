from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize geolocator
geolocator = Nominatim(user_agent="geo_locator_app")

@app.route("/api", methods=["POST"])
def api():
    """
    API endpoint to handle geocoding and reverse geocoding.
    mode = "coords" → Convert address to coordinates
    mode = "address" → Convert coordinates to address
    """
    data = request.get_json()

    if not data or "mode" not in data:
        return jsonify({"status": "error", "message": "Missing 'mode' in request"}), 400

    try:
        mode = data["mode"].lower()

        if mode == "coords":
            address = data.get("address")
            if not address:
                return jsonify({"status": "error", "message": "Address is required"}), 400

            location = geolocator.geocode(address)
            if location:
                return jsonify({
                    "status": "success",
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
            return jsonify({"status": "error", "message": "Address not found"}), 404

        elif mode == "address":
            lat = data.get("latitude")
            lon = data.get("longitude")
            if lat is None or lon is None:
                return jsonify({"status": "error", "message": "Latitude and Longitude are required"}), 400

            location = geolocator.reverse(f"{lat},{lon}")
            if location:
                return jsonify({
                    "status": "success",
                    "address": location.address
                })
            return jsonify({"status": "error", "message": "Coordinates not found"}), 404

        else:
            return jsonify({"status": "error", "message": "Invalid mode"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/")
def home():
    return "🌍 Geo Locator Flask App is running successfully 🚀"


if __name__ == "__main__":
    app.run(debug=True)
