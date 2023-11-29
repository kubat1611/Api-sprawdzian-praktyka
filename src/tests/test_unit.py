import unittest
import json
from src.api.main import app
from src.api.main import start, get_users, get_user, create_user, update_user, delete_user, users, get_user_by_id


class TestAppUnit(unittest.TestCase):

    def test_start(self):
        response = start()
        self.assertEqual(response, 'Welcome to my API!')

    def test_get_users(self):
        with app.app_context():
            response, status_code = get_users()
            self.assertEqual(status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data), 3)

    def test_create_user(self):
        with app.app_context():
            user_data = {'name': 'John', 'lastname': 'Doe'}

            with app.test_request_context(method='POST', data=json.dumps(user_data), content_type='application/json'):
                response, status_code = create_user()

                self.assertEqual(status_code, 201)
                data = json.loads(response.get_data(as_text=True))
                self.assertIn('id', data)

                self.assertEqual(len(users), 3)
                new_user = users[-1]
                self.assertEqual(new_user['name'], 'John')
                self.assertEqual(new_user['lastname'], 'Doe')

    def test_get_user(self):
        with app.app_context():
            existing_user_id = 1
            existing_user_data = {'name': 'John', 'lastname': 'Doe'}
            users.append({'id': existing_user_id, **existing_user_data})

            response, status_code = get_user(existing_user_id)
            self.assertEqual(status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(data['id'], existing_user_id)

            non_existing_user_id = 999
            response, status_code = get_user(non_existing_user_id)
            self.assertEqual(status_code, 404)
            error_data = json.loads(response.get_data(as_text=True))
            self.assertEqual(error_data['error'], 'User not found')

    def test_update_user(self):
        with app.app_context():
            existing_user_id = 1
            existing_user_data = {'name': 'John', 'lastname': 'Doe'}
            users.append({'id': existing_user_id, **existing_user_data})

            updated_data = {'name': 'UpdatedName'}

            with app.test_request_context(method='PUT', data=json.dumps(updated_data), content_type='application/json'):
                response, status_code = update_user(existing_user_id)

                self.assertEqual(status_code, 204)

                updated_user = get_user_by_id(existing_user_id)
                self.assertEqual(updated_user['name'], 'UpdatedName')
                self.assertEqual(updated_user['lastname'], 'Doe')

    def test_delete_user(self):
        with app.app_context():
            user_id = 1
            response, status_code = delete_user(user_id)
            self.assertEqual(status_code, 204)


if __name__ == '__main__':
    unittest.main()
