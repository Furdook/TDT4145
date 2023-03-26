import sqlite3
import datetime
import re

# Connect to database:
database = sqlite3.connect('TogDB.db')
cursor = database.cursor()


# weekdays to map int to day
weekdays = {1 : 'Mandag', 
            2 : 'Tirsdag', 
            3 : 'Onsdag', 
            4 : 'Torsdag', 
            5 : 'Fredag', 
            6 : 'Lørdag', 
            7 : 'Søndag'
        }


# validate that email is valid using regex: 
def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,10}\b'
    return re.fullmatch(regex, email) != None


# 
def format_available_seats(seats, compartments):
    return f"""
    Sitteplasser: 
        {seats}
    Soveplasser: 
        {compartments}
    """


# check that station exists in database:
def station_exists(station):
    cursor.execute(f"""
        SELECT Stasjonsnavn
        FROM StasjonITabell
        WHERE Stasjonsnavn = '{station}'
    """)
    return cursor.fetchone() != None


# Get all routes stopping on a chosen station on a chosen day:
def get_all_routes(station, day):
    if (day not in weekdays.values() or not station_exists(station)): return 'Invalid input...'

    cursor.execute(f"""
        SELECT TogruteTabell.RuteID
        FROM TogruteKjørerDag
            NATURAL JOIN TogruteTabell
            NATURAL JOIN StasjonITabell
        WHERE TogruteKjørerDag.Dag = '{day}' AND StasjonITabell.Stasjonsnavn = '{station}'
    """)
    
    return cursor.fetchall()


# fetch all routes between a start station and an end station for a chosen date:
def get_all_routes_between(start, end, date):
    year, month, day = map(int, date.split('-'))
    date = int(datetime.date(year, month, day).strftime("%u"))

    if (not station_exists(start) or not station_exists(end)): return 'Invalid input...'

    output = []

    for i in range(2):  # Return for selected day and day after
        cursor.execute(f"""
            SELECT TogRuteTabell.RuteID, Start.Stasjonsnavn, Start.Tid, EndStation.Stasjonsnavn, EndStation.Tid, TogruteKjørerDag.Dag 
            FROM TogRuteTabell
	            NATURAL JOIN StasjonITabell as Start
	            CROSS JOIN StasjonITabell as EndStation
	            NATURAL JOIN TogruteKjørerDag
	
            WHERE Dag = "{weekdays[date + i]}"
	            AND (Start.Stasjonsnavn = "{start}" AND EndStation.Stasjonsnavn = "{end}")
	            AND (Start.TabellID = EndStation.TabellID)
	            AND ((Start.Tid < EndStation.Tid) OR Start.Tid > "23:00") 
            ORDER BY Start.Tid
        """)
        output.append(cursor.fetchall())
    return output


# fetch customer by ID from database:
def get_customer(id): 
    return cursor.execute(f'''SELECT * FROM Kunde WHERE epost = "{id}"''').fetchone()


# register new customer to database:
def register_customer(email, firstname, lastname, phone):

    try:
        cursor.execute(f"""
                INSERT INTO Kunde
                VALUES ("{email}", "{firstname}", "{lastname}", "{phone}")
            """)
        database.commit()
        return 'Kunde registrert! ' + str(get_customer(email))
    except Exception as e:
        return 'Kunde ikke registrert! Feilmelding: ' + str(e)
    

# get all stations between a start station and an en station:
def get_stations_between(start, end, route):

    if (not station_exists(start) or not station_exists(end)): return 'Invalid input...'

    # fetch all station names between start and (including) end station:
    cursor.execute(f"""
        SELECT Stasjonsnavn
        FROM StasjonITabell NATURAL JOIN TogRuteTabell
        WHERE RuteID = {route}
            AND tid > (SELECT tid FROM StasjonITabell WHERE Stasjonsnavn = "{start}")
            AND tid <= (SELECT tid FROM StasjonITabell WHERE Stasjonsnavn = "{end}")
    """)
    return str(cursor.fetchall()).replace("('", '').replace("',)", '').replace('[', '').replace(']', '').split(', ')


# fetch all stations coming after a chosen station on a spesific route:
def get_all_stations_after(station, route):

    if (not station_exists(station)): return 'Invalid input...'

    cursor.execute(f'''
        SELECT Stasjonsnavn
        FROM StasjonITabell
        WHERE TabellID = {route} ''')
    stations = str(cursor.fetchall()).replace("('", '').replace("',)", '').replace('[', '').replace(']', '').split(', ')

    if (route == 3): stations = list(stations)[::-1]
    stations = stations[0:stations.index(station)]
    
    return stations


# fetch all takens seats on a route to a station:
def fetch_seats(station, route):

    if (not station_exists(station)): return 'Invalid input...'

    cursor.execute(f'''
        SELECT SitteplassID
        FROM TogRuteForekomst
	        NATURAL JOIN Vognoppsett
	        NATURAL JOIN SattSammenAv
            NATURAL JOIN Vogn
	        NATURAL JOIN Sitteplass
	        NATURAL JOIN SitteplassPåBillett
	        NATURAL JOIN Billett
        WHERE ForekomstID = {route}
	        AND EndeStasjon = "{station}"
            AND EXISTS (SELECT SitteplassID 
		        FROM SitteplassPåBillett 
		        WHERE SitteplassPåBillett.SitteplassID = Sitteplass.SitteplassID
	    )''')
    
    taken_seats = []

    for seat in cursor.fetchall():
            tmp = str(seat).replace('(', '').replace(',)', '')
            if (tmp != "[]"):
                taken_seats.append(str(tmp))
    return taken_seats


