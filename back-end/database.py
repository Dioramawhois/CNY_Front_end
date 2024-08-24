import psycopg2

class Database:
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host=host, 
            database=database, 
            user=user, 
            password=password
        )
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, username, user_firstname):
        try:
            self.cursor.execute(
                "INSERT INTO users (userid, username, user_firstname) VALUES (%s, %s, %s)",
                (user_id, username, user_firstname)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error adding user: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE userid = %s", (user_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error deleting user: {e}")

    def fetch_users(self):
        try:
            self.cursor.execute("SELECT * FROM users ORDER BY userid ASC")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    def close(self):
        self.cursor.close()
        self.connection.close()
