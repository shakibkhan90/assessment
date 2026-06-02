# Name: Md. Shakib Khan 
# Student Number:  10734436

# This file is provided to you as a starting point for the "admin.py" program of the Project
# of Programming Principles in Semester 1, 2026.  It gives you just enough code to help ensure
# that your program is well structured.  Use this file as the basis of your work.
# You are not required to reference it.

# The "pass" command tells Python to do nothing.  It is simply a placeholder to ensure that the starter file runs smoothly.
# They are not needed in your completed program.  Replace them with your own code as you complete the assignment.


# Import necessary module(s).
import json
import urllib.request

#API Key from openwathermap.org
API_KEY = 'fb7fd1b6da005cfff26888201dfcc63c'


# This function repeatedly prompts for input until something other than whitespace is entered.
# See Point 1 of the "Functions in admin.py" section of the assignment brief.
def input_something(prompt):
    user_input = input(prompt)
    while user_input.strip() == '':
        user_input = input(prompt)
    return user_input

# This function returns a location's name, state (if applicable) and country in a single string.
# See Point 2 of the "Functions in admin.py" section of the assignment brief.
def format_location(location):
    if 'state' in location:
        return location['name'] + ', ' + location['state'] + ', ' + location['country']
    else:
        return location['name'] + ', ' + location['country']


# This function repeatedly prompts for input until a valid item is chosen from a list.
# See Point 3 of the "Functions in admin.py" section of the assignment brief.
def select_option(prompt, options):
    valid_choice = False
    while valid_choice == False:
        try:
            number = int(input(prompt))
            if number >= 1 and number <= len(options):
                return options[number - 1]
        except ValueError:
            pass

# This function opens "locations.txt" in write mode and writes data to it in JSON format.
# See Point 4 of the "Functions in admin.py" section of the assignment brief.
def save_data(data):
    file = open('locations.txt', 'w')
    json.dump(data, file, indent=4)
    file.close()

#load locations.txt
try:
    file = open('locations.txt', 'r')
    data = json.load(file)
    file.close()
except Exception:
    data = []

# Here is where you attempt to open data.txt and read the data into a "data" variable.
# If the file does not exist or does not contain JSON data, set "data" to an empty list instead.
# This is the only time that the program should need to read anything from the file.
# See Point 1 of the "Requirements of admin.py" section of the assignment brief.


# Print welcome message, then enter the endless loop which prompts the user for a choice.
# See Point 2 of the "Requirements of admin.py" section of the assignment brief.
# The rest is up to you.
print('Welcome to the Weather App Admin Program.')

while True:
    print('\nChoose [a]dd, [l]ist, [s]earch, [v]iew, [d]elete or [q]uit.')
    choice = input('> ').lower()


    if choice == 'a':
        # Add a new location.
        
        city_name = input_something('Enter a city/town name: ')

        url = 'http://api.openweathermap.org/geo/1.0/direct?q=' + city_name.replace(' ', '+') + '&limit=4&appid=' + API_KEY
        response = urllib.request.urlopen(url).read()
        results = json.loads(response)

        if len(results) == 0:
            print('No matching locations.')
        else:
            print('Matching location(s) found:')
            for i in range(len(results)):
                location = results[i]
                print(str(i + 1) + ') ' + format_location(location))

            selected = select_option('Which one do you want to add? ', results)

            new_location = {}
            new_location['name'] = selected['name']
            new_location['country'] = selected['country']
            new_location['lat'] = round(selected['lat'], 6)
            new_location['lon'] = round(selected['lon'], 6)

            if 'state' in selected:
                new_location['state'] = selected['state']

            data.append(new_location)
            save_data(data)
            print('Location added.')
        
    elif choice == 'l':
        # List the current locations.
       
        if len(data) == 0:
            print('No locations saved.')
        else:
            print('List of locations:')
            for i in range(len(data)):
                print(str(i + 1) + ') ' + format_location(data[i]))

    elif choice == 's':
        # Search the current locations.
        
        if len(data) == 0:
            print('No locations saved.')
        else:
            search_term = input_something('Enter search term: ')
            print('Search results:')
            found = False
            for i in range(len(data)):
                location_string = format_location(data[i])
                if search_term.lower() in location_string.lower():
                    print(str(i + 1) + ') ' + location_string)
                    found = True
            if found == False:
                print('No results found.')

    elif choice == 'v':
        # View a location.
        
        if len(data) == 0:
            print('No locations saved.')
        else:
            location = select_option('Location number to view: ', data)
            print(format_location(location))
            print('Coordinates: ' + str(location['lat']) + ', ' + str(location['lon']))

    elif choice == 'd':
        # Delete a location.
        
        if len(data) == 0:
            print('No locations saved.')
        else:
            location = select_option('Location number to delete: ', data)
            data.remove(location)
            save_data(data)
            print('Location deleted.')

    elif choice == 'q':
        # Quit the program.
       
        print('Goodbye!  Thank you')
        break

    else:
        # Print "invalid choice" message.
        print('Invalid choice.')
