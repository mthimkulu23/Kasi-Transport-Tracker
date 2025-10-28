from db_setup import create_database, create_tables
from db_setup import add_driver, add_route, record_trip
from datetime import date
import csv
from db_setup import reports
from db_setup import get_money


def register_driver():
    conn = create_database()
    cursor = conn.cursor()
    
    name = input("Enter your name: ")
    taxi_number = input("Enter your taxi number: ")
    
    try:
        add_driver(cursor, name, taxi_number)
        conn.commit()
        print(f" Driver '{name}' with taxi number '{taxi_number}' registered successfully.")
    except Exception as e:
        print(f"Error registering driver: {e}")
    finally:
        cursor.close()
        conn.close()
        

def add_direction():
    conn = create_database()
    cursor = conn.cursor()
    
    origin = input("Enter route Origin: ")
    destination = input("Enter route Destination: ")
    
    while True:
        fare_input = input("Enter the fare amount: ")
        try:
            fare = float(fare_input)
            break
        except ValueError:
            print("Invalid input. Please enter a numeric fare value, e.g., 25.00")
    
    try:
        add_route(cursor, origin, destination, fare)
        conn.commit()
        print(f"Route from {origin} to {destination} with fare {fare} added successfully.")
    except Exception as e:
        print(f"Error adding route: {e}")
    finally:
        cursor.close()
        conn.close()


def log_trip():
    conn = create_database()
    cursor = conn.cursor()
    
    driver_id = int(input("Enter driver ID: "))
    route_id = int(input("Enter the Route ID: "))
    passengers = int(input("Enter the Number of Passengers: "))    
    
    try:
        trip = record_trip(cursor, driver_id, route_id, passengers)
        conn.commit()
        print(f"Trip recorded: Driver {driver_id}, Route {route_id}, Passengers {passengers}, Total {trip['total_amount']}")
    except Exception as e:
        print(f"Error adding the trip: {e}")
    finally:
        cursor.close()
        conn.close()



def daily_report():
    conn = create_database()
    cursor = conn.cursor()
    today = date.today()

    try:
      
        results = reports(cursor, today)

        print(f"\n Daily Report for {today}")
        print("-" * 70)
        print(f"{'Driver Name':<15}{'Taxi No.':<12}{'Route':<25}{'Trips':<7}{'Total (R)':>10}")
        print("-" * 70)

        for r in results:
            driver_name = r[1]
            taxi_number = r[2]
            origin = r[3]
            destination = r[4]
            total_earned = r[5]
            trips_made = r[6]
            print(f"{driver_name:<15}{taxi_number:<12}{origin}→{destination:<15}{trips_made:<7}{total_earned:>10.2f}")

        # Export to CSV
        with open(f'daily_report_{today}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Driver Name', 'Taxi Number', 'Route', 'Trips Made', 'Total Earned (R)'])
            for r in results:
                writer.writerow([r[1], r[2], f"{r[3]}→{r[4]}", r[6], r[5]])

        print(f"\n Report exported as daily_report_{today}.csv")

    except Exception as e:
        print("❌ Error generating report:", e)

    finally:
        cursor.close()
        conn.close()


        

def search_drivers():
    conn = create_database()
    cursor = conn.cursor()
    search_term = input("Enter driver name to search: ").strip()
    try:
        cursor.execute("SELECT id, name, taxi_number FROM drivers WHERE name ILIKE %s", (f"%{search_term}%",))
        results = cursor.fetchall()
        if results:
            for driver in results:
                print(f"ID: {driver[0]}, Name: {driver[1]}, Taxi: {driver[2]}")
        else:
            print("No drivers found.")
    finally:
        cursor.close()
        conn.close()

def search_routes():
    conn = create_database()
    cursor = conn.cursor()
    search_term = input("Enter origin or destination to search: ").strip()
    try:
        cursor.execute("SELECT id, origin, destination, fare FROM routes WHERE origin ILIKE %s OR destination ILIKE %s",
                       (f"%{search_term}%", f"%{search_term}%"))
        results = cursor.fetchall()
        if results:
            for route in results:
                print(f"ID: {route[0]}, {route[1]} -> {route[2]}, Fare: R{route[3]:.2f}")
        else:
            print("No routes found.")
    finally:
        cursor.close()
        conn.close()


def top_earning_driver():
    conn = create_database()
    cursor = conn.cursor()
    today = date.today()
    
    try:
        all_drivers = reports(cursor, today)
        
        if not all_drivers:
            print("No trips recorded today.")
            return
        
   
        top_driver = all_drivers[0]
        driver_name = top_driver[1]  
        driver_id = top_driver[0]    
        total_earned = top_driver[5] 
        
        print(f"Top-earning driver today: {driver_name} (ID {driver_id}) with R{total_earned:.2f}")
        
    finally:
        cursor.close()
        conn.close()





def main():
    print("🇿🇦 Sawubona! Welcome to Kasi Transport Tracker!")
    create_tables()
    
    while True:
        print("\033[1;34m========== MAIN MENU ==========\033[0m")  
        print("1. Add Driver 🚐")
        print("2. Add Route 🛣️")
        print("3. Record Trip 📝")
        print("4. Daily Report 📊")
        print("5. Search Drivers 🔍")
        print("6. Search Routes 🗺️")
        print("7. Top Earning Driver 🏆")
        print("8. Exit ❌")
        print("\033[1;34m================================\033[0m")


        choice = input("\n ENTER YOUR CHOICE: ").strip()

        if choice == "1":
            register_driver()
        elif choice == "2":
            add_direction()
        elif choice == "3":
            log_trip()
        elif choice == "4":
            daily_report()
        elif choice == "5":
            search_drivers()
        elif choice == "6":
            search_routes()
        elif choice == "7":
            top_earning_driver()
        elif choice == "8":
            print("Exiting... Hamba kahle!")
            break
        else:
            print("Invalid choice. Please try again.")
   

if __name__ == "__main__":
    main()
