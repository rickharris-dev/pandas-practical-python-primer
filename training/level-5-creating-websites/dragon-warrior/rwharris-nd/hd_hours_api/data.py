"""
This module provides the Data class which can be used for creating,
retrieving, updating, and deleting Help Desk attributes and hours.
"""

import sqlite3

class Data:
    """
    Provides an interface to a SQLite database.
    """

    def __init__(self):
        self.connection = sqlite3.connect('/tmp/hd_hours.db')
        self.connection.row_factory = sqlite3.Row

    def get_attributes(self, team) -> dict:
        """
        Returns the current attribute settings for the specified team.

        Args:
            team: A str defining the target team.

        Returns:
            A dict of attributes for the given team.
        """
        cursor = self.connection.execute(
            'SELECT id, attribute_name, attribute_value '
            'FROM attributes '
            'WHERE lower(team)=?', [team.lower()])

        matched_attributes = cursor.fetchall()

        if matched_attributes:
            team_attributes = {}
            for row in matched_attributes:
                team_attributes[row['attribute_name']] = {}
                team_attributes[row['attribute_name']]['id'] = row['id']
                team_attributes[row['attribute_name']]['value'] = row['attribute_value']
            return team_attributes
        else:
            raise ValueError("No existing attributes were found matching "
                 "the '{}' team.".format(team))


    def get_attribute(self, team, attribute_name) -> str:
        """
        Returns the specified attribute for the given team.

        Args:
            team: A str defining the target team.
            attribute_name: A str naming the attribute being specified.

        Returns:
            A str of giving the value of the specified attribute for the given team.
        """
        cursor = self.connection.execute(
            'SELECT id, attribute_value '
            'FROM attributes '
            'WHERE lower(team)=? AND lower(attribute_name)=?',
            [team.lower(), attribute_name.lower()])

        row = cursor.fetchone()
        if row:
            team_attribute = {}
            team_attribute['id'] = row['id']
            team_attribute['attribute_value'] = row['attribute_value']
            return team_attribute
        else:
            raise ValueError("No existing attribute was found matching "
                             "'{}' for the '{}' team.".format(attribute_name, team))

    def get_attribute_by_id(self, id:str) -> str:
        """
        Returns the specified attribute for the given team.

        Args:
            team: A str defining the target team.
            attribute_name: A str naming the attribute being specified.

        Returns:
            A str of giving the value of the specified attribute for the given team.
        """
        cursor = self.connection.execute(
            'SELECT team, attribute_name, attribute_value '
            'FROM attributes '
            'WHERE lower(id)=?',
            [id.lower()])

        row = cursor.fetchone()
        if row:
            team_attribute = {}
            team_attribute['team'] = row['team']
            team_attribute['attribute_name'] = row['attribute_name']
            team_attribute['attribute_value'] = row['attribute_value']
            return team_attribute
        else:
            raise ValueError("No existing attribute was found matching "
                             " the id '{}'".format(id))

    def create_attribute(self, data:dict):
        """
        Creates new attribute record for the given team.

        Args:
            team: A str defining the target team.
            attribute_name: A str naming the attribute being specified.
            attribute_value: A str defining the value of the attribute.

        Raises:
            ValueError: If data is None, doesn't contain all required
                elements, or a duplicate attribute exists for the given team.
        """
        if data is None:
            raise ValueError(
                "'None' was received when a dict was expected during "
                "the attempt to create a new team attribute.")

        required_elements = {"team", "attribute_name", "attribute_value"}

        if not required_elements.issubset(data):
            raise ValueError("Some of the data required to create a team attribute "
                             "was not present.  The following elements "
                             "must be present to create the attribute: {}".format(
                             required_elements))

        for element in data:
            if element not in required_elements:
                data.pop(element)

        try:
            self.get_attribute(data['team'],data['attribute_name'])
        except:
            self.connection.execute(
                'INSERT INTO attributes (team, attribute_name, attribute_value) '
                'VALUES (?, ?, ?)',
                [data['team'],
                 data['attribute_name'],
                 data['attribute_value']])
            self.connection.commit()
        else:
            raise ValueError("A team attribute already exists "
                             "called {} for the '{}' team.".format(
                             data['attribute_name'], data['team']))

    def update_attribute(self, id:str, data: dict):
        """
        Updates the specified attribute for the given team.

        Args:
            team: A str defining the target team.
            attribute_name: A str naming the attribute being specified.
            attribute_value: A str defining the value of the attribute.

        Raises:
            ValueError: If data is None or if no matching attribute entry is found.
        """
        if data is None:
            raise ValueError(
                "'None' was received when a dict was expected during "
                "the attempt to update an existing attribute.")

        possible_elements = {"team", "attribute_name", "attribute_value"}

        try:
            matched_attribute = self.get_attribute_by_id(id)
        except ValueError:
            raise
        else:
            update = {}
            for element in possible_elements:
                if element in data:
                    update[element] = data[element]
                else:
                    update[element] = matched_attribute[element]
            self.connection.execute(
                'UPDATE attributes '
                'SET team=?, attribute_name=?, attribute_value=? '
                'WHERE lower(id) = ?',
                [update['team'],
                 update['attribute_name'],
                 update['attribute_value'],
                 id])

    def delete_attribute(self, id:str):
        """
        Deletes the given attribute for the specified team.

        Args:
            team: A str defining the target team.
            attribute_name: A str naming the attribute being specified.

        Raises:
            ValueError: If data is None or if no matching attribute entry is found.
        """
        try:
            matched_attribute = self.get_attribute_by_id(id)
        except ValueError:
            raise
        else:
            self.connection.execute(
                'DELETE '
                'FROM attributes '
                'WHERE lower(id) = ?',
                [id.lower()])
            self.connection.commit()

    def get_schedule(self, team, type) -> list:
        """
        Returns the schedule for the given team for the requested type.

        Args:
            team: A str defining the target team.
            type: A str defining the schedule type.

        Returns:
            Returns a list with the schedule for the specified team for the given type.
        """
        cursor = self.connection.execute(
            'SELECT id, day, start, end '
            'FROM schedules '
            'WHERE lower(team) = ?'
            'AND lower(type) = ?',
            [team.lower(),
             type.lower()])

        matched_schedule = cursor.fetchall()

        if matched_schedule:
            team_schedule = {}
            for row in matched_schedule:
                try:
                    team_schedule[row['day']]
                except:
                    team_schedule[row['day']] = {}
                count = len(team_schedule[row['day']])
                team_schedule[row['day']][count] = {}
                team_schedule[row['day']][count]['id'] = row['id']
                team_schedule[row['day']][count]['start'] = row['start']
                team_schedule[row['day']][count]['end'] = row['end']
            return team_schedule
        else:
            raise ValueError("No existing schedule was found matching "
                 "the '{}' team's '{}' schedule.".format(team, type))

    def get_hours(self, team, type, day) -> dict:
        """

        Args:
            team:
            type:
            day:

        Returns:

        """
        cursor = self.connection.execute(
            'SELECT id, start, end '
            'FROM schedules '
            'WHERE lower(team) = ? '
            'AND lower(type) = ? '
            'AND lower(day) = ?',
            [team.lower(),
             type.lower(),
             day.lower()])

        matched_schedule = cursor.fetchall()

        if matched_schedule:
            team_schedule = {}
            for row in matched_schedule:
                count = len(team_schedule)
                team_schedule[count] = {}
                team_schedule[count]['id']  = row['id']
                team_schedule[count]['start'] = row['start']
                team_schedule[count]['end'] = row['end']
            return team_schedule
        else:
            raise ValueError("No existing schedule was found matching "
                 "the '{}' team's '{}' schedule for the '{}' day.".format(
                team, type, day))

    def get_hours_by_id(self, id:str) -> dict:
        """

        Args:
            id:

        Returns:

        """
        cursor = self.connection.execute(
            'SELECT team, day, start, end '
            'FROM schedules '
            'WHERE lower(id) = ?',
            [id.lower()])

        row = cursor.fetchone()

        if row:
            team_schedule = {}
            team_schedule['team']  = row['team']
            team_schedule['day'] = row['day']
            team_schedule['start'] = row['start']
            team_schedule['end'] = row['end']
            return team_schedule
        else:
            raise ValueError("No existing schedule was found matching "
                 "the id: '{}'.".format(id))

    def create_hours(self, data):
        """

        Args:
            data:

        Returns:

        """
        if data is None:
            raise ValueError(
                "'None' was received when a dict was expected during "
                "the attempt to create a new team attribute.")

        required_elements = {"team", "day", "start", "end", "type"}

        if not required_elements.issubset(data):
            raise ValueError("Some of the data required to create a team attribute "
                             "was not present.  The following elements "
                             "must be present to create the attribute: {}".format(
                             required_elements))

        for element in data:
            if element not in required_elements:
                data.pop(element)

        try:
            cursor = self.connection.execute(
                'SELECT id '
                'FROM schedules '
                'WHERE lower(team) = ? '
                'AND lower(type) = ? '
                'AND lower(day) = ? '
                'AND lower(start) = ? '
                'AND lower(end) = ?',
                [data['team'].lower(),
                 data['type'].lower(),
                 data['day'].lower(),
                 data['start'].lower(),
                 data['end'].lower()])

            row = cursor.fetchone()

            id = row['id']
        except:
            self.connection.execute(
                'INSERT INTO schedules (team, type, day, start, end) '
                'VALUES (?, ?, ?, ?, ?)',
                [data['team'],
                 data['type'],
                 data['day'],
                 data['start'],
                 data['end']])
            self.connection.commit()
        else:
            raise ValueError("A schedule already exists "
                             "from {} to {} for the '{}' team "
                             "{} schudule on day {}.".format(
                             data['start'], data['end'], data['team'], data['type'], data['day']))

        #Need to work on script to check if schedules overlap.

    def update_hours(self, id, data):
        """

        Args:
            id:
            data:

        Returns:

        """
        if data is None:
            raise ValueError(
                "'None' was received when a dict was expected during "
                "the attempt to update an existing schedule.")

        possible_elements = {"start", "end"}

        try:
            matched_attribute = self.get_hours_by_id(id)
        except ValueError:
            raise
        else:
            update = {}
            for element in possible_elements:
                if element in data:
                    update[element] = data[element]
                else:
                    update[element] = matched_attribute[element]
            self.connection.execute(
                'UPDATE schedules '
                'SET start=?, end=? '
                'WHERE lower(id) = ?',
                [update['start'],
                 update['end'],
                 id])

    def delete_hours(self, id):
        """

        Args:
            id:

        Returns:

        """
        try:
            matched_attribute = self.get_hours_by_id(id)
        except ValueError:
            raise
        else:
            self.connection.execute(
                'DELETE '
                'FROM schedules '
                'WHERE lower(id) = ?',
                [id.lower()])
            self.connection.commit()