import mysql.connector
import getpass
import logging

# Setup logging
logging.basicConfig(filename='store.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Hiei82087',
            database='gordys_novelties_db'
        )
        logging.info("Connected to the database.")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Database connection error: {err}")
        return None

# User login function
def login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        connection.close()

        if user and user['password'] == password:  # Replace with hashed password check in production
            logging.info(f"User {username} logged in.")
            return user
        else:
            print("Invalid credentials!")
            logging.warning(f"Failed login attempt for user {username}.")
    return None

# New account creation function
def create_account():
    username = input("Enter desired username: ")
    password = getpass.getpass("Enter desired password: ")
    
    # Set the role to 'user' by default
    role = 'user'

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
            connection.commit()
            logging.info(f"New account created for user {username}.")
            print("Account created successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            logging.error(f"Failed to create account for {username}: {err}")
        finally:
            connection.close()

# Function to display products
def display_products():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM gordys_novelties')
        products = cursor.fetchall()
        connection.close()
        
        for product in products:
            print(f"{product['id']}: {product['item']} - ${product['price']} (Quantity: {product['quantity']})")

# Function to create an order
def create_order(user_id):
    product_id = int(input("Enter product ID to order: "))
    quantity = int(input("Enter quantity: "))
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)', (user_id, product_id, quantity))
        connection.commit()
        connection.close()
        logging.info(f"Order created for user ID {user_id}: Product ID {product_id}, Quantity {quantity}.")
        print("Order created!")

# Admin functionality to view all users and orders
def admin_view():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)

        # View all users
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        print("\nUsers:")
        for user in users:
            print(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")
        
        # View all orders
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        print("\nOrders:")
        for order in orders:
            print(f"Order ID: {order['id']}, User ID: {order['user_id']}, Product ID: {order['product_id']}, Quantity: {order['quantity']}")
        
        connection.close()

# Main application loop
def main():
    while True:
        print("\n1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            user = login()
            if user:
                while True:
                    print("\n1. View Products")
                    print("2. Create Order")
                    if user['role'] == 'admin':
                        print("3. Admin View")
                    print("4. Logout")
                    action = input("Select an option: ")

                    if action == '1':
                        display_products()
                    elif action == '2':
                        create_order(user['id'])
                    elif action == '3' and user['role'] == 'admin':
                        admin_view()
                    elif action == '4':
                        logging.info(f"User {user['username']} logged out.")
                        break
                    else:
                        print("Invalid option!")
        elif choice == '2':
            create_account()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()