import re
from datetime import datetime
import csv
import pandas as pd
import openpyxl
from conn import execute
from collections import defaultdict


def main_menu_choice():
    """Function to display the main menu and get user input"""
    while True: #This will keep asking usert for input until a valid menu option is seleted
        print("\n\t================LEAD MANAGEMENT SYSTEM================")
        print("1. Show Leads")
        print("2. Create Leads")
        print("3. Update Leads")
        print("4. Delete Leads")
        print("5. Check Transaction")
        print("6. Export Report")
        print("7. Exit")

        
        try:
            menu = int(input("Input program menu from (1-7): ")) #menu is the variable to hold menu value 
            if 1 <= menu <= 7:  # check if input is valid between this range
                return menu #return the selected menu option 
            else:
                print("*************** Invalid choice. Please select a number between 1 and 7. ***************")
        except ValueError:
            print("*********** Invalid input. Please enter a valid number between 1 and 7. ************")

#Read Menu Functon 
def show_data_leads():
    """Function to display the result when the user chooses number 1 on main menu """
    while True:
        print("\n===== Data Leads =====")
        print("1. Show All Data Records")
        print("2. Search Data Records")
        print("3. Back to Main Menu")

        try:
            all_leads = execute("select * from data_lead")
            user_input = int(input("Enter your choice (1-3): "))  # Get user input and convert to an integer
            # if user chooses 1 : Show all data records
            if user_input == 1:
                if len(all_leads) != 0:  # If the list has at least one lead
                    show_list_of_leads(data=all_leads) #Call function to display all leads
                else:
                    print("No data available.") #Inform the user if no data exists
            # if user chooses 2: Search for specific record
            elif user_input == 2:
                search_input = input("Enter the company sector you are looking for: ") #Get the sector to search for 
                data_found = False  # Flag to track if the search finds any results

                for data in all_leads: #Loop through the leads to find maches
                    if search_input.strip().lower() in data[5].strip().lower():  # Case-insensitive search
                        data_found = True
                        details_of_leads([data])  # Display the leads details 
                        break  # Exit the loop once a matching lead is found 
                if not data_found: #If no matching leads were found
                    print("\n********* Company Sector Not Found *************")
                    print("Here are the available company sectors you can search:")
                    print("Finance")
                    print("Technology")
                    print("Real Estate")
            # if user chooses 3: Go back to the main menu 
            elif user_input == 3:
                return  # Return to exit this function and go back to the main menu
            #Invalid choice handling 
            else:
                print("Invalid choice. Please select 1, 2, or 3.") #Inform the user to enter a valid option 
        except ValueError:
            print("Invalid input. Please enter a number.") #inform the user that the input should be a number

def show_list_of_leads(comment="\n============Available Data Leads==============", data=[]):
    """Function to display the list of leads after pressing 1 on show_data_leads function"""
    if len(data) > 0:  # check if there are any leads
        print(comment)
        for lead in data:
            print(f"First Name = {lead[1]}")
            print(f"Last Name = {lead[2]}")
            print(f"Email = {lead[3]}")
            print(f"Phone Number = {lead[4]}")
            print(f"Company Sector = {lead[5]}")
            print(f"Lead Source = {lead[6]}")
            print(f"Date Created = {lead[7]}")
            print(f"Sales Representation = {lead[8]}")
            print(f"Transaction = {lead[9]}")  
            print(f"Status = {lead[10]}")
            print("-------------------------------------")
    else:
        print("No leads available.")
def details_of_leads(data_lead): #dont forget put the parameneter here to call the data  from the list
    """Function to display details of leads when being called after pressing 2 on show_data_leads_function """
    for detail in data_lead:
        print("\n============Available Data Leads==============")
        print(f"First Name = {detail[1]}")
        print(f"Last Name = {detail[2]}")
        print(f"Email = {detail[3]}")
        print(f"Phone Number = {detail[4]}")
        print(f"Company Sector = {detail[5]}")
        print(f"Lead Source = {detail[6]}")
        print(f"Date Created = {detail[7]}")
        print(f"Sales Representation = {detail[8]}")
        print(f"Transaction = {detail[9]}")
        print(f"Status = {detail[10]}")



# Main program loop
while True:
    # Ensure login before allowing access to the menu
    if login():  # Only proceed if the login is successful
        while True:
            menu_choice = main_menu_choice()
            if menu_choice == 1:
                show_data_leads()
            elif menu_choice == 2:
                create_data_lead()  # Ensure this function is defined
            elif menu_choice == 3:
                update_data_lead()  # Ensure this function is defined
            elif menu_choice == 4:
                delete_data()  # Ensure this function is defined
            elif menu_choice == 5:
                transaction()
            elif menu_choice == 6:
                report_menu()
            elif menu_choice == 7:
                print("Exiting program, Goodbye!")
                exit()  # Break the outer loop and exit the program
            else:
                print("Invalid choice. Please select a valid option.")


        
    else:
        # Failed login, retry
        print("Login failed. Please try again.")
        