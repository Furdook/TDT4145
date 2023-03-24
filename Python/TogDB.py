from Tests import *
from Queries import get_all_routes, get_all_routes_between, register_customer, get_future_tickets

# SQLite3 Dokumentasjon:
# https://docs.python.org/3/library/sqlite3.html


# an empty input will quit the while loop
while(action := input('''
    Actions:
 
    F - Get all routes stopping at a chosen station on said day.   
    B - Get all routes running between two chosen stations on a chosen day.
    R - Register a new customer.
    A - Buy tickets for a route between two stations.
    O - Get all future orders for a customer.
    T - Run unit tests.

    Press 'Enter' to quit...
    

    Select action: ''').lower()):
    
    if (action == "f"):
        print('\n' + str(get_all_routes(input('Station: '), 
                                        input('Day: '))).replace('(', '').replace(',)', ''))
   
    elif (action == "b"):
        raw = get_all_routes_between(input('Start Station: '), 
                                     input('End Station: '), 
                                     input('Enter a date in YYYY-MM-DD format: '))
        
        # return formatting:
        tmp = ""#"| ID\t| StartStasjon\t| Avg.\t| SluttStasjon\t| Ank.\t| Dag\t\t|\n"
        for day in raw:
            for row in day:
                tmp += "| "
                for i in row:
                    tmp += str(i) + "\t| "
                tmp += "\n"
        print(f'\n{tmp}') 
    
    elif (action == "r"):
        register_customer(input('Email: '), 
                          input('First name: '), 
                          input('Last name: '), 
                          input('Phone: '))
        
    elif (action == "a"):
        buy_ticket()
    
    elif (action == "o"):
        print(get_future_tickets(input('Email: ')))

    elif (action == "t"):
        test()


database.close()
