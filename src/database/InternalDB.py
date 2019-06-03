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
Internal movie database handler
"""

import os
import json

import logging

__author__ = 'Hossain Mahmud'
logger = logging.getLogger(__name__)


class InternalDB(object):
    """
    Implements operations on the internal movie database
    """

    def __init__(self):
        # hack the location of the db !!
        self._location = os.path.join(os.path.dirname(__file__), '..', '..', 'movies')

    def get_movie_info(self, id):
        """

        :param id: Id of the movie
        :return: json object containing movie information or None
        """
        try:
            with open(os.path.join(self._location, str(id) + '.json')) as json_file:
                try:
                    data = json_file.read();
                    parsed = json.loads(data)
                    return parsed
                except IOError as ioex:
                    logger.error("Error occured while reading file {file}.json".format(file=ioex))
                except Exception as ex:
                    logger.error("Json parsing failed with following error {err".format(err=ex))

        except FileNotFoundError as ex:
            logger.info("Movie id {id} does not exist in internal DB".format(id=id))
        except IOError as ioex:
            logger.error("Error occured while accessing file {file} . {err}".format(
                file=os.path.join(self._location, id, '.json'), err=ioex))
        return None

    def get_movie_list(self):
        """
        Gets the list of internal movie IDs
        :return: list of internal movie IDs
        """
        return [os.path.splitext(file)[0]
                for file in os.listdir(self._location)
                if os.path.isfile(os.path.join(self._location, file)) and file.endswith('.json')]
