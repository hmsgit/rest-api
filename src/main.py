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
Entry point of the program. Starts a REST server.
"""

import sys
import argparse
import logging
from server import app

# pylint: disable=C0103
__author__ = 'Hossain Mahmud'
logger = logging.getLogger("main")

DEFAULT_PORT = 80
DEFAULT_HOST = '0.0.0.0'


if __name__ == '__main__':
    # setup logger
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(threadName)-12.12s] [%(name)-12.12s] [%(levelname)s]  %(message)s'))
    logger.addHandler(handler)

    # parse args for port
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='port')
    args = parser.parse_args()

    try:
        port = int(args.port)
    except (TypeError, ValueError) as _:
        logger.info("Using default port {port}".format(port=DEFAULT_PORT))
        port = DEFAULT_PORT

    # start the REST server
    app.run(host=DEFAULT_HOST, port=port, threaded=True)
