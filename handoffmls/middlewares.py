from functools import wraps
from flask import session, redirect

# Authentication middleware decorator
def authentication_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        # Check if user is authenticated
        if 'user_id' in session:
            # User is authenticated, proceed to the route function
            return route_function(*args, **kwargs)
        else:
            # User is not authenticated, redirect to login page
            return redirect('/login')  # Replace with your login route

    return wrapper