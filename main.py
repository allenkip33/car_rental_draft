from rich.console import Console
from rich.table import Table

from services.auth import AuthService
from services.data_manager import DataManager
from services.rental_service import RentalService
from utils.validators import validate_date, validate_required


console = Console()

USERS_FILE = "data/users.json"
CARS_FILE = "data/cars.json"
RENTALS_FILE = "data/rentals.json"

manager = DataManager()
auth = AuthService(manager, USERS_FILE)
rental_service = RentalService(manager, RENTALS_FILE, CARS_FILE)


def register():
    console.print("\n--- Register ---")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if not validate_required(username) or not validate_required(password):
        console.print("Username and password are required.")
        return

    result = auth.register(username, password)

    if result:
        console.print("User registered successfully.")
    else:
        console.print("Username already exists.")


def login():
    console.print("\n--- Login ---")

    username = input("Enter username: ")
    password = input("Enter password: ")

    user = auth.login(username, password)

    if user:
        console.print(f"Login successful. Welcome {user.username}!")
        console.print(f"Role: {user.role}")
        return user

    console.print("Invalid username or password.")
    return None


def list_cars():
    cars = manager.load_data(CARS_FILE)

    if not cars:
        console.print("No cars found.")
        return

    table = Table(title="Available Cars")

    table.add_column("ID")
    table.add_column("Brand")
    table.add_column("Model")
    table.add_column("Year")
    table.add_column("Price/Day")
    table.add_column("Available")

    for car in cars:
        table.add_row(
            car["car_id"],
            car["brand"],
            car["model"],
            str(car["year"]),
            str(car["price_per_day"]),
            str(car["available"])
        )

    console.print(table)


def add_car(user):
    if user is None or user.role != "Admin":
        console.print("Only an Admin can add cars.")
        return

    console.print("\n--- Add Car ---")

    car_id = input("Enter car ID: ")
    brand = input("Enter brand: ")
    model = input("Enter model: ")
    year = input("Enter year: ")
    price = input("Enter price per day: ")

    if not validate_required(car_id):
        console.print("Car ID is required.")
        return

    cars = manager.load_data(CARS_FILE)

    for car in cars:
        if car["car_id"] == car_id:
            console.print("Car ID already exists.")
            return

    try:
        year = int(year)
        price = float(price)
    except ValueError:
        console.print("Year and price must be numbers.")
        return

    new_car = {
        "car_id": car_id,
        "brand": brand,
        "model": model,
        "year": year,
        "price_per_day": price,
        "available": True
    }

    cars.append(new_car)
    manager.save_data(CARS_FILE, cars)

    console.print("Car added successfully.")


def rent_car(user):
    if user is None:
        console.print("Please login first.")
        return

    console.print("\n--- Rent a Car ---")

    list_cars()

    car_id = input("Enter car ID: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    if not validate_date(start_date):
        console.print("Invalid start date.")
        return

    if not validate_date(end_date):
        console.print("Invalid end date.")
        return

    rental = rental_service.create_rental(
        user.username,
        car_id,
        start_date,
        end_date
    )

    if rental:
        console.print("\nCar rented successfully.")
        console.print(f"Rental ID: {rental.rental_id}")
        console.print(f"Total cost: {rental.total_cost()}")
    else:
        console.print("\nCould not rent the car.")
        console.print("Check the car ID, availability, and rental dates.")


def list_rentals(user):
    if user is None:
        console.print("Please login first.")
        return

    rentals = manager.load_data(RENTALS_FILE)

    user_rentals = []

    for rental in rentals:
        if rental["username"] == user.username or user.role == "Admin":
            user_rentals.append(rental)

    if not user_rentals:
        console.print("No rentals found.")
        return

    table = Table(title="Rentals")

    table.add_column("Rental ID")
    table.add_column("Username")
    table.add_column("Car ID")
    table.add_column("Start")
    table.add_column("End")
    table.add_column("Status")

    for rental in user_rentals:
        table.add_row(
            rental["rental_id"],
            rental["username"],
            rental["car_id"],
            rental["start_date"],
            rental["end_date"],
            rental["status"]
        )

    console.print(table)


def cancel_rental(user):
    if user is None:
        console.print("Please login first.")
        return

    console.print("\n--- Cancel Rental ---")

    list_rentals(user)

    rental_id = input("Enter rental ID to cancel: ")

    rentals = manager.load_data(RENTALS_FILE)

    rental_found = False

    for rental in rentals:
        if rental["rental_id"] == rental_id:
            if rental["username"] != user.username and user.role != "Admin":
                console.print("You cannot cancel this rental.")
                return

            rental_found = True
            break

    if not rental_found:
        console.print("Rental not found.")
        return

    result = rental_service.cancel_rental(rental_id)

    if result:
        console.print("Rental cancelled successfully.")
    else:
        console.print("Could not cancel rental.")


def main():
    current_user = None

    while True:
        console.print("\n")
        console.print("================================")
        console.print("    CAR RENTAL SYSTEM")
        console.print("================================")

        if current_user:
            console.print(
                f"Logged in as: {current_user.username} "
                f"({current_user.role})"
            )

        console.print("\n1. Register")
        console.print("2. Login")
        console.print("3. List Cars")
        console.print("4. Add Car (Admin)")
        console.print("5. Rent a Car")
        console.print("6. My Rentals")
        console.print("7. Cancel Rental")
        console.print("8. Logout")
        console.print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            register()

        elif choice == "2":
            current_user = login()

        elif choice == "3":
            list_cars()

        elif choice == "4":
            add_car(current_user)

        elif choice == "5":
            rent_car(current_user)

        elif choice == "6":
            list_rentals(current_user)

        elif choice == "7":
            cancel_rental(current_user)

        elif choice == "8":
            current_user = None
            auth.logout()
            console.print("Logged out successfully.")

        elif choice == "9":
            console.print("Thank you for using the Car Rental System.")
            break

        else:
            console.print("Invalid choice. Please select 1-9.")


if __name__ == "__main__":
    main()