from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from database import DatabaseService
import os

app = Flask(__name__)
CORS(app)

db_service = DatabaseService()
users_collection = db_service.get_collection("users")

if __name__ == "__main__":
    from views import *
    app.run(debug=True)


# user = User(
#     username="john_doe",
#     password="hashed_password",
#     roles=[UserRole.ADMIN, UserRole.MANAGER],  # Using enum values
#     preferences=UserPreferences(timezone="UTC"),
#     created_ts=time.time()
# )
# role = User.parse_role("is_user_admin")  # Returns UserRole.ADMIN
# role_string = User.format_role(UserRole.ADMIN)  # Returns "is_user_admin"