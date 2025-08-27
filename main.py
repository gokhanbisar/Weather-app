import datetime
import requests
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox, Canvas

# ---------------------------
# Weather App (CustomTkinter + Canvas)
# ---------------------------

# ---- Appearance & Theme ----
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ---- Main Window ----
root = ctk.CTk()
root.title("Weather App")
root.geometry("400x400")
root.minsize(400, 400)
root.configure(fg_color="white")

# ---- City Input ----
city_entry = ctk.CTkEntry(root, width=120, placeholder_text="Enter city")
city_entry.place(x=150, y=280)

# ---- OpenWeatherMap API Key ----
API_KEY = "9e8503dddb7ef0a3b9d50c02e8f7fc8e"

# ---- Weather Image Mapping ----
def get_weather_image(weather_id):
    """Return weather icon based on main weather type."""
    if weather_id == 800:
        return "images/clear.png"      # Clear sky
    elif 801 <= weather_id <= 804:
        return "images/clouds.png"     # Clouds
    elif 600 <= weather_id <= 622:
        return "images/snow.png"       # Snow
    elif 500 <= weather_id <= 531:
        return "images/rain.png"       # Rain
    else:
        return "default.png"    # Other / fallback

# ---- Weather Card Canvas ----
card_canvas = Canvas(root, width=230, height=350, bd=0, highlightthickness=0)
card_canvas.place(x=200, y=30)

# Default card image
default_img = Image.open(get_weather_image(800)).resize((230, 350))
card_img_tk = ImageTk.PhotoImage(default_img)
card_canvas.create_image(0, 0, anchor='nw', image=card_img_tk)

# Default text on card
card_canvas.create_text(10, 10, anchor='nw', text="City", fill="white", font=("Arial", 16, "bold"))
card_canvas.create_text(10, 40, anchor='nw', text="Weather", fill="white", font=("Arial", 14, "bold"))
card_canvas.create_text(10, 70, anchor='nw', text="0°C", fill="white", font=("Arial", 22, "bold"))
card_canvas.create_text(10, 300, anchor='nw', text="Min: 0°C  Max: 0°C", fill="white", font=("Arial", 12))

# ---- Fetch Weather Data ----
def show_weather():
    """Fetch weather data for the entered city and update the weather card."""
    global card_img_tk
    city = city_entry.get()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "weather" in data:
            weather_id = data['weather'][0]['id']
            card_img_path = get_weather_image(weather_id)
            img = Image.open(card_img_path).resize((230, 350))
            card_img_tk = ImageTk.PhotoImage(img)

            card_canvas.delete("all")
            card_canvas.create_image(0, 0, anchor='nw', image=card_img_tk)

            temp_c = round(data['main']['temp'] - 273.15)
            min_c = round(data['main']['temp_min'] - 273.15)
            max_c = round(data['main']['temp_max'] - 273.15)
            city_name = data['name']
            weather_desc = data['weather'][0]['description'].capitalize()

            card_canvas.create_text(10, 10, anchor='nw', text=city_name, fill="white", font=("Arial", 16, "bold"))
            card_canvas.create_text(10, 40, anchor='nw', text=weather_desc, fill="white", font=("Arial", 14, "bold"))
            card_canvas.create_text(10, 70, anchor='nw', text=f"{temp_c}°C", fill="white", font=("Arial", 22, "bold"))
            card_canvas.create_text(10, 300, anchor='nw', text=f"Min: {min_c}°C  Max: {max_c}°C", fill="white", font=("Arial", 12))
        else:
            messagebox.showinfo("Warning", "Enter a valid city")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# ---- Show Weather Button ----
button_show = ctk.CTkButton(
    root,
    text="GET",
    width=80,
    height=35,
    corner_radius=15,
    fg_color="#03a9f4",
    hover_color="#0288d1",
    text_color="white",
    command=show_weather,
    font=ctk.CTkFont("Arial", 12, "bold")
)
button_show.place(x=170, y=320)

# ---- Run App ----
root.mainloop()
