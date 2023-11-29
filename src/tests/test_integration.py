import unittest
from src.api.main import app, users


class TestAppIntegration(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_user_lifecycle(self):
        """
        Test user lifecycle: create, read, update, delete
        """
        new_user_data = {'name': 'Jakub', 'lastname': 'Teterycz'}
        response = self.app.post('/users', json=new_user_data)
        self.assertEqual(response.status_code, 201)

        new_user_id = response.json['id']

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        users_list = response.json
        self.assertTrue(any(user['id'] == new_user_id for user in users_list))

        updated_user_data = {'name': 'Jakub Updated', 'lastname': 'Teterycz Updated'}
        response = self.app.put(f'/users/{new_user_id}', json=updated_user_data)
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/users/{new_user_id}')
        self.assertEqual(response.status_code, 200)
        updated_user = response.json
        self.assertEqual(updated_user['name'], 'Jakub Updated')
        self.assertEqual(updated_user['lastname'], 'Teterycz Updated')

        response = self.app.delete(f'/users/{new_user_id}')
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/users/{new_user_id}')
        self.assertEqual(response.status_code, 404)

    def test_put_route_update_or_create_user(self):
        """
        PUT /users/<int:user_id> should update user if exists or create new one if not
        """
        existing_user_data = {'name': 'Existing', 'lastname': 'User'}
        response = self.app.post('/users', json=existing_user_data)
        existing_user_id = response.json['id']

        updated_user_data = {'name': 'Updated', 'lastname': 'User'}
        response = self.app.put(f'/users/{existing_user_id}', json=updated_user_data)
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/users/{existing_user_id}')
        self.assertEqual(response.status_code, 200)
        updated_user = response.json
        self.assertEqual(updated_user['name'], 'Updated')

        new_user_data = {'name': 'New', 'lastname': 'User'}
        response = self.app.put(f'/users/{existing_user_id}', json=new_user_data)
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/users/{existing_user_id}')
        self.assertEqual(response.status_code, 200)
        updated_user = response.json
        self.assertEqual(updated_user['name'], 'New')


if __name__ == '__main__':
    unittest.main()
