import json
from datetime import datetime
from models import UserRole, User, UserPreferences, UserModel

def parse_and_load_users():
    try:
        user_model = UserModel()

        with open('./udata.json', 'r') as file:
            data = json.load(file)
            users_data = data.get('users', [])

        inserted_count = 0
        for user_data in users_data:
            # Parse roles
            roles = []
            if user_data.get('is_user_admin'):
                roles.append(UserRole.ADMIN)
            if user_data.get('is_user_manager'):
                roles.append(UserRole.MANAGER)
            if user_data.get('is_user_tester'):
                roles.append(UserRole.USER)

            baseDate = datetime.strptime(
                user_data['created_at'], 
                "%Y-%m-%dT%H:%M:%SZ"
            ).timestamp()
            user = User(
                username=user_data['user'],
                password=user_data['password'],
                roles=roles,
                preferences=UserPreferences(
                    timezone=user_data.get('user_timezone', 'UTC')
                ),
                updated_ts=baseDate,
                created_ts=baseDate,
                active=user_data.get('is_user_active', True)
            )

            try:
                user_model.create_user(user)
                inserted_count += 1
                print(f"Inserted user: {user.username}")
            except ValueError as e:
                print(f"Warning: {e}")

        print(f"Successfully inserted {inserted_count} users")
        return True

    except FileNotFoundError:
        print("Error: udata.json file not found")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in udata.json")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    parse_and_load_users()