# return all available seatIDs between a start and an end station for a chosen route:
def get_all_available_seats_between_stations(start, end, route):
    taken_seats = []

    if (not station_exists(start) or not station_exists(end)): return 'Invalid input...'

    # get all seats booked for every station up until the end station,
    # or else we would only get seats taken between two said stations:
    
    # add every purchased seat to taken_seats array for comparison: 
    for station in get_stations_between(start, end, route):
        
        for seat in fetch_seats(station, route):
            taken_seats.append(seat)

    for station in get_all_stations_after(end, route):
        for seat in fetch_seats(station, route):
            taken_seats.append(seat)

    # fetch all available seats for a route:
    cursor.execute(f'''
        SELECT SitteplassID
        FROM TogRuteForekomst
	        NATURAL JOIN SattSammenAv
	        NATURAL JOIN Sitteplass
        WHERE ForekomstID = {route}
	        AND ForekomstID = OppsettID
    ''')
    
    # format return to str list to compare with taken seats:
    available_seats = str(cursor.fetchall()).replace('(', '').replace(',)', '').replace('[', '').replace(']', '').split(', ')

    # removes every item in taken_seats from available_seats:
    seats = [i for i in available_seats if i not in taken_seats]

    # fetch all available compartments for a route: (not ready because the table doesn't exist yet)
    cursor.execute(f'''
        SELECT SoveplassID
        FROM TogRuteForekomst
            NATURAL JOIN SattSammenAv
            NATURAL JOIN Soveplass
        WHERE ForekomstID = {route}
            AND ForekomstID = OppsettID
            AND NOT EXISTS (SELECT SoveplassID
                FROM SoveplassPåBillett
                WHERE SoveplassPåBillett.SoveplassID = Soveplass.SoveplassID
            )
    ''')
    
    compartments = str(cursor.fetchall()).replace('(', '').replace(',)', '')
    return seats, compartments


# sql to fetch valid inputs in the database for your ticket:
def set_ticket_input():
    route = input('Route: ')
    while (cursor.execute(f'SELECT * FROM Togrute WHERE RuteId = "{route}"').fetchone() == None):
        route = input('Finner ikke togruten. Prøv igjen: ')
    
    start = input('Start Station: ')
    while (cursor.execute(f'SELECT * FROM StasjonITabell NATURAL JOIN TogRuteTabell WHERE RuteID = {route} AND Stasjonsnavn = "{start}"').fetchone() == None):
        start = input('Finner ikke startstasjonen. Prøv igjen: ')
    
    end = input('End Station: ')
    while (cursor.execute(f'SELECT * FROM StasjonITabell NATURAL JOIN TogRuteTabell WHERE RuteID = {route} AND Stasjonsnavn = "{end}"').fetchone() == None):
        end = input('Finner ikke sluttstasjonen. Prøv igjen: ')
        
    return start, end, route


# purchase ticket:
def buy_ticket():
    # Set input:
    start, end, route = set_ticket_input()

    # Get available seats:
    seats, compartments = get_all_available_seats_between_stations(start, end, route)
    print(format_available_seats(seats, compartments))

    # Login or register customer:
    email = input('Email: ')
    while (not validate_email(email)):
        email = input('Ugyldig email. Prøv igjen: ')

    if (get_customer(email) == '[]'):
        register_customer(email, input('Fornavn: '), input('Etternavn: '), input('Telefon: '))

    # Create new order:
    cursor.execute(f'INSERT INTO Kundeordre (Kjøpsdato, Kunde) VALUES ("{datetime.date.today()}", "{email}")')
    order = cursor.lastrowid

    # Create new ticket:
    while(booking := input('Sitte- eller soveplass? (sitte/sove): ')):
        cursor.execute(f'INSERT INTO Billett (ForekomstID, StartStasjon, EndeStasjon, Kundeordre) VALUES ({route},"{start}","{end}",{order})')
        billett = cursor.lastrowid

        # Book seat:
        if (booking == 'sitte'):
            while (id := input('SitteplassID: ')):
                if (id in seats):
                    cursor.execute('INSERT INTO SitteplassPåBillett (SitteplassID, BillettID) VALUES (?, ?)', (id, billett))
                    print('Billett kjøpt!')
                    break
                else: print('Dette setet er tatt...')
            pass
        
        # Book compartment:
        elif (booking == 'sove'):
            while (id := input('SoveplassID: ')):
                if (id in compartments):
                    cursor.execute('INSERT INTO SoveplassPåBillett (SoveplassID, BillettID) VALUES (?, ?)', (id, billett))
                    print('Billett kjøpt!')
                    break
                else: print('Denne soveplassen er tatt...')
            pass
        else: print('Ugyldig input.')
        
    database.commit()


# For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige reiser.
def get_future_tickets(email):

    if (get_customer(email) == 'None'): return 'Invalid input...'

    cursor.execute(f'''
        SELECT DISTINCT Dato, StartStasjon, EndeStasjon, SitteplassID
        FROM Kundeordre
            NATURAL JOIN Billett
            NATURAL JOIN TogRuteForekomst
            NATURAL JOIN SitteplassPåBillett
        WHERE Kunde = "{email}"
            AND Dato > "{datetime.date.today()}"
    ''')
    tmp = cursor.fetchall()

    cursor.execute(f'''
        SELECT DISTINCT Dato, StartStasjon, EndeStasjon, SoveplassID
        FROM Kundeordre
            NATURAL JOIN Billett
            NATURAL JOIN TogRuteForekomst
            NATURAL JOIN SoveplassPåBillett 
        WHERE Kunde = "{email}"
            AND Dato > "{datetime.date.today()}"
    ''')

    return tmp + cursor.fetchall()

