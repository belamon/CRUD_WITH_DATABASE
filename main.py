import re
from datetime import datetime
import csv
import pandas as pd
import openpyxl
from conn import execute,insert_data,update_data, delete_lead
from collections import defaultdict

#varibale months
months_map = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12,
}

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

#Create menu option 
def create_data_lead():
    """Function to display the result when the user choosing number 2 on main menu """
    while True:
        # Displaying the main menu for creatin a new lead or going back 
        print("\t\t=========CREATE NEW LEAD===============")
        print("1. Create New Lead")
        print("2. Back to Menu")

        try:  # This is a block to handle any invalid input like non-integer values 
            user_input = int(input("Please enter 1 to create a lead or 2 to go back:"))

            if user_input == 1:
                print("===========Input Lead Details===========")

                while True:
                    # Asking user for an email and validate the format
                    while True:
                        lead_email = input("Enter Lead's Email: ") 
                        if validate_email(lead_email):
                            break
                        else:
                            print("Invalid Email Format. Please try again.")

                    # Checking if the email already exists 
                    lead_exists = execute(f"select * from data_lead where email = '{lead_email}'")  # this code is for checking if the email already exists in the list

                    if len(lead_exists) > 0:
                        # If the email already exists, inform the user and display the email
                        print("\t\t=====LEAD DATA CHECK========")
                        print("This email already exists in the database")
                        break
                    # Collect lead details from the user 
                    first_name = input("Enter First Name of the Lead: ")
                    last_name = input("Enter Last Name of the Lead: ")

                    # Prompt for phone number and validate it 
                    while True:
                        phone_number = input("Enter Phone Number: ")
                        if validate_phone_number(phone_number):
                            break
                    #Prompt company sector and validate it 
                    
                    while True:
                        company_sector = input("Enter Company Sector of the Lead: ")
                        if validate_sector(company_sector):
                            break
                    #Prompt lead source and validate it 
                    while True:
                        lead_source = input("Enter Lead Source of the Lead: ")
                        if validate_source(lead_source):
                            break
                    #Validate the date input    
                    while True:
                        date_created = input("Enter Date Created of the Lead: ")
                        if validate_date(date_created):
                            break
                    #Validate sales representation 
                    while True:
                        sales_rep = input("Enter Sales Representative:")
                        if validate_sales(sales_rep):
                            break

                    while True:
                        try:
                            transaction = int(input("Enter the new Transaction: "))
                            print(f"Transaction updated to: {transaction}")
                            break  # Exit the loop if a valid integer is provided
                        except ValueError:
                            print("Please input a valid number.")  # Inform the user to input a number
                            break

                    status = input("Enter Status of Leads ")

                    # Store the lead details in a dictionary 
                    new_lead = {
                        "first_name": first_name, 
                        "last_name": last_name,
                        "email": lead_email,
                        "phone_number": phone_number,
                        "company_sector": company_sector,
                        "lead_source": lead_source,
                        "date_created": date_created,
                        "sales_rep":sales_rep,
                        "transaction":transaction,
                        "status": status,
                    }

                    # Display a confirmation page
                    print("\n=== Confirmation Page ===")
                    print(f"First Name: {first_name}")
                    print(f"Last Name: {last_name}")
                    print(f"Email: {lead_email}")
                    print(f"Phone Number: {phone_number}")
                    print(f"Company Sector: {company_sector}")
                    print(f"Lead Source: {lead_source}")
                    print(f"Date Created: {date_created}")
                    print(f"Sales Representation: {sales_rep}")
                    print(f"Transaction: {transaction}")
                    print(f"Status: {status}")
                        

                    #Ask for confirmation until a valid input is received 
                    confirm = confirmation_page(action="Save", data=new_lead)
                    if confirm == "1":
                        insert_query = f"insert into data_lead (first_name, last_name, email, phone_number, company_sector, lead_source, date_created, sales_rep, transaction, status) values('{new_lead['first_name']}', '{new_lead['last_name']}', '{new_lead['email']}', '{new_lead['phone_number']}', '{new_lead['company_sector']}', '{new_lead['lead_source']}', '{new_lead['date_created']}', '{new_lead['sales_rep']}', '{new_lead['transaction']}', '{new_lead['status']}')"
                        insert_data(insert_query)
                        print("\nLead Added Successfully!")
                        # execute(f"insert into data_lead values('{new_lead['first_name']}', '{new_lead['last_name']}', '{new_lead['lead_email']}', '{new_lead['phone_number']}', '{new_lead['company_sector']}', '{new_lead['lead_source']}', '{new_lead['date_created']}', '{new_lead['sales_rep']}', '{new_lead['transaction']}', '{new_lead['status']}')")
                        break
                    elif confirm == "2":
                        print("\nLead not added.")
                        break
                    else:
                        print("Invalid input. Please choose between 1 or 2.")


            elif user_input == 2:
                # If user selects 2, then they will return to the main menu 
                print("Returning to the main menu ")
                break  # Exit the loop and back to the main menu 

            else:
                # If user enters a number other than 1 or 2, show an error message 
                print("Invalid Input. Please enter 1 or 2")


        except ValueError: #jika tidak ada value error, ini handling semua error
            print("Invalid Input. Please enter the number between (1-2)")


