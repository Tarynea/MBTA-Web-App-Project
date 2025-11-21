from flask import Flask, render_template, request
import mbta_helper


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # Render the home page with the form
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    # Get the place name from the form
    place_name = request.form.get("place_name", "").strip()

    if not place_name:
        return render_template(
            "error.html",
            message="Please enter a valid place name or address."
        )

    # Use helper to find nearest station
    station_name, wheelchair_code = mbta_helper.find_stop_near(place_name)

    if station_name is None:
        return render_template(
            "error.html",
            message=f"Sorry, we couldn't find any MBTA stops near '{place_name}'."
        )

    # Translate wheelchair code
    if wheelchair_code == 1:
        wheelchair_info = "Wheelchair accessible."
    elif wheelchair_code == 2:
        wheelchair_info = "Not wheelchair accessible."
    else:
        wheelchair_info = "No accessibility information available."

    # --- NEW: get weather near this place ---
    lat, lng = mbta_helper.get_lat_lng(place_name)
    weather_description = None
    weather_temp = None

    if lat is not None and lng is not None:
        w_desc, w_temp = mbta_helper.get_weather(lat, lng)
        weather_description = w_desc
        weather_temp = w_temp

    return render_template(
        "mbta_station.html",
        place_name=place_name,
        station_name=station_name,
        wheelchair_info=wheelchair_info,
        weather_description=weather_description,
        weather_temp=weather_temp,
    )


if __name__ == "__main__":
    app.run(debug=True)
