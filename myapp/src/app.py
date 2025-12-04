from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = '/home/Savan9900990099/user-management-app/users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend server is running"})

@app.route("/users", methods=["GET"])
def get_users():
    try:
        limit = request.args.get('limit', 20, type=int)
        cursor_param = request.args.get('cursor', None)
        
        conn = get_db()
        cursor = conn.cursor()
        
        if cursor_param:
            last_id = int(cursor_param)
            cursor.execute(
                "SELECT * FROM users WHERE id > ? ORDER BY id ASC LIMIT ?",
                (last_id, limit + 1)
            )
        else:
            cursor.execute("SELECT * FROM users ORDER BY id ASC LIMIT ?", (limit + 1,))
        
        rows = cursor.fetchall()
        conn.close()
        
        has_more = len(rows) > limit
        if has_more:
            rows = rows[:limit]
        
        next_cursor = None
        if has_more and rows:
            next_cursor = rows[-1]['id']
        
        users = [dict(row) for row in rows]
        
        return jsonify({
            "users": users,
            "nextCursor": next_cursor,
            "hasMore": has_more,
            "count": len(users)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["GET"])
def search_users():
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 10, type=int)
        
        if not query:
            return jsonify({"results": []})
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email FROM users WHERE name LIKE ? ORDER BY name ASC LIMIT ?",
            (f"{query}%", limit)
        )
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({"results": results, "count": len(results)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        
        if not name or not email:
            return jsonify({"error": "Name and email required"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({"message": "User added successfully", "id": user_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve():
    try:
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), '../myapp/dist'),
            'index.html'
        )
    except:
        return jsonify({"message": "React app"})

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), '../myapp/dist'),
            path
        )
    except:
        return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)
