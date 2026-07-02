import subprocess

from flask import Flask, render_template, request, redirect, flash, session
import os

app = Flask(__name__)
app.secret_key = "smartprintshop123"
ADMIN_USERNAME = "BITUPAN2488"
ADMIN_PASSWORD = "FX23bb@@"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Upload folder create if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Temporary memory storage
jobs = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload-page")
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():

    customer_name = request.form.get("name")
    print_type = request.form.get("print_type")
    copies = request.form.get("copies")
    paper_size = request.form.get("paper_size")

    file = request.files["file"]

    filename = file.filename
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    jobs.append({
        "id": len(jobs)+1,
        "customer_name": customer_name,
        "filename": filename,
        "print_type": print_type,
        "copies": copies,
        "paper_size": paper_size,
        "status":"Pending"
    })

    flash("✅ File uploaded successfully!")
    return redirect("/upload-page")

@app.route("/cancel/<int:id>")
def cancel_job(id):
    for job in jobs:
        if job["id"] == id:
            job["status"] = "Failed"

    return redirect("/admin")

@app.route("/print/<int:id>")
def print_job(id):
    for job in jobs:
        if job["id"] == id:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], job["filename"])

            # File ko default printer par bheje
            subprocess.run(["lp", filepath])

            job["status"] = "Completed"

    return redirect("/admin")

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")

    return render_template("admin.html", jobs=jobs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        else:
            flash("Invalid Username or Password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, port=5050)