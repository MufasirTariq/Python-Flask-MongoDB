from flask import Flask, request, render_template, jsonify, session
from werkzeug.utils import secure_filename
import os
from database.models import Customers
from database import db
from flask_session import Session
app = Flask(__name__)




app.secret_key = 'encrypted'
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)
app.config["MONGODB_SETTINGS"] = {"host": "mongodb://localhost:27017/belaciao"}
db.initialize_db(app)

@app.route("/")
def route_root():
    return render_template("Home.html")

@app.route("/registerCustomer", methods=['POST'])
def RegisterCustomer():
    data = request.form.to_dict()
    image = request.files["image"]
    filename = secure_filename(image.filename)
    filepath = os.path.join("static", filename)
    image.save(filepath)

    customer = Customers(
        email=data["email"], password=data["password"], name=data["name"],
        address=data["address"], phone=data["phone"], image=filename).save()

    res = {"customer_id": str(customer.id)}
    session["cus_id"] = customer.id
    return jsonify(res)

@app.route("/LoginCustomer", methods=['POST'])
def LoginCustomer():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    customer = Customers.objects.get(email=email, password=password)
    customer_id = str(customer.id)
    session["cus_id"] = customer.id
    return jsonify(customer_id)

@app.route("/redirect")
def redirect():
    if session.get("cus_id") is not None:
        cus_id = session["cus_id"]
        customer = Customers.objects.get(id=cus_id)
        name = customer.name
        image = customer.image
        path = "/static/" + image
        return render_template("CustomerProfile.html", name=name, image=path)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("Home.html")

@app.route("/accountSettings")
def accountSettings():
    if session.get("cus_id") is not None:
        cus_id = session["cus_id"]
        customer = Customers.objects.get(id=cus_id)
        name = customer.name
        image = customer.image
        password = customer.password
        email = customer.email
        phone = customer.phone
        address = customer.address
        return render_template("AccountSettings.html", cus_id=cus_id, name=name, image=image,
                                                  password=password, email=email, phone=phone, address=address)

@app.route("/updateProfile/<id>", methods=["PUT"])
def update_customer(id):
    data = request.form.to_dict()
    image = request.files["image"]
    filename = secure_filename(image.filename)
    filepath = os.path.join("static", filename)
    image.save(filepath)

    Customers.objects(id=id).update(email=data["email"], password=data["password"], name=data["name"],
                                    address=data["address"], phone=data["phone"], image=filename)
    res = {"customer_id": str(id)}
    return jsonify(res)


@app.route("/deleteCustomer/<id>", methods=["DELETE"])
def deleteCustomer(id):
    Customers.objects(id=id).delete()
    res = {'id': str(id), "deleted": "failed"}
    return jsonify(res)
if __name__ == '__main__':
    app.run()