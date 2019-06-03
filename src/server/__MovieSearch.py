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
This module implements search on the movie catalogue feature
"""

import json
import logging
from flask import request
from flask_restful import Resource

from database.OMDB import OMDB
from database.InternalDB import InternalDB
from database.Util import Util

__author__ = 'Hossain Mahmud'
logger = logging.getLogger(__name__)


class MovieSearch(Resource):
    """
    Implements search on movie catalogue
    """
    def get(self):
        """
        Gets all movie info with matching filters

        :return: json list of all movie info
        """

        filters = {key.lower():val.lower() for (key, val) in request.args.items()}

        internal_db = InternalDB()
        omdb = OMDB()
        movie_list = internal_db.get_movie_list()

        movies_info = []

        for movie in movie_list:
            info = internal_db.get_movie_info(movie)

            if info is not None:
                if 'imdbId' in info:
                    # omdb_data = omdb.get_movie_info(info['imdbId'])  # access token is required
                    omdb_data = internal_db.get_movie_info('test')

                    info = Util.combine(info, omdb_data)

                if not filters:
                    movies_info.append(info)
                else:
                    is_match = True
                    for key, val in info.items():
                        if key.lower() in filters:
                            if type(val) is str or type(val) is int:
                                if filters[key.lower()].lower() != val.lower():
                                    is_match = False
                            elif type(val) is list:
                                if (filters[key.lower()].lower() not in
                                        [v.lower() for v in val]):
                                    is_match = False
                    if is_match:
                        movies_info.append(info)

        ret = json.dumps(movies_info)
        logger.debug("json object to return\n" + ret)
        return ret
