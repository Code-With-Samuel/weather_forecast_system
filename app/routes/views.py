from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests

views = Blueprint("views", __name__)

# Store token in session
@views.route("/set_token", methods=["POST"])
def set_token():
    session["jwt_token"] = request.form.get("token")
    return redirect(url_for("views.dashboard"))

# Dashboard route (Requires JWT)
@views.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "jwt_token" not in session:
        return redirect(url_for("views.login"))

    weather_data = None
    return render_template("dashboard.html", weather_data=weather_data)

# Fetch Weather Data from FastAPI
@views.route("/get_weather", methods=["POST"])
def get_weather():
    if "jwt_token" not in session:
        return redirect(url_for("views.login"))

    city = request.form.get("city")
    token = session["jwt_token"]
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"http://127.0.0.1:8000/weather/current_weather?city={city}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city,
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "pressure": data["pressure"],
                "weather_condition": data["weather_condition"],
                "forecast": data["forecast"],  # Assuming FastAPI returns a 3-day forecast
            }
        else:
            weather_data = None
            flash("City not found or unauthorized request.", "error")
    except requests.exceptions.RequestException:
        flash("Error connecting to the weather service.", "error")
        weather_data = None

    return render_template("dashboard.html", weather_data=weather_data)

# Logout
@views.route("/logout")
def logout():
    session.pop("jwt_token", None)
    return redirect(url_for("views.login"))
