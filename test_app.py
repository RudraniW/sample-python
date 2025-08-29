#!/usr/bin/env python3
"""
Unit tests for the Flask application.
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestBasicEndpoints:
    """Test basic application endpoints."""
    
    def test_home_endpoint(self, client):
        """Test home endpoint returns correct response."""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['message'] == 'Hello from Harness CI Python Sample!'
        assert data['version'] == '1.0.0'
        assert 'timestamp' in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_users_endpoint(self, client):
        """Test users API endpoint."""
        response = client.get('/api/users')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]['name'] == 'John Doe'
    
    def test_404_handler(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data


class TestCalculatorAPI:
    """Test calculator API functionality."""
    
    def test_addition(self, client):
        """Test addition operation."""
        response = client.post('/api/calculate', 
                             json={'a': 5, 'b': 3, 'operation': 'add'})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 8
    
    def test_subtraction(self, client):
        """Test subtraction operation."""
        response = client.post('/api/calculate',
                             json={'a': 10, 'b': 4, 'operation': 'subtract'})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 6
    
    def test_multiplication(self, client):
        """Test multiplication operation."""
        response = client.post('/api/calculate',
                             json={'a': 6, 'b': 7, 'operation': 'multiply'})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 42
    
    def test_division(self, client):
        """Test division operation."""
        response = client.post('/api/calculate',
                             json={'a': 15, 'b': 3, 'operation': 'divide'})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 5.0
    
    def test_division_by_zero(self, client):
        """Test division by zero handling."""
        response = client.post('/api/calculate',
                             json={'a': 10, 'b': 0, 'operation': 'divide'})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'Cannot divide by zero' in data['error']
    
    def test_power_operation(self, client):
        """Test power operation."""
        response = client.post('/api/calculate',
                             json={'a': 2, 'b': 3, 'operation': 'power'})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['result'] == 8
    
    def test_invalid_operation(self, client):
        """Test invalid operation handling."""
        response = client.post('/api/calculate',
                             json={'a': 5, 'b': 3, 'operation': 'invalid'})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'Invalid operation' in data['error']
    
    def test_missing_parameters(self, client):
        """Test missing parameters handling."""
        response = client.post('/api/calculate', json={'a': 5})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'Missing required parameters' in data['error']
    
    def test_invalid_data_types(self, client):
        """Test invalid data type handling."""
        response = client.post('/api/calculate',
                             json={'a': 'invalid', 'b': 3, 'operation': 'add'})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'must be numbers' in data['error']
