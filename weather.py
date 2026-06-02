# Name:  Shakib Khan
# Student Number:  10734436

# This file is provided to you as a starting point for the "weather.py" program of the Project
# of Programming Principles in Semester 1, 2026.  It aims to give you just enough code to help ensure
# that your program is well structured.  Please use this file as the basis of your work.
# You are not required to reference it.

# The "pass" command tells Python to do nothing.  It is simply a placeholder to ensure that the starter file runs smoothly.
# They are not needed in your completed program.  Replace them with your own code as you complete the assignment.

#API Key from openwathermap.org
API_KEY = 'fb7fd1b6da005cfff26888201dfcc63c'

# Import necessary module(s).
import tkinter
import tkinter.messagebox
import json
import urllib.request
import datetime


class ProgramGUI:
    def __init__(self):
        # This is the constructor of the class.
        # It is responsible for loading the data from the text file and creating the user interface.
        
     try:
            file = open('locations.txt', 'r')
            self.data = json.load(file)
            file.close()
        except Exception:
            tkinter.messagebox.showerror('Error', 'Missing/Invalid file')
            return

        if len(self.data) == 0:
            tkinter.messagebox.showerror('Error', 'No locations found.')
            return

        self.window = tkinter.Tk()
        self.window.title('MyWeather')
        self.window.geometry('400x300')
        self.index = 0

        # Top frame with navigation buttons and location name
        top_frame = tkinter.Frame(self.window)
        top_frame.pack(pady=10)

        self.btn_prev = tkinter.Button(top_frame, text='<', font=('Arial', 12), command=self.previous, width=3)
        self.btn_prev.grid(row=0, column=0, padx=5)

        self.lbl_location = tkinter.Label(top_frame, text='', font=('Arial', 16, 'bold'))
        self.lbl_location.grid(row=0, column=1, padx=20)

        self.btn_next = tkinter.Button(top_frame, text='>', font=('Arial', 12), command=self.next, width=3)
        self.btn_next.grid(row=0, column=2, padx=5)

        # Description label
        self.lbl_desc = tkinter.Label(self.window, text='', font=('Arial', 14))
        self.lbl_desc.pack(pady=5)

        # Weather icon
        self.icon_image = tkinter.PhotoImage(file='images/01d.png')
        self.lbl_icon = tkinter.Label(self.window, image=self.icon_image)
        self.lbl_icon.pack(pady=5)

        # Temperature and humidity
        self.lbl_temp = tkinter.Label(self.window, text='', font=('Arial', 11))
        self.lbl_temp.pack(pady=5)

        # Wind info
        self.lbl_wind = tkinter.Label(self.window, text='', font=('Arial', 11))
        self.lbl_wind.pack(pady=5)

        # Sunrise and sunset
        self.lbl_sun = tkinter.Label(self.window, text='', font=('Arial', 11))
        self.lbl_sun.pack(pady=5)

        self.show_weather()
        self.window.mainloop()

    def get_wind_direction(self, degrees):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = round(degrees / 45) % 8
        return directions[index]

    def get_time_string(self, timestamp, timezone):
        local_timestamp = timestamp + timezone
        time_object = datetime.datetime.utcfromtimestamp(local_timestamp)
        return time_object.strftime('%I:%M%p')

    def show_weather(self):
        # This method requests and displays the weather of the current location in the GUI.
        location = self.data[self.index]

        if 'data' not in location:
            url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + str(location['lat']) + '&lon=' + str(location['lon']) + '&units=metric&appid=' + API_KEY
            response = urllib.request.urlopen(url).read()
            location['data'] = json.loads(response)

        weather = location['data']

        location_text = location['name']
        if 'state' in location:
            location_text = location_text + ', ' + location['state']
        location_text = location_text + ', ' + location['country']
        self.lbl_location.configure(text=location['name'])

        desc = weather['weather'][0]['description']
        first_letter = desc[0].upper()
        rest_of_desc = desc[1:]
        self.lbl_desc.configure(text=first_letter + rest_of_desc)

        icon_code = weather['weather'][0]['icon']
        self.icon_image = tkinter.PhotoImage(file='images/' + icon_code + '.png')
        self.lbl_icon.configure(image=self.icon_image)

        temp = weather['main']['temp']
        temp_rounded = round(temp, 1)
        feels = weather['main']['feels_like']
        feels_rounded = round(feels, 1)
        humidity = weather['main']['humidity']
        temp_text = str(temp_rounded) + 'C (feels like ' + str(feels_rounded) + 'C), ' + str(humidity) + '% humidity.'
        self.lbl_temp.configure(text=temp_text)

        wind_speed = weather['wind']['speed'] * 3.6
        wind_speed_rounded = round(wind_speed, 1)
        wind_deg = weather['wind']['deg']
        wind_dir = self.get_wind_direction(wind_deg)

        wind_text = 'Winds ' + wind_dir + ' at ' + str(wind_speed_rounded) + 'km/h'
        if 'gust' in weather['wind']:
            gust_speed = weather['wind']['gust'] * 3.6
            gust_rounded = round(gust_speed, 1)
            wind_text = wind_text + ' (gusts ' + str(gust_rounded) + 'km/h)'
        self.lbl_wind.configure(text=wind_text)

        timezone = weather['timezone']
        sunrise_time = weather['sys']['sunrise']
        sunset_time = weather['sys']['sunset']
        sunrise_str = self.get_time_string(sunrise_time, timezone)
        sunset_str = self.get_time_string(sunset_time, timezone)
        sun_text = 'Sunrise ' + sunrise_str + ', Sunset ' + sunset_str
        self.lbl_sun.configure(text=sun_text)

    def previous(self):
        # This method decreases the index attribute to navigate to the prior location.
        if self.index > 0:
            self.index = self.index - 1
            self.show_weather()

    def next(self):
        # This method decreases the index attribute to navigate to the next location.
        if self.index < len(self.data) - 1:
            self.index = self.index + 1
            self.show_weather()



# An object of the ProgramGUI class to begin the program.
gui = ProgramGUI()
