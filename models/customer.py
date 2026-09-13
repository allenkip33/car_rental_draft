from models.user import User


class Customer(User):
    # Create a customer
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, "Customer")

    # Customer can rent a car
    def can_rent(self):
        return True

