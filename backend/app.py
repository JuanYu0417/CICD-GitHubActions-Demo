from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD', 'apppassword123'),
        database=os.getenv('DB_NAME', 'appdb')
    )

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/users', methods=['GET', 'POST'])
def manage_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')

            if not name:
                return jsonify({"error": "Name is required"}), 400

            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )
            conn.commit()

            new_id = cursor.lastrowid
            cursor.execute("SELECT * FROM users WHERE id = %s", (new_id,))
            user = cursor.fetchone()

            return jsonify(user), 201

        else:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return jsonify(users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/api/init-db', methods=['GET', 'POST'])
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        cursor.execute("""
            INSERT INTO users (name, email) VALUES
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com')
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Database initialized"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
