#!/usr/bin/env python
# whisker/socket.py

"""
===============================================================================

    Copyright (C) 2011-2018 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of the Whisker Python client library.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

===============================================================================

**Low-level network socket functions.**

"""

import re
import socket
from typing import Union

from whisker.constants import BUFFERSIZE


def get_port(x: Union[str, int]) -> int:
    """
    Works out an integer TCP/IP port number.

    Args:
        x: port number or name

    Returns:
        port number

    Raises:
        ValueError: bad value
        TypeError: bad type

    """
    if type(x) is int:
        return x
    m = re.match(r"\D", x)  # search for \D = non-digit characters
    if m:
        port = socket.getservbyname(x, "tcp")
    else:
        port = int(x)
    return port


# In Python 3, we work with strings within the client code, and bytes
# to/from the socket. Translation occurs here:


def socket_receive(sock: socket.socket, bufsize: int = BUFFERSIZE) -> str:
    """
    Receives ASCII data from a socket and returns a string.

    Args:
        sock: TCP/IP socket
        bufsize: buffer size

    Returns:
        data as a string
    """
    # return socket.recv(bufsize)  # Python 2
    return sock.recv(bufsize).decode('ascii')  # Python 3


def socket_sendall(sock: socket.socket, data: str) -> None:
    """
    Sends all the data specified to a network socket, encoded via ASCII.

    See https://stackoverflow.com/questions/34252273.
    """
    # return socket.sendall(data)  # Python 2
    return sock.sendall(data.encode('ascii'))  # Python 3


def socket_send(sock: socket.socket, data: str) -> int:
    """
    Sends some of the data to a network socket, encoded via ASCII,
    and returns the number of bytes actually sent.

    See https://stackoverflow.com/questions/34252273.
    """
    # return socket.send(data)  # Python 2
    return sock.send(data.encode('ascii'))  # Python 3
