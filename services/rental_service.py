from models.rental import Rental


class RentalService:
    def __init__(self, data_manager, rentals_file, cars_file):
        self.data_manager = data_manager
        self.rentals_file = rentals_file
        self.cars_file = cars_file

    # Check if the dates overlap with another rental
    def dates_overlap(self, start_date, end_date, rental):
        return start_date < rental["end_date"] and end_date > rental["start_date"]

    # Create a new rental
    def create_rental(self, username, car_id, start_date, end_date):
        cars = self.data_manager.load_data(self.cars_file)
        rentals = self.data_manager.load_data(self.rentals_file)

        car = None

        for item in cars:
            if item["car_id"] == car_id:
                car = item
                break

        if car is None:
            return False

        if not car["available"]:
            return False

        for rental in rentals:
            if rental["car_id"] == car_id and rental["status"] == "Active":
                if self.dates_overlap(start_date, end_date, rental):
                    return False

        rental_id = "R" + str(len(rentals) + 1)

        rental = Rental(
            rental_id,
            username,
            car_id,
            start_date,
            end_date,
            car["price_per_day"]
        )

        rentals.append(rental.to_dict())
        car["available"] = False

        self.data_manager.save_data(self.rentals_file, rentals)
        self.data_manager.save_data(self.cars_file, cars)

        return rental

    # Cancel a rental
    def cancel_rental(self, rental_id):
        rentals = self.data_manager.load_data(self.rentals_file)
        cars = self.data_manager.load_data(self.cars_file)

        for rental in rentals:
            if rental["rental_id"] == rental_id:
                rental["status"] = "Cancelled"

                for car in cars:
                    if car["car_id"] == rental["car_id"]:
                        car["available"] = True

                self.data_manager.save_data(self.rentals_file, rentals)
                self.data_manager.save_data(self.cars_file, cars)

                return True

        return False
