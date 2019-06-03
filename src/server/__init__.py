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
Setup the REST server
"""

import logging
from flask import Flask
from flask_restful import Api

# Import REST APIs
from server.__MovieLists import MovieList
from server.__MovieSearch import MovieSearch

__author__ = 'Hossain Mahmud'
logger = logging.getLogger("main")

app = Flask(__name__, static_folder='')
api = Api(app)

# Register /movies
api.add_resource(MovieList, '/api/movies/<string:id>')
api.add_resource(MovieSearch, '/api/movies')
