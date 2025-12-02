const mysql = require("mysql2/promise");

async function test() {
  try {
    const pool = mysql.createPool({
      host: "localhost",
      user: "myuser",
      password: "mypassword",
      database: "mydb"
    });
    
    console.log("Pool created");
    
    const connection = await pool.getConnection();
    console.log("Got connection");
    
    const [results] = await connection.query("SELECT * FROM users");
    console.log("Query successful:", results);
    
    connection.release();
    pool.end();
  } catch (err) {
    console.log("ERROR:", err.message);
  }
}

test();

