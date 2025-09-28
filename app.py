from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from geopy.geocoders import Nominatim

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

geolocator = Nominatim(user_agent="geo_locator_app")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    try:
        if data["mode"] == "coords":
            address = data.get("address")
            location = geolocator.geocode(address)
            if location:
                return jsonify({
                    "status": "success",
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
            else:
                return jsonify({"status": "error", "message": "Address not found"})

        elif data["mode"] == "address":
            lat = data.get("latitude")
            lon = data.get("longitude")
            location = geolocator.reverse(f"{lat},{lon}")
            if location:
                return jsonify({
                    "status": "success",
                    "address": location.address
                })
            else:
                return jsonify({"status": "error", "message": "Coordinates not found"})

        else:
            return jsonify({"status": "error", "message": "Invalid mode"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
