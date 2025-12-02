const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Create a new connection for each query
function queryDatabase(sql, params) {
  return new Promise((resolve, reject) => {
    const db = mysql.createConnection({
      host: "localhost",
      user: "myuser",
      password: "mypassword",
      database: "mydb"
    });

    db.connect((err) => {
      if (err) {
        reject(err);
        return;
      }

      db.query(sql, params || [], (err, results) => {
        db.end();
        if (err) {
          reject(err);
        } else {
          resolve(results);
        }
      });
    });
  });
}

// Root route
app.get("/", (req, res) => {
  res.json({ message: "Backend server is running" });
});

// GET all users
app.get("/users", async (req, res) => {
  try {
    console.log("GET /users - querying");
    const results = await queryDatabase("SELECT * FROM users");
    console.log("GET /users - success");
    res.json(results);
  } catch (err) {
    console.log("GET /users - error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// ADD new user
app.post("/users", async (req, res) => {
  try {
    const { name, email } = req.body;
    const result = await queryDatabase("INSERT INTO users (name, email) VALUES (?, ?)", [name, email]);
    res.json({ message: "User added successfully", id: result.insertId });
  } catch (err) {
    console.log("POST /users - error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

// Start Server
app.listen(5000, () => {
  console.log("Backend server running at: http://localhost:5000");
});
