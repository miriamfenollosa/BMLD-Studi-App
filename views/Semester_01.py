from flask import Flask, render_template, request

app = Flask(__name__)

# Startseite mit Tabelle
@app.route("/")
def index():
    schueler = [
        {"name": "Max", "klasse": "10A"},
        {"name": "Anna", "klasse": "10B"}
    ]
    return render_template("index.html", schueler=schueler)

# Seite für Noten
@app.route("/noten/<name>", methods=["GET", "POST"])
def noten(name):
    if request.method == "POST":
        mathe = request.form["mathe"]
        deutsch = request.form["deutsch"]
        englisch = request.form["englisch"]

        return f"Gespeichert für {name}: {mathe}, {deutsch}, {englisch}"

    return render_template("noten.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)
