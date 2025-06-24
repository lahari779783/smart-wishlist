from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend from any origin to access the API

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Set password if needed
app.config['MYSQL_DB'] = 'wishlist_app'

mysql = MySQL(app)

# Route: Home
@app.route('/')
def home():
    return '👋 Hello Lahari! Your Flask backend is running.'

# Route: Save item to wishlist
@app.route('/save', methods=['POST'])
def save_item():
    try:
        data = request.get_json()
        title = data.get('title')
        url = data.get('url')

        if not title or not url:
            return jsonify({"error": "Missing title or URL"}), 400

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO wishlist (title, url) VALUES (%s, %s)", (title, url))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "✅ Item saved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Get all wishlist items
@app.route('/wishlist', methods=['GET'])
def get_wishlist():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title, url FROM wishlist")
        items = cur.fetchall()
        cur.close()

        result = [{"id": row[0], "title": row[1], "url": row[2]} for row in items]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Delete a wishlist item by ID
@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM wishlist WHERE id = %s", (item_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "🗑️ Item deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
