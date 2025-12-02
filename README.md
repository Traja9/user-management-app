# Complete Setup Guide: User Management App

## Project Overview
Full-stack web application with React frontend, Flask backend, and MySQL database featuring smart search, pagination, and 100k+ user management.

---

## 📋 Prerequisites

Before starting, ensure you have installed:
- **Node.js** (v18+) - [Download](https://nodejs.org/)
- **Python** (v3.8+) - [Download](https://www.python.org/)
- **MySQL** (v5.7+) - [Download](https://www.mysql.com/downloads/)
- **Git** - [Download](https://git-scm.com/)

Verify installations:
```bash
node --version
python3 --version
mysql --version
```

---

## 🗄️ Step 1: MySQL Database Setup

### 1.1 Start MySQL Service

**Linux/Mac:**
```bash
mysql.server start
```

**Windows:**
```bash
net start MySQL80
```

### 1.2 Login to MySQL

```bash
mysql -u root -p
```
Enter your MySQL root password when prompted.

### 1.3 Create Database and User

```sql
-- Create database
CREATE DATABASE mydb;

-- Create user
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';

-- Grant permissions
GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

### 1.4 Create Users Table

```bash
mysql -u myuser -p mydb
```

Enter password: `mypassword`

Then run:
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Verify table creation:
```sql
SHOW TABLES;
DESCRIBE users;
EXIT;
```

---

## 🐍 Step 2: Flask Backend Setup

### 2.1 Navigate to Backend Folder

```bash
cd backend
```

### 2.2 Create Python Virtual Environment

```bash
python3 -m venv venv
```

### 2.3 Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal.

### 2.4 Install Python Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, create it:
```bash
pip install Flask flask-cors mysql-connector-python Faker
```

Then save it:
```bash
pip freeze > requirements.txt
```

### 2.5 Update Flask Configuration

Edit `app.py` and verify these credentials:

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="myuser",           # Your MySQL username
        password="mypassword",   # Your MySQL password
        database="mydb"          # Your database name
    )
```

### 2.6 Generate Sample Data (Optional)

Create `generate_data.py`:

```python
from faker import Faker
import mysql.connector

fake = Faker()

def generate_users(count=100000):
    db = mysql.connector.connect(
        host="localhost",
        user="myuser",
        password="mypassword",
        database="mydb"
    )
    cursor = db.cursor()
    
    batch_size = 1000
    users = []
    
    print(f"Generating {count} users...")
    
    for i in range(count):
        name = fake.name()
        email = fake.email()
        users.append((name, email))
        
        if len(users) == batch_size:
            cursor.executemany(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                users
            )
            db.commit()
            print(f"Inserted {i + 1} users...")
            users = []
    
    if users:
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            users
        )
        db.commit()
    
    cursor.close()
    db.close()
    print("✅ Data generation complete!")

if __name__ == "__main__":
    generate_users(100000)
```

Run it:
```bash
python3 generate_data.py
```

### 2.7 Start Flask Server

```bash
python3 app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
```

Keep this terminal open!

---

## ⚛️ Step 3: React Frontend Setup

### 3.1 Navigate to Frontend Folder

**In a new terminal:**

```bash
cd myapp
```

### 3.2 Install Dependencies

```bash
npm install
```

This installs all packages from `package.json`.

### 3.3 Verify API Connection

Make sure your `App.jsx` has the correct backend URL:

```javascript
const response = await fetch('http://localhost:5001/users');
```

If Flask is running on a different port, update this URL.

### 3.4 Start React Development Server

```bash
npm run dev
```

You should see:
```
VITE v7.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
```

### 3.5 Open in Browser

Visit: **http://localhost:5173/**

---

## 🔧 Step 4: Verify Everything Works

### Test Backend API

In your browser or terminal, visit:
```
http://localhost:5001/users
```

You should see JSON data with user records.

### Test Frontend

1. Open **http://localhost:5173/**
2. You should see the "User Management App"
3. Try searching for a user
4. Try adding a new user
5. Load more users

---

## 📁 Project Structure

```
user-management-app/
├── myapp/                          # React Frontend
│   ├── src/
│   │   ├── App.jsx                # Main React component
│   │   ├── App.css                # Styling
│   │   ├── main.jsx               # Entry point
│   │   └── index.css              # Global styles
│   ├── index.html                 # HTML template
│   ├── package.json               # Dependencies
│   ├── vite.config.js             # Vite config
│   └── eslint.config.js           # Linting config
│
├── backend/                        # Flask Backend
│   ├── app.py                     # Flask application
│   ├── generate_data.py           # Data generation script
│   ├── requirements.txt           # Python dependencies
│   └── venv/                      # Virtual environment
│
└── README.md                       # Project documentation
```

---

## 🚀 Running the Full Application

### Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate          # or venv\Scripts\activate on Windows
python3 app.py
```

### Terminal 2 (Frontend):
```bash
cd myapp
npm run dev
```

### Terminal 3 (Optional - Data Generation):
```bash
cd backend
source venv/bin/activate
python3 generate_data.py
```

---

## 🆘 Troubleshooting

### Issue: "Can't connect to MySQL server"
**Solution:**
```bash
# Check if MySQL is running
mysql -u myuser -p

# If not, start it
mysql.server start  # Mac/Linux
net start MySQL80   # Windows
```

### Issue: "Port 5001 already in use"
**Solution:**
```bash
# Change port in app.py
app.run(debug=True, port=5002)  # Use 5002 instead
```

### Issue: "Port 5173 already in use"
**Solution:**
```bash
# Vite will auto-assign next available port
npm run dev
```

### Issue: "Module not found" in Python
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Module not found" in Node
**Solution:**
```bash
# Reinstall dependencies
npm install

# Clear cache if needed
npm cache clean --force
npm install
```

### Issue: Search not returning results
**Solution:**
1. Verify data was inserted: 
```sql
SELECT COUNT(*) FROM users;
```
2. Check Flask is running on correct port
3. Verify API endpoint: `http://localhost:5001/search?q=John`

---

## 📊 Database Management

### View All Users:
```sql
SELECT * FROM users LIMIT 10;
```

### Count Users:
```sql
SELECT COUNT(*) FROM users;
```

### Search Users:
```sql
SELECT * FROM users WHERE name LIKE 'John%';
```

### Delete All Users:
```sql
DELETE FROM users;
ALTER TABLE users AUTO_INCREMENT = 1;
```

---

## 📦 Dependencies

### Python (Backend)
- **Flask** - Web framework
- **flask-cors** - Handle cross-origin requests
- **mysql-connector-python** - MySQL connection
- **Faker** - Generate random data

### Node.js (Frontend)
- **React** - UI framework
- **Vite** - Build tool
- **ESLint** - Code quality

---

## 🌐 Deployment (Optional)

### Deploy Backend (Heroku)
```bash
heroku create your-app-name
git push heroku main
```

### Deploy Frontend (Vercel)
```bash
npm install -g vercel
vercel
```

---

## 📝 Environment Variables

Create `.env` file in backend (if needed):

```
FLASK_ENV=development
FLASK_DEBUG=True
DB_HOST=localhost
DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=mydb
```

Load in `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv('DB_USER')
```

---

## ✅ Quick Checklist

- [ ] MySQL installed and running
- [ ] Database `mydb` created
- [ ] User `myuser` created
- [ ] `users` table created
- [ ] Python venv activated
- [ ] Flask dependencies installed
- [ ] Flask server running on 5001
- [ ] Node dependencies installed
- [ ] React server running on 5173
- [ ] Can see data in browser
- [ ] Search functionality working
- [ ] Add user functionality working

---

## 🎉 You're All Set!

Your full-stack application is now ready. Start developing!

**Need Help?**
- Check API: http://localhost:5001/users
- Check Frontend: http://localhost:5173
- Check Flask Logs: Terminal 1
- Check Browser Console: F12 in browser

Happy coding! 🚀
