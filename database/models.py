from .db import db

class Customers(db.Document):
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    phone = db.StringField(required=True)
    address = db.StringField(required=True)
    image = db.StringField(required=True)


class PaymentInfo(db.Document):
    cus_id = db.StringField(required=True)
    pay_method = db.StringField(required=True)
    number = db.StringField
    card_no = db.StringField
    card_exp = db.StringField
    card_cvv = db.StringField


class OrderInfo(db.Document):
    cus_id = db.StringField(required=True)
    order = db.StringField(required=True)
    time = db.StringField(required=True)
    date = db.StringField(required=True)
    amount = db.StringField(required=True)
    pay_method = db.StringField(required=True)
    rec_method = db.StringField(required=True)


