import mysql.connector
import getpass
import logging

# Setup logging
logging.basicConfig(filename='store.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Database connection function
def get_db_connection():
    try:
        # Set the host, mysql user, mysql password to your machine's settings. Make sure to use the .sql file to create and populate the database before running - possibly in Workbench
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

        if user and user['password'] == password:
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
    
    role = 'user'  # Set the role to 'user' by default

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
            print(f"{product['id']}: {product['item']} - ${product['price']:.2f} (Quantity: {product['quantity']})")

# Function to get a valid integer input
def get_valid_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a non-negative integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Function to create an order
def create_order(user_id):
    product_id = get_valid_integer("Enter product ID to order: ")
    quantity = get_valid_integer("Enter quantity (must be at least 1): ")

    if quantity < 1:
        print("Quantity must be at least 1.")
        return
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM gordys_novelties WHERE id = %s', (product_id,))
        product = cursor.fetchone()
        
        if product:
            if product['quantity'] >= quantity:
                cursor.execute('INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)', (user_id, product_id, quantity))
                cursor.execute('UPDATE gordys_novelties SET quantity = quantity - %s WHERE id = %s', (quantity, product_id))
                connection.commit()
                logging.info(f"Order created for user ID {user_id}: Product ID {product_id}, Quantity {quantity}.")
                print("Order created! We will send you an invoice soon.")
            else:
                print("Cannot create order. Product is not available in sufficient quantity.")
        else:
            print("Invalid product ID. Cannot create order.")
        
        connection.close()

# Function to add a new item to inventory
def add_item_to_inventory():
    item_name = input("Enter the item name: ")
    price = float(input("Enter the item price: "))
    quantity = get_valid_integer("Enter the initial quantity: ")

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO gordys_novelties (item, price, quantity) VALUES (%s, %s, %s)', (item_name, price, quantity))
            connection.commit()
            logging.info(f"Added new item: {item_name} (Price: {price}, Quantity: {quantity}).")
            print("Item added to inventory successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            logging.error(f"Failed to add item to inventory: {err}")
        finally:
            connection.close()

# Function to change a user's role
def change_user_role():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        if not users:
            print("No users found.")
            return
        
        print("\nUsers:")
        for user in users:
            print(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")
        
        user_id = get_valid_integer("Enter the ID of the user to change role: ")
        
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        if not user:
            print("Invalid user ID. User does not exist.")
            return
        
        new_role = 'admin' if user['role'] == 'user' else 'user'
        
        try:
            cursor.execute('UPDATE users SET role = %s WHERE id = %s', (new_role, user_id))
            connection.commit()
            logging.info(f"User ID {user_id} role changed to {new_role}.")
            print(f"User role changed to {new_role}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            logging.error(f"Failed to change role for user ID {user_id}: {err}")
        finally:
            connection.close()

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

        # Mark an order as complete
        order_id = get_valid_integer("Enter Order ID to mark as complete (or 0 to skip): ")
        if order_id > 0:
            cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
            order = cursor.fetchone()
            if order:
                cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
                connection.commit()
                logging.info(f"Order ID {order_id} marked as complete.")
                print("Order marked as complete!")
            else:
                print("Invalid Order ID.")

        # Change user role
        if input("Change a user's role? (yes/no): ").strip().lower() == 'yes':
            change_user_role()

        # Add a new item to inventory
        if input("Add a new item to inventory? (yes/no): ").strip().lower() == 'yes':
            add_item_to_inventory()

        # Remove item from inventory
        if input("Remove an item from inventory? (yes/no): ").strip().lower() == 'yes':
            item_id = get_valid_integer("Enter item ID to remove: ")
            cursor.execute('SELECT * FROM gordys_novelties WHERE id = %s', (item_id,))
            item = cursor.fetchone()
            if item:
                try:
                    cursor.execute('DELETE FROM gordys_novelties WHERE id = %s', (item_id,))
                    connection.commit()
                    logging.info(f"Removed item with ID: {item_id}.")
                    print("Item removed successfully!")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    logging.error(f"Failed to remove item with ID: {item_id}: {err}")
            else:
                print("Invalid item ID. Item does not exist.")

        # Update item quantity
        if input("Update item quantity? (yes/no): ").strip().lower() == 'yes':
            item_id = get_valid_integer("Enter item ID to update: ")
            cursor.execute('SELECT * FROM gordys_novelties WHERE id = %s', (item_id,))
            item = cursor.fetchone()
            if item:
                new_quantity = get_valid_integer("Enter new quantity: ")
                try:
                    cursor.execute('UPDATE gordys_novelties SET quantity = %s WHERE id = %s', (new_quantity, item_id))
                    connection.commit()
                    logging.info(f"Updated item ID {item_id} to new quantity: {new_quantity}.")
                    print("Item quantity updated successfully!")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    logging.error(f"Failed to update quantity for item ID {item_id}: {err}")
            else:
                print("Invalid item ID. Item does not exist.")

        connection.close()

# Function to delete a user and their orders
def delete_user():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        if not users:
            print("No users found.")
            return
        
        print("\nUsers:")
        for user in users:
            print(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")
        
        user_id = get_valid_integer("Enter the ID of the user to delete: ")
        
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        if not user:
            print("Invalid user ID. User does not exist.")
            return
        
        # Confirm deletion
        confirm = input("Are you sure you want to delete this user and their associated orders? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Deletion canceled.")
            return
        
        try:
            # First delete the orders associated with the user
            cursor.execute('DELETE FROM orders WHERE user_id = %s', (user_id,))
            connection.commit()
            logging.info(f"Deleted orders for user ID {user_id}.")

            # Then delete the user
            cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
            connection.commit()
            print("User deleted successfully!")
            logging.info(f"User with ID {user_id} deleted.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            logging.error(f"Failed to delete user with ID {user_id}: {err}")
        finally:
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
                        print("4. Delete User")
                    print("5. Logout")
                    action = input("Select an option: ")

                    if action == '1':
                        display_products()
                    elif action == '2':
                        create_order(user['id'])
                    elif action == '3' and user['role'] == 'admin':
                        admin_view()
                    elif action == '4' and user['role'] == 'admin':
                        delete_user()
                    elif action == '5':
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
