from datetime import date


class Rental:
    # Create a rental
    def __init__(self, rental_id, username, car_id, start_date, end_date, price_per_day):
        self._rental_id = rental_id
        self._username = username
        self._car_id = car_id
        self._start_date = start_date
        self._end_date = end_date
        self._price_per_day = price_per_day
        self._status = "Active"

    @property
    def rental_id(self):
        return self._rental_id

    @property
    def username(self):
        return self._username

    @property
    def car_id(self):
        return self._car_id

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    # Calculate number of rental days
    def rental_days(self):
        start = date.fromisoformat(self._start_date)
        end = date.fromisoformat(self._end_date)
        return (end - start).days

    # Calculate total rental cost
    def total_cost(self):
        return self.rental_days() * self._price_per_day

    # Cancel the rental
    def cancel(self):
        self._status = "Cancelled"

    # Convert rental information into a dictionary
    def to_dict(self):
        return {
            "rental_id": self._rental_id,
            "username": self._username,
            "car_id": self._car_id,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "price_per_day": self._price_per_day,
            "status": self._status
        }
