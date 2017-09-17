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
        entry = {
            'description': 'Test Entry',
            'comment': 'Test Entry'
        }
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(entry),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        new_entry = json.loads(response.get_data(as_text=True))
        self.assertEqual(new_entry['comment'], entry['comment'])
        self.assertEqual(new_entry['description'], entry['description'])
        self.assertIsNotNone(new_entry['id'])

if __name__ == '__main__':
    unittest.main()
