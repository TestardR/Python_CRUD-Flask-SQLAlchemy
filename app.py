from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from utils.security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister
from db.db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# To allow flask propagating exception even if debug is set to false on app
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "my_secret"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
