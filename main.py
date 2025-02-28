import tkinter as tk
import ttkbootstrap as ttk



class MainApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Air Quality App")
        self.geometry("600x450")

        # Text entry for city name
        self.entry_city = ttk.Entry(self, font=("Arial", 12))
        self.entry_city.pack(pady=10)

        # Search button
        self.button_search = ttk.Button(self, text="Search", command=self.search_city)
        self.button_search.pack(pady=5)

        # Label to display results
        self.label_info = ttk.Label(self, text="Enter a city and click 'Search'", font=("Arial", 14))
        self.label_info.pack(pady=20)

    def search_city(self):
        city = self.entry_city.get()
        if city:
            self.label_info.config(text=f"Searching data for: {city}")
        else:
            self.label_info.config(text="Please enter a city name!")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
