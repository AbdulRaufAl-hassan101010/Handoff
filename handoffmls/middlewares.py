from functools import wraps
from flask import session, redirect

# Authentication middleware decorator
def authentication_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        
        # Check if user is authenticated
        if 'username' in session:
            # User is authenticated, proceed to the route function
            return route_function(*args, **kwargs)
        else:
            # User is not authenticated, redirect to login page
            return redirect('/login') 

    return wrapper


# Authentication middleware decorator
def is_logged_in(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        
        # Check if user is authenticated
        if 'username' in session:
            # User is authenticated, redirect to dashboard page
            return redirect('/dashboard') 
            
        else:
            # User is not authenticated, proceed to the route function            
            return route_function(*args, **kwargs) 

    return wrapper