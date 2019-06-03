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
This module implements joint fetching of internal and omdb catalogues
"""

import logging
from flask_restful import Resource

from database.OMDB import OMDB
from database.InternalDB import InternalDB
from database.Util import Util

__author__ = 'Hossain Mahmud'
logger = logging.getLogger(__name__)


class MovieList(Resource):
    """
    Fetches the movie lists and combines with the OMDB data
    """
    def get(self, id):
        """
        Gets the movie information from all the databases

        :param id: movie id
        :return:
        """

        internal_data = InternalDB().get_movie_info(id)

        omdb_id = id
        if internal_data is not None and 'imdbId' in internal_data:
            omdb_id = internal_data['imdbId']

        # omdb_data = OMDB().get_movie_info(omdb_id)  # access token is required
        omdb_data = InternalDB().get_movie_info('test')

        return omdb_data if internal_data is None else Util.combine(internal_data, omdb_data)
