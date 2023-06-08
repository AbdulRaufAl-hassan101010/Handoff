from handoffmls import create_app, db
# imported tables to make db.reflect  create tables in order specified
from handoffmls.models.lab import Lab
from handoffmls.models.user import User
from handoffmls.models.task import Task
from handoffmls.models.handoff import Handoff


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Define the tables in the desired order
        db.reflect()
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5002)

