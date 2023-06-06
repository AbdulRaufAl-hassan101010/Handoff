from flask import Blueprint


landingpage = Blueprint('landingpage', __name__, template_folder="templates/landingpage")


from handoffmls.landingpage.routes import *
