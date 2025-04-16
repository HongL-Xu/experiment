import unittest
import json
import tempfile
import os
import sqlite3
from app import app
from database import Database

class TestDonationsApp(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Configure the app to use the temporary database
        app.config['TESTING'] = True
        app.config['DATABASE'] = self.db_path
        
        # Create a test client
        self.client = app.test_client()
        
        # Initialize the database
        self.db = Database(self.db_path)
        
        # Add some test data
        self.test_donation1_id = self.db.add_donation(
            donor_name="Test Donor 1",
            amount=100.0,
            date="2023-01-01",
            note="Test note 1"
        )
        
        self.test_donation2_id = self.db.add_donation(
            donor_name="Test Donor 2",
            amount=200.0,
            date="2024-01-01",
            note="Test note 2"
        )
    
    def tearDown(self):
        # Close the database connection
        if hasattr(self, 'db'):
            # Close any open connections to the database
            try:
                conn = sqlite3.connect(self.db_path)
                conn.close()
            except:
                pass
        
        # Close and remove the temporary database
        try:
            os.close(self.db_fd)
            os.unlink(self.db_path)
        except:
            pass
    
    def test_add_donation(self):
        """Test adding a new donation via POST request"""
        # Prepare test data
        test_data = {
            "donorName": "New Test Donor",
            "amount": 150.0,
            "date": "2024-05-15",
            "note": "New test note"
        }
        
        # Make the POST request
        response = self.client.post(
            '/api/donations',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        
        # Verify the donation was added to the database
        all_donations = self.db.get_all_donations()
        self.assertTrue(any(d['donor_name'] == "New Test Donor" for d in all_donations))
    
    def test_filter_by_year(self):
        """Test filtering donations by year"""
        # Test filtering for 2023
        response = self.client.get('/api/donations?year=2023')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['donor_name'], "Test Donor 1")
        
        # Test filtering for 2024
        response = self.client.get('/api/donations?year=2024')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['donor_name'], "Test Donor 2")
        
        # Test getting all donations (no year filter)
        response = self.client.get('/api/donations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    def test_delete_donation(self):
        """Test deleting a donation"""
        # Delete the first test donation
        response = self.client.delete(f'/api/donations/{self.test_donation1_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify the donation was deleted
        all_donations = self.db.get_all_donations()
        self.assertEqual(len(all_donations), 1)
        self.assertEqual(all_donations[0]['donor_name'], "Test Donor 2")
        
        # Try to delete a non-existent donation
        response = self.client.delete('/api/donations/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 