#Update Data Leads Function 
def update_data_lead():
    """Function to display the result when the user inputs number 3 on the main menu."""
    
    while True:  # Outer loop for updating data leads
        print("\t\t============UPDATE DATA LEADS====================")
        print("1. Update Data Leads")
        print("2. Back to Menu")

        try:
            operation = False
            user_input = int(input("Please Choose an Option (1-2): "))

            if user_input == 1:
                print("===============Input Update Data of The Leads=====================")

                while not operation:  # Inner loop for updating leads
                    lead_email = input("Enter the email of the Lead you want to update: ")
                    lead_found = False

                    all_leads = execute(f"select * from data_lead where email = '{lead_email}'")
                    for lead in all_leads:
                        if lead[3] == lead_email:
                            lead_found = True 

                            details_of_leads([lead])  # Display lead details

                            user_confirmation = confirmation_page(action="update", data=lead)  # Re-confirmation

                            if user_confirmation == "1":  # Confirm update
                                # Store original values for confirmation
                                original_lead = list(lead)  # Change this to create a list from the tuple
                                update_made = False  # Flag to track if an update has been made

                                print("Choose column that you want to be updated")
                                print("1. First Name ")
                                print("2. Last Name")
                                print("3. Email")
                                print("4. Phone Number")
                                print("5. Company Sector")
                                print("6. Lead Source")
                                print("7. Date Created")
                                print("8. Status")  # Add this to the options list

                                while True:
                                    try:  # This is a block to get the column that user wants to update
                                        column_choice = int(input("Please Choose an Option (1-8): "))
                                        if column_choice == 1:
                                            first_name = input("Enter the new First Name: ")
                                            original_lead[1] = first_name  # Update the original_lead list
                                            print(f"First Name updated to: {first_name}")
                                            update_made = True  # Update occurred
                                            break 
                                        elif column_choice == 2:
                                            last_name = input("Enter the new Last Name: ")
                                            original_lead[2] = last_name  # Update the original_lead list
                                            print(f"Last Name updated to: {last_name}")
                                            update_made = True  # Update occurred
                                            break
                                        elif column_choice == 3:
                                            email = input("Enter the new Email: ")
                                            if validate_email(email):
                                                original_lead[3] = email  # Update the original_lead list
                                                print(f"Email updated to: {email}")
                                                update_made = True  # Update occurred
                                                break
                                            else:
                                                print("Invalid email format. Please try again.")
                                        elif column_choice == 4:
                                            phone_number = input("Enter the new Phone Number: ")
                                            if validate_phone_number(phone_number):
                                                original_lead[4] = phone_number  # Update the original_lead list
                                                print(f"Phone Number updated to: {phone_number}")
                                                update_made = True  # Update occurred
                                                break
                                            else:
                                                print("Invalid phone number. Please enter digits only (10-15 characters).")
                                        elif column_choice == 5:
                                            company_sector = input("Enter the new Company Sector: ")
                                            if validate_sector(company_sector):
                                                original_lead[5] = company_sector  # Update the original_lead list
                                                print(f"Company Sector updated to: {company_sector}")
                                                update_made = True  # Update occurred
                                                break
                                            else:
                                                print(f"Invalid sector. Please choose from the following options: {', '.join(valid_sectors)}")  
                                        elif column_choice == 6:
                                            lead_source = input("Enter the new Lead Source: ")
                                            if validate_source(lead_source):
                                                original_lead[6] = lead_source  # Update the original_lead list
                                                print(f"Lead Source updated to: {lead_source}")
                                                update_made = True  # Update occurred
                                                break
                                            else:
                                                print(f"Invalid source. Please choose from the following options: {', '.join(valid_lead_sources)}")
                                        elif column_choice == 7:
                                            date_created = input("Enter the new Date Created (YYYY-MM-DD): ")
                                            if validate_date(date_created):
                                                original_lead[7] = date_created  # Update the original_lead list
                                                print(f"Date Created updated to: {date_created}")
                                                update_made = True  # Update occurred
                                                break
                                            else:
                                                print("Invalid date format. Please use YYYY-MM-DD.")
                                        elif column_choice == 8:
                                            status = input("Enter the new Status: ")  # Corrected label for status
                                            original_lead[8] = status  # Update the original_lead list
                                            print(f"Status updated to: {status}")
                                            update_made = True  # Update occurred
                                            break
                                        else:
                                            print("Invalid Option. Please choose a valid option (1-8).")
                        
                                    except ValueError:
                                        print("Invalid Input. Please enter a valid number.")
                                        continue

                                # Ask for confirmation to save changes only if an update was made
                                if update_made:
                                    while True:  # Add a loop to keep asking for confirmation
                                        save_confirmation = confirmation_page(action="save", data=original_lead)  # Pass the updated lead for confirmation
                                        if save_confirmation == "1":  # User confirms save
                                            update_query = f"""
                                                UPDATE data_lead 
                                                SET 
                                                    first_name = '{original_lead[1]}', 
                                                    last_name = '{original_lead[2]}', 
                                                    email = '{original_lead[3]}', 
                                                    phone_number = '{original_lead[4]}', 
                                                    company_sector = '{original_lead[5]}', 
                                                    lead_source = '{original_lead[6]}', 
                                                    date_created = '{original_lead[7]}', 
                                                    status = '{original_lead[8]}'
                                                WHERE email = '{lead_email}'
                                            """
                                            update_data(update_query)
                                            print("Changes saved successfully.")
                                            operation = True
                                            break  # Break out of the save confirmation loop
                                        elif save_confirmation == "2":  # User cancels save
                                            # No need to revert since we already have original_lead values
                                            print("Changes reverted.")
                                            operation = True 
                                            break  # Break out of the save confirmation loop
                                        else:
                                            print("Invalid Option. Please choose a valid option.")
                                    
                            elif user_confirmation == "2":
                                print("Data update canceled.")
                                break  # Exit the inner loop and go back to the outer loop

                    if not lead_found:
                        print("The data you are looking for does not exist.")

                    # Check if we broke out of the inner loop due to cancellation
                    if not lead_found or user_confirmation == "2":
                        break  # Break the inner loop to go back to the outer menu

            elif user_input == 2:
                return  # Go back to the main menu
            else:
                print("Invalid choice. Please choose 1 or 2.")

        except ValueError:
            print("Invalid input. Please enter a number.")

