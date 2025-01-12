import os
import sys 
import math 


import pandas as pd
from datetime import datetime

def get_user_inputs(station_data):
    print("Welcome to the London Tube Fare Calculator Game!")
    print("Please answer a few questions to get the best travel advice.\n")

    # Ask for starting station
    start_station = ""
    while start_station not in station_data['Station Name'].values:
        start_station = input("Enter the starting station: ").strip()
        if start_station not in station_data['Station Name'].values:
            print("Invalid station name. Please try again.\n")

    # Ask for destination station
    destination_station = ""
    while destination_station not in station_data['Station Name'].values:
        destination_station = input("Enter the destination station: ").strip()
        if destination_station not in station_data['Station Name'].values:
            print("Invalid station name. Please try again.\n")

    # Ask for time and day of travel
    while True:
        try:
            travel_time = input("Enter the time of travel (HH:MM, 24-hour format): ").strip()
            travel_day = input("Enter the day of the week (e.g., Monday): ").strip().capitalize()
            travel_datetime = datetime.strptime(travel_time, "%H:%M")

            is_peak = False
            if travel_day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] and (
                (6 <= travel_datetime.hour < 9) or (16 <= travel_datetime.hour < 19)
            ):
                is_peak = True
            break
        except ValueError:
            print("Invalid input. Please enter the time in HH:MM format and a valid day of the week.\n")

    # Ask for number of travelers
    while True:
        try:
            num_travelers = int(input("How many people are traveling? "))
            if num_travelers > 0:
                break
            else:
                print("Please enter a positive number.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")

    # Collect ages and additional details of travelers
    traveler_details = []
    for i in range(num_travelers):
        while True:
            try:
                age = int(input(f"Enter the age of traveler {i + 1}: "))
                if age >= 0:
                    lives_in_london = input("Does this traveler live in London? (yes/no): ").strip().lower()
                    has_railcard = input("Does this traveler have a railcard? (yes/no): ").strip().lower()
                    is_care_leaver = "no"
                    if 18 <= age <= 25:
                        is_care_leaver = input("Is this traveler a care leaver? (yes/no): ").strip().lower()
                    traveler_details.append({
                        "age": age,
                        "lives_in_london": lives_in_london == "yes",
                        "has_railcard": has_railcard == "yes",
                        "is_care_leaver": is_care_leaver == "yes"
                    })
                    break
                else:
                    print("Age cannot be negative.\n")
            except ValueError:
                print("Invalid input. Please enter a valid age.\n")

    # Ask for ticket type
    ticket_type = ""
    while ticket_type not in ["oyster", "contactless", "travelcard", "paper"]:
        ticket_type = input(
            "Do you have an 'oyster' card, 'contactless' payment, a 'travelcard', or need a 'paper' ticket? "
        ).strip().lower()
        if ticket_type not in ["oyster", "contactless", "travelcard", "paper"]:
            print("Please choose a valid ticket type: oyster, contactless, travelcard, or paper.\n")

    # If the user has a travelcard, exit early
    if ticket_type == "travelcard":
        print("\nEnjoy using your Travelcard! In the future, consider using a contactless card for better value.")
        exit()

    # Ask for duration of stay
    while True:
        try:
            duration = int(input("How many days will you be using the Tube? "))
            if duration > 0:
                break
            else:
                print("Please enter a positive number.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")

    # Return collected inputs
    return {
        "start_station": start_station,
        "destination_station": destination_station,
        "time_of_day": "peak" if is_peak else "off-peak",
        "num_travelers": num_travelers,
        "traveler_details": traveler_details,
        "ticket_type": ticket_type,
        "duration": duration,
    }

def calculate_fare(inputs, station_data):
    start_zone = station_data.loc[station_data['Station Name'] == inputs['start_station'], 'Zone'].values[0]
    end_zone = station_data.loc[station_data['Station Name'] == inputs['destination_station'], 'Zone'].values[0]

    
    zones_crossed = abs(start_zone - end_zone) + 1

    
    peak_fares = {1: 8.10, 2: 8.10, 3: 9.60, 4: 11.70, 5: 13.90, 6: 14.90}
    off_peak_fares = {1: 7.50, 2: 7.50, 3: 8.70, 4: 10.60, 5: 12.80, 6: 13.90}

    fares = peak_fares if inputs['time_of_day'] == "peak" else off_peak_fares
    base_fare = fares.get(zones_crossed, max(fares.values()))

    
    total_fare = 0
    for traveler in inputs['traveler_details']:
        age = traveler['age']
        if age < 11:
            total_fare += 0  
        elif 11 <= age <= 15:
            total_fare += base_fare * 0.5  
        elif 16 <= age <= 17:
            total_fare += base_fare * 0.5  
        elif 18 <= age <= 30 and traveler['has_railcard']:
            total_fare += base_fare * 0.66  
        elif 18 <= age <= 25 and traveler['lives_in_london'] and traveler['is_care_leaver']:
            total_fare += base_fare * 0.5  
        elif age >= 60 and traveler['lives_in_london']:
            total_fare += 0  
        else:
            total_fare += base_fare

    
    if inputs['ticket_type'] in ["oyster", "contactless"]:
        daily_cap = 14.90
        total_fare = min(total_fare, daily_cap * inputs['duration'])

    return total_fare

def main():
    # Example station dataset (replace with the cleaned data from your CSV)
    station_data = pd.read_csv("Cleaned_London_Tube_Stations_Data 4")

    inputs = get_user_inputs(station_data)
    total_fare = calculate_fare(inputs, station_data)

    print("\nTravel Summary:")
    print(f"From: {inputs['start_station']}")
    print(f"To: {inputs['destination_station']}")
    print(f"Time of Day: {inputs['time_of_day'].capitalize()}")
    print(f"Number of Travelers: {inputs['num_travelers']}")
    print(f"Ticket Type: {inputs['ticket_type'].capitalize()}")
    print(f"Duration: {inputs['duration']} days")
    print(f"Total Fare: £{total_fare:.2f}")

if __name__ == "__main__":
    main()
