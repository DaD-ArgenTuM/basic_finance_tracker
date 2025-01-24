import sqlite3
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Function to create the database and table if they don't exist
# Function to create the database and table if they don't exist
def init_db():
    if not os.path.exists('finance_tracker.db'):
        print("Database does not exist. Creating database...")
    else:
        print("Database already exists. Skipping creation.")

    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()

    # Create the transactions table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            timestamp TEXT,
            amount REAL,
            merchant TEXT,
            category TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database and table are ready.")


# Initialize the database (create tables if not already created)
init_db()

# Route to render the frontend (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch all transactions from the database
@app.route('/transactions')
@app.route('/transactions')
def transactions():
    print("Fetching transactions from the database...")
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM transactions')
        rows = cursor.fetchall()
        print(f"Fetched {len(rows)} transactions from the database.")
        transactions = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        transactions = []
    finally:
        conn.close()

    return jsonify(transactions)


# Route to fetch and insert dummy transactions into the database
@app.route('/fetch-transactions', methods=['POST'])
@app.route('/fetch-transactions', methods=['POST'])
def fetch_transactions():
    print("Fetching dummy transactions...")
    transactions = [
        {
            "transaction_id": "TX12345",
            "timestamp": "2025-01-01T12:00:00Z",
            "amount": 100.00,
            "merchant": "Merchant A",
            "category": "Groceries",
            "notes": "Payment for groceries"
        },
        {
            "transaction_id": "TX12346",
            "timestamp": "2025-01-02T14:30:00Z",
            "amount": 50.00,
            "merchant": "Merchant B",
            "category": "Entertainment",
            "notes": "Movie ticket"
        }
    ]

    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()

    try:
        for tx in transactions:
            print(f"Inserting transaction: {tx['transaction_id']}")
            cursor.execute('''
                INSERT INTO transactions (transaction_id, timestamp, amount, merchant, category, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                tx['transaction_id'], tx['timestamp'], tx['amount'], tx['merchant'], tx['category'], tx['notes']
            ))

        conn.commit()
        print("Transactions fetched and stored successfully!")
    except Exception as e:
        print(f"Error inserting transactions: {e}")
    finally:
        conn.close()

    return jsonify({"message": "Transactions fetched and stored successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
