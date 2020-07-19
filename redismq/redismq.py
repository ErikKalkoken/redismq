from redis import Redis


class RedisMQ:
    """Defines a FIFO message queue using Redis"""

    def __init__(self, conn: Redis, name: str, base_name: str = "rqueue") -> None:
        """creates a queue on Redis with the given name
        
        Args:
        - conn: Redis connection object, e.g. conn = Redis()
        - name: name of this queue
        - base_name: name of this app which is added as prefix to the queue name on Redis
        """

        if not isinstance(conn, Redis):
            raise TypeError("conn must be of type Redis")

        self._conn = conn
        self._name = str(name)
        self._base_name = str(base_name)

    def _redis_key(self) -> str:
        """returns the full key used to address this queue on redis"""
        return "{}:{}".format(self.base_name, self.name)

    @property
    def conn(self) -> Redis:
        return self._conn

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_name(self) -> str:
        return self._base_name

    def size(self) -> int:
        """return current number of messages in the queue"""
        return self.conn.llen(self._redis_key())

    def enqueue(self, message: str) -> int:
        """enqueue one message int the queue
        
        returns size of the queue after enqueuing
        """
        self.conn.rpush(self._redis_key(), str(message))

    def enqueue_bulk(self, messages: list) -> int:
        """enqueue a list of messages into the queue at once
        
        returns size of the queue after enqueuing
        """
        queue_size = None
        for x in list(messages):
            queue_size = self.enqueue(x)

        return queue_size

    def dequeue(self) -> str:
        """dequeue one message from the queue. returns None if empty"""
        value = self.conn.lpop(self._redis_key())
        if value is not None:
            return value.decode("utf8")
        else:
            return None

    def dequeue_bulk(self, max: int = None) -> list:
        """dequeue a list of message from the queue.

        return no more than max message from queue
        returns all messages int the queue if max is not specified
        returns empty list if queue is empty
        """

        if max is not None and int(max) < 0:
            raise ValueError("max can not be negative")

        messages = list()
        n = 0
        while True:
            if max is not None and n == int(max):
                break
            else:
                n += 1
                x = self.dequeue()
                if x is None:
                    break
                else:
                    messages.append(x)

        return messages
