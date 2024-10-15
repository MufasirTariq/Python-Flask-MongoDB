from flask import request, Response, jsonify
from flask_restful import Resource
from database.models import Customers

class CustomerAPI(Resource):
    def post(self):
        data = request.get_json()
        cus = Customers(**data).save()
        return {"id": str(cus.id)}, 200
