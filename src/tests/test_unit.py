import unittest
import json
from src.api.main import app, users


class TestAppUnit(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_start_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Welcome to my API!')

    def test_get_users_endpoint(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, users)

    def test_get_single_user_endpoint(self):
        user_id = 1
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, users[user_id - 1])

    def test_get_single_user_endpoint_not_found(self):
        user_id = 999
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {'error': 'User not found'})

    def test_create_user_endpoint(self):
        new_user_data = {"name": "Jakub", "lastname": "Teterycz"}
        response = self.app.post('/users', json=new_user_data)
        self.assertEqual(response.status_code, 201)
        user_id = json.loads(response.data.decode('utf-8'))['id']
        created_user = {"id": user_id, **new_user_data}
        self.assertIn(created_user, users)

    def test_create_user_endpoint_missing_data(self):
        new_user_data = {"name": "Jakub"}
        response = self.app.post('/users', json=new_user_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {'error': 'Name and lastname are required'})

    def test_update_user_endpoint(self):
        user_id = 1
        update_data = {"name": "UpdatedName"}
        response = self.app.patch(f'/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users[user_id - 1]['name'], update_data['name'])

    def test_update_user_endpoint_not_found(self):
        user_id = 999
        update_data = {"name": "UpdatedName"}
        response = self.app.patch(f'/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {'error': 'User not found'})

    def test_update_user_endpoint_invalid_data(self):
        user_id = 1
        update_data = {"invalid": "data"}
        response = self.app.patch(f'/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {'error': 'Invalid request body'})

    def test_delete_user_endpoint(self):
        new_user_data = {"name": "ToDelete", "lastname": "User"}
        response = self.app.post('/users', json=new_user_data)
        self.assertEqual(response.status_code, 201)
        user_id = json.loads(response.data.decode('utf-8'))['id']
        created_user = {"id": user_id, **new_user_data}
        self.assertIn(created_user, users)

        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(created_user, users)

    def test_delete_user_endpoint_not_found(self):
        user_id = 999
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {'error': 'User not found'})


if __name__ == '__main__':
    unittest.main()
