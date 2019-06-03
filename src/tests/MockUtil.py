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
Utility for mocking objects
"""

from mock import patch

__author__ = 'Hossain Mahmud'


class MockUtil(object):  # pragma: no cover

    @classmethod
    def fakeit(cls, test_object, target_module):
        """
        Create a mock, setup auto cleanup

        :param test_object: unittest.TestCase class for which target would be mocked
        :param target_module: module to be patched by mock.patch()
        :return: MagicMock() object obtained from patch.start()
        """

        test_object.patch = patch(target_module)
        test_object.addCleanup(test_object.patch.stop)
        return test_object.patch.start()

    @classmethod
    def any(cls):
        """
        Helper function to assert equal to anything, similar to mock.ANY.
        """
        class Ignore(object):
            """Equal to everything"""
            def __eq__(self, other):
                return True

        return Ignore()
