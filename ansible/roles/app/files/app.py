#!/usr/bin/env python3
"""
Flask DevOps Lab Application

A simple Flask web application that demonstrates:
- Database connectivity with PostgreSQL
- Docker containerization
- Reverse proxy setup with Nginx
- Basic CRUD operations 
"""

import os
import psycopg2 # PostgreSQL driver
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import logging

# Configure logging for better debugging in containerized environment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '192.168.61.11'),
    'database': os.environ.get('DB_NAME', 'devops_lab'),
    'user': os.environ.get('DB_USER', 'lab_user'),
    'password': os.environ.get('DB_PASSWORD', 'lab_password'),
    'port': os.environ.get('DB_PORT', '5432')
}

def get_db_connection():
    """
    Establish connection to PostgreSQL database.
    Returns connection object or None if connection fails.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None

def init_database():
    """
    Initialize database tables if they don't exist.
    Creates a simple 'visitors' table to demonstrate database operations.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor() # Create a cursor to execute SQL commands
            # Create a simple table to track visitor information
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visitors (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    message TEXT
                );
            """)
            conn.commit()
            logger.info("Database tables initialized successfully")
        except psycopg2.Error as e:
            logger.error(f"Database initialization failed: {e}")
        finally:
            cursor.close()
            conn.close()


# Initialize database on startup
init_database()

@app.route('/')
def index():
    """
    Main page displaying visitor statistics and a form to add new visitors.
    """

    conn = get_db_connection()
    visitors = []
    visitor_count = 0
    
    if conn:
        try:
            cursor = conn.cursor()
            # Get total visitor count
            cursor.execute("SELECT COUNT(*) FROM visitors;")
            visitor_count = cursor.fetchone()[0]
            
            # Get recent visitors (last 10)
            cursor.execute("""
                SELECT name, email, visit_time, message 
                FROM visitors 
                ORDER BY visit_time DESC 
                LIMIT 10;
            """)
            visitors = cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Database query failed: {e}")
        finally:
            cursor.close()
            conn.close()
    
    return render_template('index.html', 
                         visitors=visitors, 
                         visitor_count=visitor_count,
                         db_status='Connected' if conn else 'Disconnected')

@app.route('/add_visitor', methods=['POST'])
def add_visitor():
    """
    Add a new visitor to the database.
    """
    name = request.form.get('name')
    email = request.form.get('email', '')
    message = request.form.get('message', '')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO visitors (name, email, message) 
                VALUES (%s, %s, %s);
            """, (name, email, message))
            conn.commit()
            logger.info(f"New visitor added: {name}")
        except psycopg2.Error as e:
            logger.error(f"Failed to add visitor: {e}")
            return jsonify({'error': 'Database operation failed'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500
    
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """
    Health check endpoint for container orchestration.
    """
    conn = get_db_connection()
    db_status = 'healthy' if conn else 'unhealthy'
    
    if conn:
        conn.close()
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
def api_stats():
    """
    API endpoint returning visitor statistics in JSON format.
    Useful for monitoring and external integrations.
    """
    conn = get_db_connection()
    stats = {'total_visitors': 0, 'recent_visitors': []}
    
    if conn:
        try:
            cursor = conn.cursor()
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM visitors;")
            stats['total_visitors'] = cursor.fetchone()[0]
            
            # Get recent visitors
            cursor.execute("""
                SELECT name, visit_time 
                FROM visitors 
                ORDER BY visit_time DESC 
                LIMIT 5;
            """)
            recent = cursor.fetchall()
            stats['recent_visitors'] = [
                {'name': row[0], 'visit_time': row[1].isoformat()} 
                for row in recent
            ]
        except psycopg2.Error as e:
            logger.error(f"Stats query failed: {e}")
        finally:
            cursor.close()
            conn.close()
    
    return jsonify(stats)

if __name__ == '__main__':    
    # Run the application
    # In production, use a proper WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
