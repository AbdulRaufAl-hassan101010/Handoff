from handoffmls import app, db
from handoffmls import routes

if __name__ == "__main__":
        """UNCOMMENT WHEN RUNNING THE FIRST TIME"""
    #with app.app_context():
        #db.create_all()
        app.run(host="0.0.0.0", debug=True, port=5000)