class User:
    # Create a new user
    def __init__(self, username, password_hash, role):
        self._username = username
        self._password_hash = password_hash
        self._role = role

    # Get the username
    @property
    def username(self):
        return self._username

    # Get the password hash
    @property
    def password_hash(self):
        return self._password_hash

    # Get the user's role
    @property
    def role(self):
        return self._role

    # Convert the user information into a dictionary
    def to_dict(self):
        return {
            "username": self._username,
            "password_hash": self._password_hash,
            "role": self._role
        }