#Delete data function

def delete_data():
    """Function to delete leads based on user input."""
    
    while True:
        print("====DELETE DATA LEAD=====")

        # Show options to the user
        print("\nOptions:")
        print("1. Delete lead by email")
        print("2. Back to Main Menu")

        user_input = input("Enter Choice: ")

        if user_input == "1":  # Delete lead by email
            # Show list of current leads before proceeding
            all_leads = execute("SELECT * FROM data_lead")
            active_leads = all_leads  # Fetch active leads from the database
            show_list_of_leads(active_leads)  # Display active leads

            # Ask user to input email
            email = input("Enter email of the lead to delete: ")

            # Find the lead with the matching email
            lead_found = None
            for lead in active_leads:
                if lead[3] == email:  
                    lead_found = lead  # Store the lead to delete
                    break

            if lead_found:  # If a matching lead was found
                # Confirm deletion
                user_confirmation = confirmation_page(action="delete", data=lead_found)
                if user_confirmation == "1":  # Confirm deletion
                    delete_lead(email)  # Call delete_lead with the email
                    print(f"\nLead with email {email} has been successfully deleted.")
                elif user_confirmation == "2":  # Cancel deletion
                    print("\nLead not deleted.")
            else:
                print("No lead found with the provided email.")

        elif user_input == "2":  # Back to Main Menu
            return  # Exit back to the main menu

        else:
            print("Invalid choice. Please enter 1 or 2.")

#Transaction function 
def transaction():
    print("====TRANSACTION====")
    
    month = input("Enter the month to filter leads: ")

    # Assuming you have a function or a method to retrieve your lead data
    data_lead = execute("SELECT * FROM data_lead")  # Adjust as necessary to fit your context

    # Call the filtering function with both the month and the data_lead
    filter_leads_by_month(month, data_lead)

