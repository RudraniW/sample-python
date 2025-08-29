#!/usr/bin/env python3
"""
Sample Flask application for Harness CI pipeline demonstration.
"""

from flask import Flask, jsonify, request
import os
import datetime
import json

app = Flask(__name__)

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['PORT'] = int(os.getenv('PORT', 5000))


@app.route('/')
def home():
    """Home endpoint returning basic app info."""
    return jsonify({
        'message': 'Hello from Harness CI Python Sample!',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'timestamp': datetime.datetime.utcnow().isoformat()
    })


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/users')
def get_users():
    """Sample API endpoint returning user data."""
    users = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'},
        {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com'}
    ]
    return jsonify(users)


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculator API for mathematical operations."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        a = data.get('a')
        b = data.get('b')
        operation = data.get('operation')
        
        if a is None or b is None or not operation:
            return jsonify({'error': 'Missing required parameters: a, b, operation'}), 400
        
        # Convert to numbers
        try:
            a = float(a)
            b = float(b)
        except (ValueError, TypeError):
            return jsonify({'error': 'Parameters a and b must be numbers'}), 400
        
        # Perform calculation
        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            if b == 0:
                return jsonify({'error': 'Cannot divide by zero'}), 400
            result = a / b
        elif operation == 'power':
            result = a ** b
        else:
            return jsonify({'error': 'Invalid operation. Use: add, subtract, multiply, divide, power'}), 400
        
        return jsonify({
            'result': result,
            'operation': f"{a} {operation} {b} = {result}",
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = app.config['PORT']
    debug = app.config['DEBUG']
    
    print(f"Starting Flask app on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
