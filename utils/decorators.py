from functools import wraps

def login_required(auth_service):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if auth_service.current_user is None:
                print("\n[bold red]Please login first.[/bold red]")
                return None
            return function(*args, **kwargs)
        return wrapper
    return decorator
