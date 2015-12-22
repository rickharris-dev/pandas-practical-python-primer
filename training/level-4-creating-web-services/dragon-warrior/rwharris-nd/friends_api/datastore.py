"""
This modules provides Datastore class which can be used for creating,
retrieving, updating, and deleting friend records from our database.
"""

import sqlite3

class Datastore:
    """
    Provides an interface to an SQLite database.
    """

    def __init__(self):
        self.connection = sqlite3.connect('/tmp/friends.db')

    def friends(self) -> list:
        """
        Return the current list of friends.

        Returns:
            A list of friends.
        """
        cursor = self.connection.execute(
            'SELECT id, firstName, lastName, telephone, email, notes '
            'FROM friends')

        friends = []
        for row in cursor.fetchall():
            friends.append(
                {"id": row[0],
                 "firstName": row[1],
                 "lastName": row[2],
                 "telephone": row[3],
                 "email": row[4],
                 "notes": row[5]})
        return friends

    def friend(self, id: str) -> dict:
        """
        Return data on a specific friend.

        Args:
            id: The unique identifier of a specific friend.

        Returns:
            A dict of data on the specified friend.

        Raises:
            ValueError: If no matching friend is found.
        """
        cursor = self.connection.execute(
            'SELECT id, firstName, lastName, telephone, email, notes '
            'FROM friends '
            'WHERE lower(id) = ?', [id.lower()])

        row = cursor.fetchone()

        if row:
            return {"id": row[0],
                 "firstName": row[1],
                 "lastName": row[2],
                 "telephone": row[3],
                 "email": row[4],
                 "notes": row[5]}
        else:
            raise ValueError("No existing friend was found matching id: {}".format(id))

    def create_friend(self, data: dict):
        """
        Create a new friend entry is our datastore of friends.

        Args:
            data: A dictionary of data for our new friend.  Must have
                the following elements: ['id', 'firstName', 'lastName',
                'telephone', 'email', 'notes']

        Raises:
            ValueError: If data is None, doesn't contain all required
                elements, or a duplicate id already exists in `friends`.
        """
        if data is None:
            raise ValueError(
                "`None` was received when a dict was expected during "
                "the attempt to create a new friend resource.")

        required_elements = {"id", "firstName", "lastName", "telephone",
                             "email", "notes"}

        if not required_elements.issubset(data):
            raise ValueError("Some of the data required to create a friend "
                             "was not present.  The following elements "
                             "must be present to create a friend: {}".format(
                required_elements))

        for element in data:
            if element not in required_elements:
                data.pop(element)
        try:
            self.friend(data['id'])
        except:
            self.connection.execute(
                'INSERT INTO friends (id, firstName, lastName, telephone, email, notes) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                [data['id'],
                 data['firstName'],
                 data['lastName'],
                 data['telephone'],
                 data['email'],
                 data['notes']])
            self.connection.commit()
        else:
            raise ValueError("A friend already exists with the "
                                 "`id` specified: {}".format(data['id']))

    def update_friend(self, id: str, data: dict):
        """
        Update an existing friend entry is our datastore of friends.

        Args:
            data: A dictionary of data to update an existing friend entry with.

        Raises:
            ValueError: If data is None or if no matching friend entry is found.
        """

        if data is None:
            raise ValueError(
                "`None` was received when a dict was expected during "
                "the attempt to update an existing friend resource.")

        required_elements = {"id", "firstName", "lastName", "telephone",
                             "email", "notes"}

        #TODO: Remove extraneous data elements.

        try:
            matched_friend = self.friend(id)
        except ValueError:
            raise
        else:
            self.connection.execute(
                'UPDATE friends '
                'SET id=?, firstName=?, lastName=?, telephone=?, email=?, notes=? '
                'WHERE lower(id) = ?',
                [data['id'],
                 data['firstName'],
                 data['lastName'],
                 data['telephone'],
                 data['email'],
                 data['notes'],
                 data['id'].lower()])
            self.connection.commit()

    def destroy_friend(self, id: str):
        """
        Remove an existing friend entry from our datastore of friends.

        Args:
            id: The id value of the friend to delete

        Returns:
            ValueError: If the 'id' parameter doesn't match any existing
            friend entries in our datastore.
        """
        try:
            matched_friend = self.friend(id)
        except ValueError:
            raise
        else:
            self.connection.execute(
                'DELETE '
                'FROM friends '
                'WHERE lower(id) = ?',
                [id.lower()])
            self.connection.commit()