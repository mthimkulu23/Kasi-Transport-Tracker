from db_setup import create_database, create_tables
from db_setup import add_driver, add_route, record_trip
from datetime import date


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
        query = """
            SELECT driver_id, SUM(total_amount) AS total_amount
            FROM trips
            WHERE DATE(trip_date) = %s
            GROUP BY driver_id
            ORDER BY total_amount DESC;
        """
        cursor.execute(query, (today,))
        results = cursor.fetchall()

        print(f"Daily Report for {today}")
        print("-" * 35)
        for driver_id, total in results:
            print(f"Driver {driver_id}: R{total:.2f}")

    except Exception as e:
        print("Error generating report:", e)

    finally:
        cursor.close()
        conn.close()


def main():
    print("Sawubona! Welcome to Kasi Transport Tracker!")
    create_tables()
    
    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Add Driver")
        print("2. Add Route")
        print("3. Record Trip")
        print("4. Daily Report")
        print("5. Exit")
        print("================================")

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
            print("Exiting... Hamba kahle!")
            break
        else:
            print("Invalid choice. Please try again.")
   

if __name__ == "__main__":
    main()
