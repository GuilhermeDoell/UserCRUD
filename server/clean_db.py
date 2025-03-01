from database import DatabaseService

def test_db_connection():
    db = DatabaseService()
    users = db.get_collection("users")
    
    # Test insert
    test_user = {
        "username": "test_user",
        "password": "test_password",
        "roles": ["USER"],
        "preferences": {"timezone": "UTC"}
    }
    
    result = users.insert_one(test_user)
    print(f"Inserted user with id: {result.inserted_id}")
    
    db.close_connection()

def clean_database():
    """Clean all collections in the database"""
    try:
        db = DatabaseService()
        users = db.get_collection("users")
        
        # Delete all documents from users collection
        result = users.delete_many({})
        print(f"Deleted {result.deleted_count} documents from users collection")
        
        db.close_connection()
        return True
    except Exception as e:
        print(f"Error cleaning database: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()
    clean_database()