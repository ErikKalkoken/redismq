# Redis Message Queue

This package contains a simple message queue based on Redis.

Basic example:

```
from redis import Redis
from redismq import RedisMQ

conn = Redis()
q = RedisMQ(conn, 'example_queue')
q.enqueue('Hello, World!')
message = q.dequeue()
print(message)
```

See also the examples folder for examples.