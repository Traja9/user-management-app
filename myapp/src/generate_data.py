from faker import Faker
import mysql.connector
import sys

# Initialize Faker
fake = Faker()

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="myuser",
        password="mypassword",
        database="mydb"
    )

def generate_and_insert_users(count=100000):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        print(f"Starting to generate and insert {count} users...")
        
        # Generate data in batches (insert 1000 at a time for better performance)
        batch_size = 1000
        users_data = []
        
        for i in range(count):
            name = fake.name()
            email = fake.email()
            users_data.append((name, email))
            
            # Insert batch every 1000 records
            if len(users_data) == batch_size:
                insert_batch(cursor, users_data)
                users_data = []
                print(f"Inserted {i + 1} users...")
        
        # Insert remaining records
        if users_data:
            insert_batch(cursor, users_data)
        
        db.commit()
        cursor.close()
        db.close()
        
        print(f"✅ Successfully inserted {count} users into database!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def insert_batch(cursor, users_data):
    """Insert a batch of users"""
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.executemany(sql, users_data)

if __name__ == "__main__":
    # Change the number here if you want more or fewer records
    num_users = 100000
    generate_and_insert_users(num_users)
