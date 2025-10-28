import psycopg2


def create_database():
    conn = psycopg2.connect(
        host="localhost",
        database="kasi_transport",
        user="postgres",
        password="mypassword"
    )
    print("Connection has been created")
    return conn


def create_tables():
    conn = create_database()
    cursor = conn.cursor()

    create_drivers_table = """
    CREATE TABLE IF NOT EXISTS drivers(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        taxi_number VARCHAR(15) NOT NULL
    );
    """

    create_routes_table = """
    CREATE TABLE IF NOT EXISTS routes(
    id SERIAL PRIMARY KEY,
    origin VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    fare NUMERIC(10, 2)
    );
    """



    create_trips_table = """
    CREATE TABLE IF NOT EXISTS trips(
    id SERIAL PRIMARY KEY,
    driver_id INTEGER NOT NULL REFERENCES drivers(id),
    route_id INTEGER NOT NULL REFERENCES routes(id),
    passengers INTEGER NOT NULL,
    total_amount NUMERIC(10, 2),
    trip_date TIMESTAMP 
);
"""


    cursor.execute(create_drivers_table)
    cursor.execute(create_routes_table)
    cursor.execute(create_trips_table)

    conn.commit()
    print("Tables have been created successfully")

    cursor.close()
    conn.close()

def add_driver(cursor, name, taxi_number):
    insert_query = """
        INSERT INTO drivers (name, taxi_number)
        VALUES (%s, %s);
    """
    cursor.execute(insert_query, (name, taxi_number))
    


def add_route(cursor, origin, destination, fare):
    cursor.execute("""
        INSERT INTO routes (origin, destination, fare)
        VALUES (%s, %s, %s)
    """, (origin, destination, fare))




    
    
def record_trip(cursor, driver_id, route_id, passengers):
    
    cursor.execute("SELECT fare FROM routes WHERE id = %s", (route_id,))
    route = cursor.fetchone()
    if route is None:
        raise ValueError(f"Route with ID {route_id} does not exist.")
    
    fare = route[0]
    total_amount = fare * passengers
    
    cursor.execute("""
        INSERT INTO trips (driver_id, route_id, passengers, total_amount, trip_date)
        VALUES (%s, %s, %s, %s, NOW())
    """, (driver_id, route_id, passengers, total_amount))
    
    return {
        'driver_id': driver_id,
        'route_id': route_id,
        'passengers': passengers,
        'total_amount': total_amount
    }
    

def reports(cursor, today):
    query = """
        SELECT 
            d.id AS driver_id,
            d.name AS driver_name,
            d.taxi_number,
            r.origin,
            r.destination,
            SUM(t.total_amount) AS total_earned,
            COUNT(t.id) AS trips_made
        FROM trips t
        JOIN drivers d ON t.driver_id = d.id
        JOIN routes r ON t.route_id = r.id
        WHERE DATE(t.trip_date) = %s
        GROUP BY d.id, d.name, d.taxi_number, r.origin, r.destination
        ORDER BY total_earned DESC;
    """
    cursor.execute(query, (today,))
    return cursor.fetchall()

def get_money(cursor, today):
     cursor.execute("""
            SELECT driver_id, SUM(total_amount) AS total_amount
            FROM trips
            WHERE DATE(trip_date) = %s
            GROUP BY driver_id
            ORDER BY total_amount DESC
            LIMIT 1;
        """, (today,))





create_tables()
