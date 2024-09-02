from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="119.159.147.37",  # Replace with your host
        user="pms_smart_usr",  # Replace with your MySQL username
        password="Trivelles@M26",  # Replace with your MySQL password
        database="newuser_data"
    )

@app.route('/')
def index():
    return render_template('test1.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    username = data.get('signup-username')
    password = data.get('signup-password')
    email = data.get('email')
    phone = data.get('phone')
    user_type = data.get('user-type')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (username, password, email, phone, user_type) VALUES (%s, %s, %s, %s, %s)",
            (username, password, email, phone, user_type)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM Users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({"message": "Login successful!", "user": user}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
