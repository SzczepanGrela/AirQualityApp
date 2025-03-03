import os
import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "air_quality.settings")
django.setup()

import tkinter as tk
import ttkbootstrap as ttk
import sensors.colorFunctions as cf
from sensors.services import (
    DatabaseCitySearch,
    ApiCitySearch,
    FindNearbyStationsByCoordinates,
    FetchMeasurementsByStationId,
    FetchSensorById
)


class MainApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Air Quality App")
        self.geometry("1200x1000")
        self.resizable(True, True)
        self.city_data = {}

        # --- Top Frame (Title) ---
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="🌍 Air Quality Search", font=("Arial", 30, "bold")).pack()

        # --- Search Frame ---
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10, fill="x")
        search_frame.columnconfigure(0, weight=1)
        search_frame.columnconfigure(1, weight=0)

        self.entry_var = tk.StringVar()

        self.entry_city = ttk.Entry(search_frame, textvariable=self.entry_var, font=("Arial", 20), width=40)
        self.entry_city.grid(row=0, column=0, padx=10, sticky="ew")

        self.button_search = ttk.Button(search_frame, text="🔍 Search", command=self.search_city)
        self.button_search.grid(row=0, column=1, padx=10)

        # --- Cities List ---
        self.listbox_results = tk.Listbox(self, font=("Arial", 20), height=5)
        self.listbox_results.pack(pady=5, fill="x", padx=10)
        self.listbox_results.bind("<<ListboxSelect>>", self.city_click)

        # --- Info Label ---
        self.label_info = ttk.Label(self, text="Enter a city and click 'Search'", font=("Arial", 20), foreground="blue")
        self.label_info.pack(pady=10)

        # --- Pollutant Frame ---
        pollutant_title = ttk.Label(self, text="Pollutant Measurements", font=("Arial", 24, "bold"))
        pollutant_title.pack(pady=(10, 0))

        self.pollutant_frame = ttk.Frame(self)
        self.pollutant_frame.pack(pady=10, padx=10, fill="x")

    def city_click(self, event):
        selection = self.listbox_results.curselection()
        if not selection:
            return

        max_distance = 25000  # in meters
        selected_index = selection[0]
        city = self.city_data[selected_index]
        city_long = city['lng']
        city_lat = city['lat']

        stations = FindNearbyStationsByCoordinates.find_nearby_stations_by_coordinates(
            city_lat, city_long, max_distance
        )
        if not stations:
            self.label_info.config(text="⚠ No nearby stations found!", foreground="red")
            return

        closest_station = stations[0]
        measurements = FetchMeasurementsByStationId.fetch_latest_measurements_by_station_id(closest_station['id'])

        # Czyścimy panel z wynikami pomiarów
        for widget in self.pollutant_frame.winfo_children():
            widget.destroy()

        if measurements:
            measurement_dict = {}
            for item in measurements:
                sensor_resp = FetchSensorById.fetch_sensor_by_id(item["sensorsId"])
                sensor = sensor_resp[0]
                param_name = sensor["parameter"]["name"].lower()
                measurement_dict[param_name] = {
                    "value": item["value"],
                    "unit": sensor["parameter"]["units"],
                    "datetime": item["datetime"]["local"]
                }

            known_params = ["pm25", "pm10", "no2", "o3", "co", "so2", "voc"]
            for param in known_params:
                if param in measurement_dict:
                    data = measurement_dict[param]
                    detail_text = f"{param.upper()} ({data['unit']}): {data['value']}  measured at {data['datetime']}"
                    color = cf.color_by_sensor(param, data["value"])
                else:
                    detail_text = f"{param.upper()}: No data"
                    color = "black"
                ttk.Label(
                    self.pollutant_frame,
                    text=detail_text,
                    font=("Arial", 20),
                    foreground=color,
                ).pack(anchor="w", padx=5, pady=2)

            self.label_info.config(text="Measurements updated", foreground="blue")
        else:
            self.label_info.config(text="No measurement data available", foreground="red")

    def search_city(self):
        city_name = self.entry_var.get().strip()
        if not city_name:
            self.label_info.config(text="⚠ Please enter a city name!", foreground="red")
            return

        self.listbox_results.delete(0, tk.END)
        cities = ApiCitySearch.get_location_details(city_name, max_rows=10)

        if cities:
            self.listbox_results.delete(0, tk.END)
            self.city_data.clear()
            for index, city in enumerate(cities):
                display_text = f"{city['name']}, {city.get('adminName3', '')}, {city.get('adminName2', '')}, {city.get('adminName1', '')}, {city['countryName']}"
                self.listbox_results.insert(tk.END, display_text)
                self.city_data[index] = city

            self.label_info.config(text="✅ Select a city from the list below", foreground="green")
        else:
            self.label_info.config(text=f"⚠ No data found for {city_name}", foreground="red")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
