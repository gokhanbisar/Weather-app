import json
import tkinter as tk
import requests
from tkinter import PhotoImage
from PIL import Image, ImageTk
import customtkinter as ctk


# OpenWeatherMap API key
API_KEY = "9e8503dddb7ef0a3b9d50c02e8f7fc8e"


def example_func_button():
    """
    Triggered when the button is clicked.
    Fetches weather data for the entered city from the API,
    updates the background image based on the weather condition,
    and displays the weather details on the canvas.
    """
    global data
    city = city_entry.get()
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()

        # Select background image based on weather condition ID
        weather_id = int(data["weather"][0]["id"])
        if weather_id == 800:  # Clear sky
            change_bg("images/sun.png")
        elif 801 <= weather_id <= 804:  # Clouds
            change_bg("images/clouds.png")
        elif 200 <= weather_id <= 232:  # Thunderstorm
            change_bg("images/storm.png")
        elif 300 <= weather_id <= 321:  # Drizzle
            change_bg("images/drizzle.png")
        elif 500 <= weather_id <= 531:  # Rain
            change_bg("images/rain.png")
        elif 600 <= weather_id <= 622:  # Snow
            change_bg("images/snow.png")
        elif 701 <= weather_id <= 781:  # Fog / Atmosphere
            change_bg("images/fog.png")
        else:  # Unknown condition
            change_bg("images/background.png")

        # Clear old weather data and update with new one
        data_wea_clear()
        data_wea()


def data_wea_clear():
    """
    Clears previously displayed weather data from the canvas.
    """
    global data
    canvas.delete("city")
    canvas.delete("temp")
    canvas.delete("description")
    canvas.delete("temp_min")
    canvas.delete("temp_max")


def data_wea():
    """
    Displays weather data fetched from the API on the canvas.
    """
    global data
    canvas.create_text((85, 40), text=f"{city_entry.get().capitalize()}",
                       font="Arial 17 bold", fill="#ffffff", tag="city")
    canvas.create_text((85, 63), text=f"°C {data['main']['temp']}",
                       font="Arial 13 bold", fill="#ffffff", tag="temp")
    canvas.create_text((113, 80), text=f"{data['weather'][0]['description']}",
                       font="Arial 13 bold", fill="#fff", tag="description")
    canvas.create_text((110, 200), text=f"Min Temp : {data['main']['temp_min']}",
                       font="Arial 11 bold", fill="#fff", tag="temp_min")
    canvas.create_text((110, 225), text=f"Max Temp : {data['main']['temp_max']}",
                       font="Arial 11 bold", fill="#fff", tag="temp_max")


#### ----- SCREEN SETTINGS ----- ####
screen = tk.Tk()
screen.title("Weather App")
screen.geometry("230x350")
screen.minsize(230, 350)

# Canvas setup
canvas = tk.Canvas(screen, height=350, width=230)
canvas.pack(side="top")

# Background image
bg_img = tk.PhotoImage(file="images/background.png")
bg_label = canvas.create_image((0, 0), image=bg_img, anchor=tk.N + tk.W)

# City input label
city_text = canvas.create_text((110, 248), text="City Name : ",
                               font="Arial 7 bold", fill="#ffffff")


def change_bg(file_path: str):
    """
    Changes the background image of the canvas.
    """
    global bg_img
    bg_img = tk.PhotoImage(file=file_path)
    canvas.itemconfig(bg_label, image=bg_img)


# City input box
city_entry = tk.Entry(width=12, bg="#fff", highlightthickness=0, bd=0)
city_entry.place(x=75, y=261)

# Weather fetch button
button_click = ctk.CTkButton(
    master=screen,
    text="GET",
    width=54,
    height=26,
    command=example_func_button,
    bg_color="#1ea9eb",
    fg_color="#1ea9eb",
    corner_radius=2
)
button_click.place(x=84, y=290)

# Start program loop
tk.mainloop()
