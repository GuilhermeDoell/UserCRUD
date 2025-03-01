from dataclasses import dataclass
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from typing import List
from enum import Enum
import os

class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: List[UserRole]
    preferences: UserPreferences
    updated_ts: float
    created_ts: float
    active: bool = True

class UserModel:
    def __init__(self):
        mongo_uri = os.getenv(
            "MONGO_URI", 
            "mongodb://admin:password@localhost:27017/my_database?authSource=admin" 
        ) # not using .env file again for simplicity
        self.client = MongoClient(mongo_uri)
        self.db = self.client["my_database"]
        self.collection = self.db["users"]

        self.collection.create_index([("username", ASCENDING)], unique=True)

    def create_user(self, user: User):
        try:
            # Convert user object, roles and prefernces
            user_dict = user.__dict__.copy()
            user_dict['roles'] = [role.value for role in user.roles]
            user_dict['preferences'] = user.preferences.__dict__
            
            result = self.collection.insert_one(user_dict)
            return str(result.inserted_id)
        except DuplicateKeyError:
            raise ValueError(f"User with username '{user.username}' already exists")

    def get_user(self, username: str):
        user_dict = self.collection.find_one({"username": username})
        if user_dict:
            # Convert role strings back to Enum
            user_dict['roles'] = [UserRole(role) for role in user_dict['roles']]
            user_dict['preferences'] = UserPreferences(**user_dict['preferences'])
            return User(**user_dict)
        return None

    def update_user(self, username: str, update_data: dict):
        result = self.collection.update_one({"username": username}, {"$set": update_data})
        return result.modified_count

    def delete_user(self, username: str):
        result = self.collection.delete_one({"username": username})
        return result.deleted_count