#report data function 
def report_menu():
    data_leads = execute("select * from data_lead")
    while True:
        print("\n==== Reporting Menu ====")
        print("1. Generate Summary Report")
        print("2. Back to Main Menu")
    

        choice = input("Enter your choice: ")

        if choice == "1":
            report = generate_summary_report(data_leads)
            print("============Summary Report:===========")
            for sector, count in report.items():
                print(f"{sector}: {count}")
            input("Press enter  to continue...")
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


def validate_email(email):
    """
    Function to validate if an email is in the correct format.

    Returns True if valid, False otherwise
    """
    # Regular expression for validating an email address
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    #user re.match() to check if the email matches the regex pattern 
    if re.match(email_regex, email):
        return True
    else:
        return False

def validate_phone_number(phone_number):
    #this is regex pattern to allow numbers, spaces, +, _, and parentheses
    pattern = r'^\+?[0-9\s\-()]{7,15}$'

    #validate phone number
    if re.match(pattern, phone_number):
        return True
    else:
        print("Invalid phone number. Please enter a 10-digit number, e.g., 123-456-7890.")
        return False

def validate_sector(company_sector):
    valid_sectors = execute("Select * from company_sector ")
    if company_sector.lower() in [sector[1].lower() for sector in valid_sectors]:
        return True
    else:
        print("Company sector is not listed")
        print("Here are the available company sectors you can search:")
        print("Finance")
        print("Technology")
        print("Real Estate")
        return False
    
def validate_source(lead_source):
    valid_lead_sources = execute("Select * from lead_source")
    if lead_source.lower() in [source[1].lower() for source in valid_lead_sources]:
        return True
    else:
        print("Lead source is not listed")
        return False

def validate_date(date_created):
    """This is a function to validate if an input date is in the correct format

    Returns True if valid, False otherwise
    """
    try:
        #try to parse the input date using the format 'yyyy/mm/dd'
        datetime.strptime(date_created, "%Y/%m/%d")
        return True
    except ValueError:
        print("Invalid date. Please enter a date in the format 'yyyy/mm/dd'.")
        return False

def validate_sales(sales_rep):
    valid_sales_reps = execute("Select * from sales_reps")
    if sales_rep.lower() in [rep[1].lower() for rep in valid_sales_reps]:
        return True
    else:
        print("Sales representation is not listed")
        return False
from datetime import datetime

def confirmation_page(action, data):
    """Mock function for user confirmation."""
    print(f"Are you sure you want to {action} this lead?")  # Show details of the lead
    return input("Enter 1 to confirm, 2 to cancel: ")

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

def filter_leads_by_month(month, data_lead):
    """Function to filter and sum transactions for a given month."""
    
    # Normalize the input to lowercase to make it case-insensitive
    month = month.lower()
    
    if month in months_map:
        month_number = months_map[month]
        total_transaction_value = 0
        filtered_leads = []

        # Loop through the leads data and filter by the given month
        for lead in data_lead:
            lead_date = lead[7]  # Assuming index 7 contains the date
            
            # Convert lead_date to datetime.date if it's a string
            if isinstance(lead_date, str):
                lead_date = datetime.strptime(lead_date, '%Y-%m-%d').date()
            
            lead_month = lead_date.month  # Get the month from the date object
            
            # Debug output
            print(f"Lead Date: {lead_date}, Month: {lead_month}, Month Number: {month_number}")

            if lead_month == month_number:
                filtered_leads.append(lead)
                total_transaction_value += float(lead[9])  # Assuming index 9 contains the 'Transaction' value

        # Check if any leads were found
        if filtered_leads:
            print(f"Total transaction value in {month.capitalize()}: {total_transaction_value}")
        else:
            print(f"No leads found for {month.capitalize()}.")
    else:
        print("Invalid month name. Please enter a valid month.")

def generate_summary_report(data_leads):
    """Generate a summary report of leads by company sector."""
    report = defaultdict(int)  # Use defaultdict to avoid key errors

    all_leads = execute(f"select * from data_lead")
    for lead in all_leads:
        sector = lead[5]
        report[sector] += 1  # Increment the count for each sector

    return report


def login():
        
    while True:

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        is_username_exists= execute(f"select * from valid_user where username = '{username}' and password = '{password}'")

        if len(is_username_exists) > 0 :
            print("Login Successful")
            return True
        else:
            print("Login unsuccessful. Please try again ")
            return False
        
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
        