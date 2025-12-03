from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import base64
import json

app = Flask(__name__)
CORS(app)

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="myuser",
        password="mypassword",
        database="mydb"
    )

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend server is running"})

@app.route("/users", methods=["GET"])
def get_users():
    """
    Cursor-based pagination endpoint
    Query params:
    - cursor: base64 encoded ID (optional, for next page)
    - limit: number of records to return (default: 20, max: 100)
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        cursor = request.args.get('cursor', None)
        
        # Validate limit
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 20
        
        db = get_db_connection()
        cursor_obj = db.cursor(dictionary=True)
        
        # If cursor exists, decode it to get the ID
        if cursor:
            try:
                last_id = int(base64.b64decode(cursor).decode())
            except:
                return jsonify({"error": "Invalid cursor"}), 400
            
            # Get records after the cursor ID
            cursor_obj.execute(
                "SELECT * FROM users WHERE id > %s ORDER BY id ASC LIMIT %s",
                (last_id, limit + 1)
            )
        else:
            # Get first batch of records
            cursor_obj.execute(
                "SELECT * FROM users ORDER BY id ASC LIMIT %s",
                (limit + 1,)
            )
        
        rows = cursor_obj.fetchall()
        cursor_obj.close()
        db.close()
        
        # Check if there are more records
        has_more = len(rows) > limit
        if has_more:
            rows = rows[:limit]
        
        # Generate next cursor
        next_cursor = None
        if has_more and rows:
            last_id = rows[-1]['id']
            next_cursor = base64.b64encode(str(last_id).encode()).decode()
        
        return jsonify({
            "users": rows,
            "nextCursor": next_cursor,
            "hasMore": has_more,
            "count": len(rows)
        })
    
    except Exception as e:
        print(f"Error in GET /users: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["GET"])
def search_users():
    """
    Smart search endpoint with autocomplete
    Query params:
    - q: search query (name or email prefix)
    - limit: max results (default: 10)
    """
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        if not query or len(query) < 1:
            return jsonify({"results": []})
        
        if limit > 50:
            limit = 50
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Search by name (case-insensitive prefix match)
        cursor.execute(
            "SELECT id, name, email FROM users WHERE name LIKE %s ORDER BY name ASC LIMIT %s",
            (f"{query}%", limit)
        )
        
        results = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify({"results": results, "count": len(results)})
    
    except Exception as e:
        print(f"Error in GET /search: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """Get specific user by ID"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        print(f"Error in GET /users/<id>: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/users", methods=["POST"])
def add_user():
    """Add a new user"""
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        
        print(f"Adding user: {name}, {email}")
        
        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
        
        user_id = cursor.lastrowid
        cursor.close()
        db.close()
        
        print(f"User added with ID: {user_id}")
        return jsonify({"message": "User added successfully", "id": user_id})
    
    except Exception as e:
        print(f"Error in POST /users: {e}")
        return jsonify({"error": str(e)}), 500

def get_db_connection():
    return mysql.connector.connect(
        host="Savan9900990099.mysql.pythonanywhere-services.com",
        user="Savan9900990099$myuser",
        password="mypassword",
        database="Savan9900990099$mydb"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5002)
