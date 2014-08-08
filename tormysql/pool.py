# -*- coding: utf-8 -*-
# 14-8-8
# create by: snower

from collections import deque
from tornado.concurrent import TracebackFuture
from tornado.ioloop import IOLoop
from client import Client

class Connection(Client):
    def __init__(self, pool, *args, **kwargs):
        self._pool = pool
        super(Connection, self).__init__(*args, **kwargs)

    def close(self):
        future = TracebackFuture()
        future.set_result(self._pool.release_connection(self))
        return future


class ConnectionPool(object):
    def __init__(self, max_connections, *args, **kwargs):
        self._max_connections = max_connections
        self._args = args
        self._kwargs = kwargs
        self._connections = deque()
        self._used_connections = []
        self._connections_count = 0
        self._wait_connections = deque()

    def init_connection(self, callback):
        def _(connection_future):
            if connection_future._exception is None and connection_future._exc_info is None:
                connection = connection_future._result
                callback(True, connection)
            else:
                callback(False, connection_future._exc_info)
        connection = Connection(self, *self._args, **self._kwargs)
        connection_future = connection.connect()
        self._connections_count +=1
        IOLoop.current().add_future(connection_future, _)

    def get_connection(self):
        future = TracebackFuture()
        if not self._connections:
            if self._connections_count < self._max_connections:
                def _(succed, result):
                    if succed:
                        self._used_connections.append(result)
                        future.set_result(result)
                    else:
                        future.set_exc_info(result)
                self.init_connection(_)
            else:
                self._wait_connections.append(future)
        else:
            connection = self._connections.popleft()
            self._used_connections.append(connection)
            future.set_result(connection)
        return future

    Connection = get_connection

    def release_connection(self, connection):
        if self._wait_connections:
            future = self._wait_connections.popleft()
            future.set_result(connection)
        else:
            self._used_connections.remove(connection)
            self._connections.append(connection)
