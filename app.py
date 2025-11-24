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

    # 1) Geocode the place
    place_lat, place_lng = mbta_helper.get_lat_lng(place_name)
    if place_lat is None or place_lng is None:
        return render_template(
            "error.html",
            message=f"Sorry, we couldn't locate '{place_name}'. Try a different place name."
        )

    # 2) Nearest station with details
    (station_name,
     wheelchair_code,
     stop_lat,
     stop_lng,
     stop_id) = mbta_helper.get_nearest_station_details(place_lat, place_lng)

    if station_name is None:
        return render_template(
            "error.html",
            message=f"Sorry, we couldn't find any MBTA stops near '{place_name}'."
        )

    # 3) Wheelchair info text
    if wheelchair_code == 1:
        wheelchair_info = "Wheelchair accessible."
    elif wheelchair_code == 2:
        wheelchair_info = "Not wheelchair accessible."
    else:
        wheelchair_info = "No accessibility information available."

    # 4) Weather near the place
    weather_description = None
    weather_temp = None
    try:
        w_desc, w_temp = mbta_helper.get_weather(place_lat, place_lng)
        weather_description = w_desc
        weather_temp = w_temp
    except Exception:
        weather_description = None
        weather_temp = None

    # 5) Walking time from place → stop
    walking_minutes = None
    if stop_lat is not None and stop_lng is not None:
        walking_minutes = mbta_helper.estimate_walking_time_minutes(
            place_lat, place_lng, stop_lat, stop_lng
        )

    # 6) Static map centered on the stop
    map_url = None
    if stop_lat is not None and stop_lng is not None:
        map_url = mbta_helper.get_static_map_url(stop_lat, stop_lng)

    # 7) MBTA alerts for that stop
    alerts = []
    if stop_id is not None:
        try:
            alerts = mbta_helper.get_alerts_for_stop(stop_id)
        except Exception:
            alerts = []

    # 8) Render template
    return render_template(
        "mbta_station.html",
        place_name=place_name,
        station_name=station_name,
        wheelchair_info=wheelchair_info,
        weather_description=weather_description,
        weather_temp=weather_temp,
        walking_minutes=walking_minutes,
        map_url=map_url,
        alerts=alerts,
    )


if __name__ == "__main__":
    app.run(debug=True)
