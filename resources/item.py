import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sys

from models.item import ItemModel
from pprint import pprint


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occured retrieving the item."}, 500

        if item:
            return item.json()
        return {"message": "item not found"}, 400

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exits."}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:    
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return item.json(), 201

    """ @jwt_required() """

    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": f"Item {name} deleted"}

    """ @jwt_required() """

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"])
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.commit()
        connection.close()

        return {"items": items}
