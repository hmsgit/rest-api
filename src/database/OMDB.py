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
OMDB handler
"""

import os
import json
import requests
import urllib

import logging

__author__ = 'Hossain Mahmud'
logger = logging.getLogger(__name__)


class OMDB(object):
    """
    Implements operations on the OMDB
    """

    def __init__(self):
        self._url = "http://www.omdbapi.com/"
        self._access_token = "testtoken"

    def get_movie_info(self, id):
        """

        :param id: Id of the movie
        :return: json object containing movie information or None
        """

        params = {
            'i': id,
            'apikey': self._access_token,
            'plot': "full"
        }

        res = requests.get(url=self._url, params=params)

        if res.status_code < 200 or res.status_code > 299:
            logger.info("OMDB request failed. HTTP status code: {code}".format(
                code=res.status_code))
            return None

        data = res.json()
        return data
