from Queries import *

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

    Press 'Enter' to quit...
    

    Select action: ''').lower()):
    
    if (action == "f"): # validate day!!! TODO TODO TODO
        query = str(get_all_routes(station := input('Station: '), day := input('Day: ')))
        
        for i in ['(', ')', '[', ']', ' ,']:
            query = query.replace(i, ' ')

        # check if station and day is valid and exists in database:
        if (query == 'Invalid input...'):
            print(f'\n{query}')
            continue

        print(f'\n\tRute: {query} kjører gjennom {station} på {day}')
    
    
    elif (action == "b"):
        raw = get_all_routes_between(start := input('Start Station: '), 
                                     end   := input('End Station: '), 
                                     date  := input('Enter a date in YYYY-MM-DD format: '))
        
        if (raw == 'Invalid input...'):
            print(f'\n{raw}')
            continue

        # return formatting:
        tmp = ""
        for day in raw:
            for row in day:
                tmp += "| "
                for i in row:
                    tmp += str(i) + "\t| "
                tmp += "\n"

        print(f'\nRutetabell fra {date} mellom {start} og {end}:\n{tmp}') 
    
    elif (action == "r"):
        print(register_customer(input('Email: ').lower(), 
                                input('First name: '), 
                                input('Last name: '), 
                                input('Phone: ')))
        
    elif (action == "a"):
        print('\nIf you wish to see all routes between two stations, please use the "B" action.\n')
        buy_ticket()
    
    elif (action == "o"):
        query = input('Email: ')

        print(f'\nFuture tickets for {query}:\n')
        print(get_future_tickets(query))
        for i in get_future_tickets(query):
            print(f'Dato: {i[0]}\tFra: {i[1]}\tTil: {i[2]}\tSitte/Soveplassnummer: {i[3]}')


database.close()
