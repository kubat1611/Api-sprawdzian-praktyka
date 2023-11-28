#Api-sprawdzian-praktyka
Endpoints
1. Get List of Users

    URL: /users
    Method: GET
    Description: Get a list of all users.

2. Get User by ID

    URL: /users/<int:user_id>
    Method: GET
    Description: Get user details by specifying the user ID.

3. Create User

    URL: /users
    Method: POST
    Description: Create a new user by providing a JSON payload with name and lastname.

4. Update User

    URL: /users/<int:user_id>
    Method: PATCH
    Description: Update an existing user by providing a JSON payload with the fields to be updated (name and/or lastname).

5. Create or Update User

    URL: /users/<int:user_id>
    Method: PUT
    Description: Create a new user if the user ID does not exist; otherwise, update the existing user with the provided data.

6. Delete User

    URL: /users/<int:user_id>
    Method: DELETE
    Description: Delete a user by specifying the user ID.
