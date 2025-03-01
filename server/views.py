from app import app, users_collection
from flask import request, jsonify
from bson.objectid import ObjectId
import time

@app.route("/api/users", methods=["GET"])
def get_users():
    """
    Retrieve all users
    """
    try:
        users = list(users_collection.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/users", methods=["POST"])
def create_user():
    """
    Create a new user
    """
    try:
        user_data = request.json
        user_data["created_ts"] = time.time()
        user_data["updated_ts"] = time.time()
        
        # Validate required fields
        required_fields = ["username", "password", "roles", "preferences"]
        if not all(field in user_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        result = users_collection.insert_one(user_data)
        return jsonify({"inserted_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update an existing user by ID.
    """
    try:
        update_data = request.json
        update_data["updated_ts"] = time.time()
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "message": "User updated successfully",
            "modified_count": result.modified_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by ID.
    """
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "message": "User deleted successfully",
            "deleted_count": result.deleted_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a single user by ID.
    """
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500