# A simple REST API demonstrating data manipulation
# Copyright (C) 2019  Hossain Mahmud
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Implements utility class for handling movie json
"""


class Util:
    """
    Utility class for handling movie json
    """
    @staticmethod
    def combine(internal, omdb):
        """
        Combines jsons based on following rules
        * Title overwrites title
        * Plot overwrites description
        * duration overwrites Runtime
        * userrating will become part of Ratings, applying a similar logic as current Ratings
        * Director, Writer and Actors should be transformed from String to an String[]
        * Other fields merged into the resulting JSON without transformation

        :param internal: json object read from internal db
        :param omdb: json object read from external omdb
        :return: combined json
        """

        preferences = [
            ['Title', 'title'],
            ['Plot', 'description'],
            ['duration', 'Runtime']
        ]

        to_arrayfy = ['Director', 'Writer', 'Actors', 'Language', 'Genre']

        combined = {**omdb, **internal}

        # choose preferred items
        for item in preferences:
            if item[0] in combined and item[1] in combined:
                del combined[item[1]]

        # convert strings to lists
        for item in to_arrayfy:
            if item in combined:
                combined[item] = [elem.lstrip().rstrip() for elem in combined[item].split(',')]

        if 'userrating' in combined:
            total = 0
            for i in range(1, 6):
                total += (combined['userrating']['countStar' + str(i)] * i
                          if 'countStar' + str(i) in combined['userrating']
                          else 0);

            if 'Ratings' not in combined:
                combined['Ratings'] = []

            combined['Ratings'].append(
                {
                    "Source": "7tv",
                    "Value": str(round(total / combined['userrating']['countTotal'], 2)) + '/5.0'
                }
            )

            del combined['userrating']

        return combined
