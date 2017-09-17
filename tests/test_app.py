#!/usr/bin/env python3

import json
import unittest
import os


class AppTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['APP_DATABASE_URI'] = 'sqlite:///:memory:'
        from entries import app
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        self.client = None

    def test_status(self):
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True).strip(),
                         json.dumps('OK'))

    def test_list_entries(self):
        response = self.client.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        entries = json.loads(response.get_data(as_text=True))
        self.assertEqual(type(entries), list)

    def test_new_entry(self):
        # Create a new entry
        entry = {
            'description': 'Test Entry',
            'comment': 'Test Entry'
        }
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(entry),
                                    content_type='application/json')
        # Check whether the return was correct
        self.assertEqual(response.status_code, 200)
        new_entry = json.loads(response.get_data(as_text=True))
        self.assertEqual(new_entry['comment'], entry['comment'])
        self.assertEqual(new_entry['description'], entry['description'])
        self.assertIsNotNone(new_entry['id'])
        # Also check whether it is correct inside the system
        response = self.client.get('/api/v1/entries/%s' % new_entry['id'])
        retrieved_entry = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(retrieved_entry['id'], new_entry['id'])
        self.assertEqual(retrieved_entry['comment'], new_entry['comment'])
        self.assertEqual(retrieved_entry['description'],
                         new_entry['description'])

    def test_edit_entry(self):
        # Create a new entry
        entry = {
            'description': 'Test Edit Entry',
            'comment': 'Test Edit Entry'
        }
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(entry),
                                    content_type='application/json')
        # Recover its id and edit it
        new_entry = json.loads(response.get_data(as_text=True))
        new_id = new_entry['id']
        edited_entry = {
            'description': 'Edited Entry',
            'comment': 'Edited Entry'
        }
        response = self.client.post('/api/v1/entries/%s' % new_id,
                                    data=json.dumps(edited_entry),
                                    content_type='application/json')
        # Check whether the return was correct
        new_entry = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_entry['id'], new_id)
        self.assertEqual(new_entry['comment'], edited_entry['comment'])
        self.assertEqual(new_entry['description'], edited_entry['description'])
        # Also check whether it is correct inside the system
        response = self.client.get('/api/v1/entries/%s' % new_id)
        retrieved_entry = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(retrieved_entry['id'], new_id)
        self.assertEqual(retrieved_entry['comment'], edited_entry['comment'])
        self.assertEqual(retrieved_entry['description'],
                         edited_entry['description'])

    def test_remote_entry(self):
        # Create a new entry
        entry = {
            'description': 'Test Delete Entry',
            'comment': 'Test Delete Entry'
        }
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(entry),
                                    content_type='application/json')
        # Recover its id and remove it
        new_entry = json.loads(response.get_data(as_text=True))
        new_id = new_entry['id']
        response = self.client.delete('/api/v1/entries/%s' % new_id)
        # Check whether the return was correct
        deleted_entry = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(deleted_entry['id'], new_id)
        self.assertEqual(deleted_entry['comment'], entry['comment'])
        self.assertEqual(deleted_entry['description'], entry['description'])
        # Also check whether it was really removed from inside the system
        response = self.client.get('/api/v1/entries/%s' % new_id)
        retrieved_entry = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(retrieved_entry, '')


if __name__ == '__main__':
    unittest.main()
