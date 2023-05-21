from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/<name>")
def landing_page(name):
    print(name)
    return render_template(f"{name}.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)