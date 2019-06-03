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
Test module for InternalDB
"""

import os
import unittest

__author__ = 'Hossain Mahmud'
from mock import patch, MagicMock
from tests.MockUtil import MockUtil

from database.InternalDB import InternalDB

_base_path = 'database.InternalDB.'


@patch(_base_path + 'logging', new=MagicMock())
class TestInternalDB(unittest.TestCase):  # pragma: no cover
    def setUp(self):

        # mock os
        self.m_os = MockUtil.fakeit(self, _base_path + 'os')
        # restore harmless path functions
        self.m_os.path.join = os.path.join
        self.m_os.path.dirname = os.path.dirname
        self.m_os.path.splitext = os.path.splitext

        self.m_json = MockUtil.fakeit(self, _base_path + 'json')

        self.db = InternalDB()
        self.db._location = "/my/awesome/directory"

        # test setup
        self.movie1_json = '{"title": "awesome movie"}'
        self.movie2_json = '{"title": "not so awesome movie"}'

        m_movie1_file = MagicMock()
        m_movie1_file.read.return_value = self.movie1_json

        m_movie2_file = MagicMock()
        m_movie2_file.read.return_value = self.movie2_json

        files = {
            "/my/awesome/directory/movie1.json": m_movie1_file,
            "/my/awesome/directory/movie2.json": m_movie2_file
        }

        # # monkey patch json.loads
        # json.loads = lambda _self: True

        self.mopen = MagicMock(side_effect=lambda v: files[v])

    def tearDown(self):
        pass

    def test_get_movie_info_success(self):
        self.m_json.loads.return_value = "this is a dictionary"

        with patch("builtins.open", self.mopen):
            info = self.db.get_movie_info('movie1')

        self.m_json.loads.called_once_with(self.movie1_json)
        self.assertEqual(info, "this is a dictionary")

    def test_get_movie_info_raises_exception(self):
        #self.mopen.side_effect = FileNotFoundError
        with patch("builtins.open", self.mopen):
            self.assertRaises(KeyError, self.db.get_movie_info, 'movie3')

        self.mopen.side_effect = IOError
        with patch("builtins.open", self.mopen):
            try:
                self.db.get_movie_info('movie2')
            except IOError as ex:
                self.assertFalse(False, "Should not raised IOError")

    def test_get_movie_info_json_raises_exception(self):
        self.m_json.loads.side_effect = Exception
        with patch("builtins.open", self.mopen):
            self.assertRaises(Exception, self.db.get_movie_info, 'movie1')

    def test_get_movie_list(self):
        list_dir = ['movie1.txt', 'movie2.json', 'movie3.json', 'somedir/']

        self.m_os.path.isfile.side_effect = [True, True, True, False]

        self.m_os.listdir.return_value = list_dir

        movie_list = self.db.get_movie_list()
        self.m_os.listdir.called_once_with(list_dir)

        self.assertEqual(movie_list, ['movie2', 'movie3'])


if __name__ == '__main__':
    unittest.main()
