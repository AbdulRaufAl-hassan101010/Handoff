from flask import Blueprint, render_template

dashboard = Blueprint("dashboard", __name__,
                      template_folder="templates")


from handoffmls.dashboard.routes import *

print(dashboard)


# @dashboard.route("/")
# def dash():
#     return render_template("home.html")
