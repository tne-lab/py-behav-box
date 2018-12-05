#!/usr/bin/env python
# whisker/rawsocketclient.py

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

**Framework for Whisker Python clients using raw sockets.**

**CONSIDER USING THE TWISTED OR QT FRAMEWORKS INSTEAD.**

- Created: 18 Aug 2011.
- Last update: 10 Feb 2016

"""

# =============================================================================
# Dependencies
# =============================================================================

import logging
import re
import socket
import time
from typing import Generator, Union

from whisker.socket import (
    get_port,
    socket_receive,
    socket_send,
    socket_sendall,
)

log = logging.getLogger(__name__)


# =============================================================================
# Basic Whisker class, in which clients do all the work
# =============================================================================

class WhiskerRawSocketClient(object):
    """
    Basic Whisker class, in which clients do all the work via raw network
    sockets.

    (Not sophisticated. Use :class:`whisker.twistedclient.WhiskerTwistedTask`
    instead.)
    """

    def __init__(self) -> None:
        self.mainsock = None
        self.immsock = None

    @classmethod
    def set_verbose_logging(cls, verbose: bool) -> None:
        """
        Set the Python log level.
        """
        if verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

    def connect_both_ports(self, server: str,
                           mainport: Union[str, int]) -> bool:
        """
        Connect the main and immediate ports to the server.
        """
        if not self.connect_main(server, mainport):  # Log in to the server.
            return False
        # Listen to the server until we can connect the immediate socket.
        immport = None
        for line in self.getlines_mainsock():
            # The server has sent us a message via the main socket.
            log.debug("SERVER: " + line)
            m = re.search(r"^ImmPort: (\d+)", line)
            if m:
                immport = m.group(1)
            m = re.search(r"^Code: (\w+)", line)
            if m:
                code = m.group(1)
                if not self.connect_immediate(server, immport, code):
                    return False
                break
        return True

    def connect_main(self, server: str, portstring: Union[str, int]) -> bool:
        """
        Connect the main port to the server.
        """
        log.info("Connecting main port to server.")
        port = get_port(portstring)
        proto = socket.getprotobyname("tcp")
        try:
            self.mainsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                          proto)
            self.mainsock.connect((server, port))
        except socket.error as x:
            # "except socket.error, msg" used to work; see
            # http://stackoverflow.com/questions/2535760
            self.mainsock.close()
            self.mainsock = None
            log.error("ERROR creating/connecting main socket: " + str(x))
            return False
        log.info("Connected to main port " + str(port) +
                 " on server " + server)

        # Disable the Nagle algorithm:
        self.mainsock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        return True

    def connect_immediate(self, server: str, portstring: Union[str, int],
                          code: str) -> bool:
        """
        Connect the immediate port to the server.
        """
        port = get_port(portstring)
        proto = socket.getprotobyname("tcp")
        try:
            self.immsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                         proto)
            self.immsock.connect((server, port))
        except socket.error as x:
            self.immsock.close()
            self.immsock = None
            log.error("ERROR creating/connecting immediate socket: " +
                      str(x))
            return False
        log.info("Connected to immediate port " + str(port) +
                 " on server " + server)

        # Disable the Nagle algorithm:
        self.immsock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.immsock.setblocking(True)
        self.send_immediate("Link " + code)
        sleeptime = 0.1
        log.info("Sleeping for " + str(sleeptime) +
                 " seconds as the Nagle-disabling feature of Python "
                 "isn't working properly...")
        time.sleep(sleeptime)
        # the Nagle business isn't working; the Link packet is getting
        # amalgamated with anything the main calling program starts to send.
        # So pause.
        log.info("... continuing. Immediate socket should now be "
                 "correctly linked.")
        return True

    def log_out(self) -> None:
        """
        Shut down the connection to Whisker.
        """
        try:
            self.mainsock.close()
        except socket.error as x:
            log.error("Error closing main socket: " + str(x))
        try:
            self.immsock.close()
        except socket.error as x:
            log.error("Error closing immediate socket: " + str(x))

    def send(self, s: str) -> None:
        """
        Send something to the server on the main socket, with a trailing
        newline.
        """
        log.debug("Main socket command: " + s)
        socket_send(self.mainsock, s + "\n")

    def send_immediate(self, s: str) -> str:
        """
        Send a command to the server on the immediate socket, and retrieve
        its reply.
        """
        log.debug("Immediate socket command: " + s)
        socket_sendall(self.immsock, s + "\n")
        reply = next(self.getlines_immsock())
        log.debug("Immediate socket reply: " + reply)
        return reply

    def getlines_immsock(self) -> Generator[str, None, None]:
        """
        Yield a set of lines from the immediate socket.
        """
        # http://stackoverflow.com/questions/822001/python-sockets-buffering
        buf = socket_receive(self.immsock)
        done = False
        while not done:
            if "\n" in buf:
                (line, buf) = buf.split("\n", 1)
                yield line
            else:
                more = socket_receive(self.immsock)
                if not more:
                    done = True
                else:
                    buf += more
        if buf:
            yield buf

    def getlines_mainsock(self) -> Generator[str, None, None]:
        """
        Yield a set of lines from the main socket.
        """
        buf = socket_receive(self.mainsock)
        done = False
        while not done:
            if "\n" in buf:
                (line, buf) = buf.split("\n", 1)
                yield line
            else:
                more = socket_receive(self.mainsock)
                if not more:
                    done = True
                else:
                    buf += more
        if buf:
            yield buf
